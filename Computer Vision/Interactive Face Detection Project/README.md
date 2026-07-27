# Interactive Facial Detection Streamlit Web App

Public Streamlit app link: https://facedetecc-mini.streamlit.app/

A lightweight computer vision portfolio project that detects faces in images and
videos using MediaPipe's TFLite face detector and displays the results in a
Streamlit interface.

The app is designed to be compute-friendly. Images are processed immediately,
while video analysis uses an adjustable frame rate and duration limit.

## Features

- Upload JPG, JPEG, PNG, or WEBP images.
- Upload MP4, WEBM, MOV, AVI, or MKV videos.
- Choose any bundled image or video from the sample dropdown.
- Switch between short-range, full-range, and sparse full-range BlazeFace
  detectors.
- Adjust the minimum detection confidence from the sidebar.
- Run MediaPipe face detection with bundled TFLite models.
- Compare the original image and detected-face output side by side.
- View face count and detection time metrics.
- Download the detected-face image as a PNG.
- Configure how many video frames are analyzed per second.
- Preview and download a browser-compatible H.264 MP4 video.

## Project Structure

```text
.
|-- app.py                  # Streamlit app and MediaPipe detection pipeline
|-- blaze_face_short_range.tflite
|-- blaze_face_full_range.tflite
|-- blaze_face_full_range_sparse.tflite
|                            # Selectable MediaPipe face detector models
|-- sample_image_1.jpg      # Sample image
|-- sample_image_2.jpg      # Sample image
|-- sample_image_3.png      # Sample image
|-- sample_video_feed.mp4   # Sample video
|-- launch.bat              # Windows helper for launching the app
|-- requirements.txt        # Python dependencies
`-- README.md               # Project documentation
```

## Setup

This project was tested with Python 3.14.6.

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

Install dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Run the app:

```powershell
python -m streamlit run app.py
```

On Windows, you can also run:

```powershell
.\launch.bat
```

## Usage

1. Open the Streamlit URL shown in the terminal.
2. Upload an image or video, or choose an item from the sample dropdown.
3. Choose a detector model and adjust the confidence threshold if needed.
4. For videos, choose the analysis frame rate and maximum duration, then select
   **Process Video**.
5. Review the detection metrics and bounding-box output.
6. Optionally download the detected image or processed video.

## Notes

- This is a face detection project, not a face recognition or identity verification system.
- The three `blaze_face_*.tflite` files must stay in the same folder as
  `app.py`.
- Full Range Sparse is the default and is recommended for group scenes.
- Short Range is optimized for close, selfie-like framing.
- Changing the detector invalidates an existing processed-video result, so the
  video must be processed again with the newly selected model.
- An uploaded file takes precedence if a sample is also selected.
- Video output is sampled at the configured analysis frame rate and does not
  retain the source video's audio.
- Video encoding uses the FFmpeg binary bundled with `imageio-ffmpeg`. If that
  encoder is unavailable, the app tries several OpenCV codecs instead.
- The duration limit prevents long videos from monopolizing a Streamlit session.

## Possible Improvements

- Improve label styling for better readability on bright or busy images.
- Add an upscaling model for low-resolution images
- Add a downscaling model for high-resolution images
- Preserve audio in processed videos.
- Add real-time webcam support.
- Add facial landmark features
- Add facial recognition features

## Limitations

- Because this project prioritizes lightweight, accessible computation, the face detector may be less robust on challenging images, such as low-light scenes, small faces, side profiles, occlusions, or crowded group photos.
- Browser playback of uploaded AVI, MOV, or MKV files depends on browser codec
  support, although OpenCV may still be able to process them.
