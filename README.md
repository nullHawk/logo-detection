# Coke-Pepsi Logo Detection

This project aims to detect Pepsi and Coca-Cola logos in video files using the YOLOv8 object detection model. The pipeline extracts frames from the video, processes them using the YOLOv8 model, and outputs the timestamps of detected logos in a JSON format.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Dependencies](#dependencies)

## Installation

### Setup the Codebase

1. Clone the repository:

    ```bash
    git clone https://github.com/nullHawk/logo-detection
    cd logo-detection
    ```

2. Install the dependencies using a virtual environment:

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```


## Usage

### Run the Pipeline

The pipeline accepts a video file (MP4 format) and outputs a JSON file with the timestamps of detected Pepsi and Coca-Cola logos.

1. Place your video file in the project directory.

2. Run the pipeline:

    ```bash
    python main.py your_video_file.mp4
    ```

3. The output JSON file will be saved as `output.json` in the project directory.

### Run using Gradio UI

1. Run the following python script
    ```bash
    python app.py
    ```
2. Upload the video and click on sumbit button

3. The output json will shown on the right side

### Example Output

The output JSON format:

```json
{
    "Pepsi_pts": [
        "00:01:23",
        "00:02:34",
        "00:03:45"
        // List of timestamps (HH:MM:SS) when Pepsi logos were detected
    ],
    "CocaCola_pts": [
        "00:05:12",
        "00:07:20",
        "00:08:45"
        // List of timestamps (HH:MM:SS) when CocaCola logos were detected
    ],
    "Pepsi_details": [
        {
            "timestamp": "00:01:23",
            "size": {
                "width": 50,
                "height": 30
            },
            "distance_from_center": 15.3
        }
        // More Pepsi details
    ],
    "CocaCola_details": [
        {
            "timestamp": "00:05:12",
            "size": {
                "width": 60,
                "height": 40
            },
            "distance_from_center": 10.0
        }
        // More CocaCola details
    ]
}
```
### Approach
- **Extract Frames**: Using av library to extract frames from the video.
- **YOLOv8 Detection**: Load the trained YOLOv8 model and run it on the extracted frames.
- **Generate Output**: Collect timestamps of frames where logos are detected and save them in a JSON file.

### Dependencies
- Python 3.8+
- av
- ultralytics(YOLOv8)
- gradio
