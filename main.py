import os
import json
import av
from ultralytics import YOLO
from PIL import Image
from datetime import timedelta

# Paths
VIDEOS_DIR = '.'
video_path = os.path.join(VIDEOS_DIR, 'sample_video.mp4')
output_json_path = 'output.json'
model_path = os.path.join('.', 'runs', 'detect', 'train', 'weights', 'best.pt')

# Load YOLOv8 model
model = YOLO(model_path)  # Load a custom model

threshold = 0.5

def format_timestamp(seconds):
    # Convert seconds to timedelta and format as HH:MM:SS
    td = timedelta(seconds=seconds)
    return str(td)

def extract_frames(video_path):
    container = av.open(video_path)
    frames = []
    for frame in container.decode(video=0):
        # Convert timestamp to float seconds
        timestamp = float(frame.pts * frame.time_base)
        img = frame.to_image()
        frames.append((img, timestamp))
    return frames

def detect_logos(frames):
    pepsi_pts = []
    cocacola_pts = []

    for img, timestamp in frames:
        results = model(img)  # Run inference
        
        for result in results:
            boxes = result.boxes  # Boxes object for bounding box outputs

            for box in boxes:
                # Extract the bounding box and confidence
                x1, y1, x2, y2 = box.xyxy[0].tolist()  # Convert to list
                score = box.conf[0].item()  # Convert to float
                class_id = int(box.cls[0].item())  # Convert to int

                if score > threshold:
                    class_name = result.names[class_id].upper()
                    width = x2 - x1
                    height = y2 - y1
                    center_x = (x1 + x2) / 2
                    center_y = (y1 + y2) / 2
                    frame_center_x = img.width / 2
                    frame_center_y = img.height / 2
                    distance_from_center = ((center_x - frame_center_x) ** 2 + (center_y - frame_center_y) ** 2) ** 0.5

                    formatted_timestamp = format_timestamp(timestamp)
                    entry = {
                        "timestamp": formatted_timestamp,
                        "size": {"width": width, "height": height},
                        "distance_from_center": distance_from_center
                    }
                    
                    if class_name == 'PEPSI':
                        pepsi_pts.append(entry)
                    elif class_name == 'COCA-COLA':
                        cocacola_pts.append(entry)

    return pepsi_pts, cocacola_pts

def generate_output_json(pepsi_pts, cocacola_pts, output_path='output.json'):
    # Convert all values to strings for JSON serialization
    def to_serializable(obj):
        if isinstance(obj, (list, dict)):
            return obj
        elif hasattr(obj, 'tolist'):
            return obj.tolist()  # Convert numpy arrays or tensors
        elif hasattr(obj, 'item'):
            return obj.item()  # Convert single element tensors
        else:
            return str(obj)  # Convert other non-serializable objects to string

    output = {
        "Pepsi_pts": [entry["timestamp"] for entry in pepsi_pts],
        "CocaCola_pts": [entry["timestamp"] for entry in cocacola_pts],
        "Pepsi_details": [ {k: to_serializable(v) for k, v in entry.items()} for entry in pepsi_pts ],
        "CocaCola_details": [ {k: to_serializable(v) for k, v in entry.items()} for entry in cocacola_pts ]
    }
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=4)




def main(video_path):
    frames = extract_frames(video_path)
    pepsi_pts, cocacola_pts = detect_logos(frames)
    generate_output_json(pepsi_pts, cocacola_pts)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python main.py <video_path>")
        sys.exit(1)
    video_path = sys.argv[1]
    main(video_path)
