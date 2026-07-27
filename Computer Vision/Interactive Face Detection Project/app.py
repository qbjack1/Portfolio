from io import BytesIO
from pathlib import Path
import hashlib
import tempfile
import time
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
from PIL import Image as PILImage
from PIL import ImageDraw
import streamlit as st


APP_DIR = Path(__file__).resolve().parent

DETECTOR_MODELS = {
    "BlazeFace Full Range Sparse (Recommended)": {
        "path": APP_DIR / "blaze_face_full_range_sparse.tflite",
        "description": (
            "Lightweight full-range model for group scenes and more distant faces."
        ),
    },
    "BlazeFace Full Range": {
        "path": APP_DIR / "blaze_face_full_range.tflite",
        "description": (
            "Full-range model that favors recall at a higher model size."
        ),
    },
    "BlazeFace Short Range": {
        "path": APP_DIR / "blaze_face_short_range.tflite",
        "description": (
            "Fast close-range model for selfies and webcam-style framing."
        ),
    },
}

SAMPLE_MEDIA = {
    "None": None,
    "Sample Image 1": APP_DIR / "sample_image_1.jpg",
    "Sample Image 2": APP_DIR / "sample_image_2.jpg",
    "Sample Image 3": APP_DIR / "sample_image_3.png",
    "Sample Video 1": APP_DIR / "sample_video_feed_1.mp4",
    "Sample video 2": APP_DIR / "sample_video_feed_2.mp4"
}

IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp"}
VIDEO_SUFFIXES = {".mp4", ".webm", ".mov", ".avi", ".mkv"}
VIDEO_MIME_TYPES = {
    ".mp4": "video/mp4",
    ".webm": "video/webm",
    ".mov": "video/quicktime",
    ".avi": "video/x-msvideo",
    ".mkv": "video/x-matroska",
}

APP_TITLE = "Facedetecc: An Interactive Facial Detection Project by QBjack"
GITHUB_REPO_1 = "https://github.com/qbjack1/facedetecc"
GITHUB_REPO_2 = "https://github.com/qbjack1/Portfolio"


@st.cache_resource
def load_mp_detector(model_path: str, min_confidence: float):
    base_options = python.BaseOptions(model_asset_path=model_path)
    options = vision.FaceDetectorOptions(
        base_options=base_options,
        running_mode=vision.RunningMode.IMAGE,
        min_detection_confidence=min_confidence,
    )
    return vision.FaceDetector.create_from_options(options)


def run_detection(image_np, detector):
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_np)

    start = time.perf_counter()
    results = detector.detect(mp_image)
    elapsed = time.perf_counter() - start

    return results, elapsed


def extract_detections(results, image_size):
    width, height = image_size
    detections = []

    for detection in results.detections or []:
        bbox = detection.bounding_box
        score = detection.categories[0].score

        x1 = max(0, bbox.origin_x)
        y1 = max(0, bbox.origin_y)
        x2 = min(width, bbox.origin_x + bbox.width)
        y2 = min(height, bbox.origin_y + bbox.height)

        detections.append(
            {
                "x": x1,
                "y": y1,
                "w": max(0, x2 - x1),
                "h": max(0, y2 - y1),
                "score": score,
            }
        )

    return detections


def draw_detections(image, detections):
    result = image.copy()
    draw = ImageDraw.Draw(result)

    for detection in detections:
        x = detection["x"]
        y = detection["y"]
        w = detection["w"]
        h = detection["h"]
        score = detection["score"]

        draw.rectangle((x, y, x + w, y + h), outline="red", width=4)
        label = f"{score:.2f}"
        label_box = draw.textbbox((x, y), label)
        label_width = label_box[2] - label_box[0]
        label_height = label_box[3] - label_box[1]
        label_y = max(0, y - label_height - 6)
        draw.rectangle(
            (x, label_y, x + label_width + 8, label_y + label_height + 6),
            fill="red",
        )
        draw.text((x + 4, label_y + 3), label, fill="white")

    return result


def get_media_kind(filename):
    suffix = Path(filename).suffix.lower()
    if suffix in IMAGE_SUFFIXES:
        return "image"
    if suffix in VIDEO_SUFFIXES:
        return "video"
    return None


def safe_download_stem(filename):
    stem = Path(filename).stem
    safe_stem = "".join(
        character if character.isalnum() or character in {"-", "_"} else "_"
        for character in stem
    )
    return safe_stem[:80] or "processed_video"


