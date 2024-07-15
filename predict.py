from ultralytics import YOLO

model = YOLO("runs/detect/train3/weights/best.pt")  # load a custom model

results = model("sample_img.png")