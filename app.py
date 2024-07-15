import gradio as gr
import main
import json

def video_identity(video):
    video_path = video.name
    frames = main.extract_frames(video_path)
    pepsi_pts, cocacola_pts = main.detect_logos(frames)
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
    return json.dumps(output)


demo = gr.Interface(
    fn=video_identity,
    inputs=[
        "file",
    ],
    outputs="json"
)


if __name__ == "__main__":
    demo.launch()