def create_video_writer(output_directory, frame_size, fps):
    ffmpeg_error = None
    writer = None

    try:
        import imageio_ffmpeg

        output_path = output_directory / "detected_faces.mp4"
        writer = imageio_ffmpeg.write_frames(
            str(output_path),
            frame_size,
            pix_fmt_in="rgb24",
            pix_fmt_out="yuv420p",
            fps=fps,
            quality=6,
            codec="libx264",
            macro_block_size=2,
            ffmpeg_log_level="error",
            output_params=["-movflags", "+faststart"],
        )
        writer.send(None)
        return {
            "writer": writer,
            "backend": "ffmpeg",
            "output_path": output_path,
            "mime_type": "video/mp4",
            "file_extension": ".mp4",
            "encoder": "H.264 (bundled FFmpeg)",
            "playback_warning": None,
        }
    except Exception as error:
        ffmpeg_error = error
        if writer is not None:
            try:
                writer.close()
            except Exception:
                pass

    fallback_options = (
        ("VP80", ".webm", "video/webm", None),
        (
            "mp4v",
            ".mp4",
            "video/mp4",
            "The fallback MP4 codec may not play in every browser. "
            "The downloaded file can still be opened in a desktop video player.",
        ),
        (
            "MJPG",
            ".avi",
            "video/x-msvideo",
            "The fallback AVI codec may not play in the browser. "
            "Download the file to view it in a desktop video player.",
        ),
    )

    for codec, extension, mime_type, playback_warning in fallback_options:
        output_path = output_directory / f"detected_faces{extension}"
        writer = cv2.VideoWriter(
            str(output_path),
            cv2.VideoWriter_fourcc(*codec),
            fps,
            frame_size,
        )
        if writer.isOpened():
            return {
                "writer": writer,
                "backend": "opencv",
                "output_path": output_path,
                "mime_type": mime_type,
                "file_extension": extension,
                "encoder": f"{codec} (OpenCV fallback)",
                "playback_warning": playback_warning,
            }
        writer.release()

    raise ValueError(
        "No compatible video encoder is available. Reinstall the dependencies "
        "from requirements.txt and try again."
    ) from ffmpeg_error


def process_video(
    video_bytes,
    source_suffix,
    detector,
    target_fps,
    max_duration_seconds,
    progress_callback=None,
):
    source_suffix = source_suffix if source_suffix in VIDEO_SUFFIXES else ".mp4"

    with tempfile.TemporaryDirectory() as temp_directory:
        temp_path = Path(temp_directory)
        input_path = temp_path / f"input{source_suffix}"
        input_path.write_bytes(video_bytes)

        capture = cv2.VideoCapture(str(input_path))
        if not capture.isOpened():
            raise ValueError("OpenCV could not open this video format.")

        source_fps = capture.get(cv2.CAP_PROP_FPS)
        if not np.isfinite(source_fps) or source_fps <= 0:
            source_fps = 24.0

        total_source_frames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_stride = max(1, round(source_fps / target_fps))
        output_fps = source_fps / frame_stride
        max_source_frames = max(1, int(source_fps * max_duration_seconds))
        frames_to_read = (
            min(total_source_frames, max_source_frames)
            if total_source_frames > 0
            else max_source_frames
        )

        writer_info = None
        frames_read = 0
        frames_analyzed = 0
        total_face_detections = 0
        max_faces_in_frame = 0
        total_inference_time = 0.0
        processing_started = time.perf_counter()

        try:
            while frames_read < frames_to_read:
                frame_ok, frame_bgr = capture.read()
                if not frame_ok:
                    break

                current_frame = frames_read
                frames_read += 1

                if current_frame % frame_stride != 0:
                    continue

                frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
                image = PILImage.fromarray(frame_rgb)
                results, elapsed = run_detection(frame_rgb, detector)
                detections = extract_detections(results, image.size)
                annotated_image = draw_detections(image, detections)
                annotated_rgb = np.ascontiguousarray(annotated_image)

                if annotated_rgb.shape[1] % 2 or annotated_rgb.shape[0] % 2:
                    annotated_rgb = annotated_rgb[
                        : annotated_rgb.shape[0] - (annotated_rgb.shape[0] % 2),
                        : annotated_rgb.shape[1] - (annotated_rgb.shape[1] % 2),
                    ]

                if writer_info is None:
                    height, width = annotated_rgb.shape[:2]
                    output_width = width - (width % 2)
                    output_height = height - (height % 2)
                    writer_info = create_video_writer(
                        temp_path,
                        (output_width, output_height),
                        output_fps,
                    )

                if writer_info["backend"] == "ffmpeg":
                    writer_info["writer"].send(annotated_rgb)
                else:
                    annotated_bgr = cv2.cvtColor(
                        annotated_rgb, cv2.COLOR_RGB2BGR
                    )
                    writer_info["writer"].write(annotated_bgr)

                frames_analyzed += 1
                face_count = len(detections)
                total_face_detections += face_count
                max_faces_in_frame = max(max_faces_in_frame, face_count)
                total_inference_time += elapsed

                if progress_callback is not None:
                    progress_callback(min(frames_read / frames_to_read, 1.0))
        finally:
            capture.release()
            if writer_info is not None:
                if writer_info["backend"] == "ffmpeg":
                    writer_info["writer"].close()
                else:
                    writer_info["writer"].release()

        if writer_info is None:
            raise ValueError("No readable frames were found in this video.")

        output_path = writer_info["output_path"]
        if not output_path.exists() or output_path.stat().st_size == 0:
            raise ValueError("The video encoder did not produce an output file.")

        processing_time = time.perf_counter() - processing_started
        truncated = (
            total_source_frames > max_source_frames
            or (total_source_frames <= 0 and frames_read >= max_source_frames)
        )

        return {
            "video_bytes": output_path.read_bytes(),
            "frames_analyzed": frames_analyzed,
            "average_faces": total_face_detections / frames_analyzed,
            "max_faces": max_faces_in_frame,
            "inference_time": total_inference_time,
            "processing_time": processing_time,
            "source_fps": source_fps,
            "output_fps": output_fps,
            "processed_duration": frames_read / source_fps,
            "truncated": truncated,
            "mime_type": writer_info["mime_type"],
            "file_extension": writer_info["file_extension"],
            "encoder": writer_info["encoder"],
            "playback_warning": writer_info["playback_warning"],
        }


def show_image_results(media_bytes, source_name, detector, model_label):
    image = PILImage.open(BytesIO(media_bytes)).convert("RGB")
    image_np = np.array(image)

    results, elapsed = run_detection(image_np, detector)
    detections = extract_detections(results, image.size)
    result_image = draw_detections(image, detections)
    result_buffer = BytesIO()
    result_image.save(result_buffer, format="PNG", optimize=True)

    metric_cols = st.columns(2)
    metric_cols[0].metric("Faces Detected", len(detections))
    metric_cols[1].metric("Detection Time", f"{elapsed:.4f} s")
    st.caption(f"Detector: {model_label}")

    left_col, right_col = st.columns(2)
    left_col.subheader("Original Image")
    left_col.image(image, use_container_width=True)

    right_col.subheader("Detected Faces")
    right_col.image(result_image, use_container_width=True)
    right_col.download_button(
        "Download Detected Image",
        data=result_buffer.getvalue(),
        file_name=(
            f"{safe_download_stem(source_name)}_face_detection.png"
        ),
        mime="image/png",
        use_container_width=True,
    )


def show_video_results(
    media_bytes,
    source_name,
    source_suffix,
    confidence_threshold,
    model_label,
    model_path,
):
    st.subheader("Original Video")
    st.video(
        media_bytes,
        format=VIDEO_MIME_TYPES.get(source_suffix, "video/mp4"),
    )

    st.sidebar.subheader("Video Processing")
    target_fps = st.sidebar.slider(
        "Frames analyzed per second",
        min_value=1,
        max_value=10,
        value=5,
        help="Lower values process faster. The output keeps only analyzed frames.",
    )
    max_duration_seconds = st.sidebar.slider(
        "Maximum duration to process",
        min_value=5,
        max_value=60,
        value=30,
        step=5,
        format="%d seconds",
    )

    request_key = (
        hashlib.sha256(media_bytes).hexdigest(),
        "portable-video-v2",
        model_path.name,
        model_path.stat().st_mtime_ns,
        confidence_threshold,
        target_fps,
        max_duration_seconds,
    )

    if st.button("Process Video", type="primary"):
        progress_bar = st.progress(0.0, text="Preparing video...")

        def update_progress(value):
            progress_bar.progress(value, text=f"Processing video: {value:.0%}")

        try:
            detector = load_mp_detector(str(model_path), confidence_threshold)
            result = process_video(
                media_bytes,
                source_suffix,
                detector,
                target_fps,
                max_duration_seconds,
                update_progress,
            )
        except Exception as error:
            progress_bar.empty()
            st.error(f"Video processing failed: {error}")
        else:
            progress_bar.progress(1.0, text="Video processing complete.")
            st.session_state["video_result_key"] = request_key
            st.session_state["video_result"] = result

    if st.session_state.get("video_result_key") != request_key:
        st.info("Choose the video settings, then select **Process Video**.")
        return

    result = st.session_state["video_result"]
    st.subheader("Detected Faces")
    st.video(result["video_bytes"], format=result["mime_type"])

    metric_cols = st.columns(4)
    metric_cols[0].metric("Frames Analyzed", result["frames_analyzed"])
    metric_cols[1].metric("Max Faces / Frame", result["max_faces"])
    metric_cols[2].metric(
        "Average Faces / Frame",
        f"{result['average_faces']:.2f}",
    )
    metric_cols[3].metric(
        "Processing Time",
        f"{result['processing_time']:.2f} s",
    )

    st.caption(
        f"Analyzed at approximately {result['output_fps']:.2f} FPS for "
        f"{result['processed_duration']:.1f} seconds. The processed video "
        f"does not include the original audio. Detector: {model_label}. "
        f"Encoder: {result['encoder']}."
    )
    if result["playback_warning"]:
        st.warning(result["playback_warning"])
    if result["truncated"]:
        st.warning(
            "Only the configured maximum duration was processed. Increase the "
            "duration limit to process more of the video."
        )

    download_name = (
        f"{safe_download_stem(source_name)}_face_detection"
        f"{result['file_extension']}"
    )
    st.download_button(
        "Download Processed Video",
        data=result["video_bytes"],
        file_name=download_name,
        mime=result["mime_type"],
    )


def main():
    st.set_page_config(page_title=APP_TITLE, layout="wide")
    st.title(APP_TITLE)
    st.subheader("🔗 Please see the documentation located in the GitHub Repository")
    st.markdown(GITHUB_REPO_1)
    st.subheader("🔗 Check out my portfolio!")
    st.markdown(GITHUB_REPO_2)

    available_models = {
        label: details
        for label, details in DETECTOR_MODELS.items()
        if details["path"].exists()
    }
    missing_models = [
        details["path"].name
        for details in DETECTOR_MODELS.values()
        if not details["path"].exists()
    ]

    if not available_models:
        st.error("No compatible BlazeFace detector models were found.")
        st.stop()

    if missing_models:
        st.sidebar.warning(
            "Missing detector models: " + ", ".join(missing_models)
        )

    selected_model_label = st.sidebar.selectbox(
        "Detector Model",
        tuple(available_models),
        help="Choose a close-range or full-range BlazeFace detector.",
    )
    selected_model = available_models[selected_model_label]
    selected_model_path = selected_model["path"]
    st.sidebar.caption(selected_model["description"])

    confidence_threshold = st.sidebar.slider(
        "Minimum Detection Confidence",
        min_value=0.1,
        max_value=0.95,
        value=0.3,
        step=0.05,
    )

    uploaded_file = st.file_uploader(
        "Upload an image or video...",
        type=["jpg", "jpeg", "png", "webp", "mp4", "webm", "mov", "avi", "mkv"],
    )
    sample_label = st.selectbox(
        "Or select from the sample collection:",
        tuple(SAMPLE_MEDIA),
    )
    sample_path = SAMPLE_MEDIA[sample_label]

    if uploaded_file is not None:
        media_bytes = uploaded_file.getvalue()
        source_name = uploaded_file.name
        if sample_path is not None:
            st.caption("The uploaded file takes precedence over the sample selection.")
    elif sample_path is not None:
        if not sample_path.exists():
            st.error(f"Sample file not found: {sample_path.name}")
            st.stop()
        media_bytes = sample_path.read_bytes()
        source_name = sample_path.name
    else:
        st.info("Please upload an image or video, or choose a sample.")
        st.stop()

    source_suffix = Path(source_name).suffix.lower()
    media_kind = get_media_kind(source_name)

    if media_kind == "image":
        try:
            detector = load_mp_detector(
                str(selected_model_path),
                confidence_threshold,
            )
            show_image_results(
                media_bytes,
                source_name,
                detector,
                selected_model_label,
            )
        except Exception as error:
            st.error(f"Image processing failed: {error}")
    elif media_kind == "video":
        show_video_results(
            media_bytes,
            source_name,
            source_suffix,
            confidence_threshold,
            selected_model_label,
            selected_model_path,
        )
    else:
        st.error("Unsupported file type.")


if __name__ == "__main__":
    main()
