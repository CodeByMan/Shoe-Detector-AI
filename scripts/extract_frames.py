"""Extract periodic JPEG frames from local video files."""

from __future__ import annotations

import argparse
from pathlib import Path

import cv2


VIDEO_SUFFIXES = {".mov", ".mp4", ".avi", ".mkv"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract periodic JPEG frames from local videos."
    )
    parser.add_argument(
        "--input-dir",
        type=Path,
        required=True,
        help="Directory containing source video files.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="Directory where extracted JPEG frames will be written.",
    )
    parser.add_argument(
        "--every-n-frames",
        type=int,
        default=30,
        help="Write one frame for every N input frames (default: 30).",
    )
    parser.add_argument(
        "--jpeg-quality",
        type=int,
        default=95,
        help="JPEG quality from 0 to 100 (default: 95).",
    )
    return parser.parse_args()


def extract_frames(
    input_dir: Path,
    output_dir: Path,
    every_n_frames: int = 30,
    jpeg_quality: int = 95,
) -> int:
    if not input_dir.is_dir():
        raise FileNotFoundError(f"Input directory not found: {input_dir}")
    if every_n_frames < 1:
        raise ValueError("every_n_frames must be at least 1")
    if not 0 <= jpeg_quality <= 100:
        raise ValueError("jpeg_quality must be between 0 and 100")

    videos = sorted(
        path
        for path in input_dir.iterdir()
        if path.is_file() and path.suffix.lower() in VIDEO_SUFFIXES
    )
    if not videos:
        print("No supported video files found.")
        return 0

    output_dir.mkdir(parents=True, exist_ok=True)
    written = 0
    failures: list[str] = []
    write_options = [cv2.IMWRITE_JPEG_QUALITY, jpeg_quality]

    for video_path in videos:
        capture = cv2.VideoCapture(str(video_path))
        if not capture.isOpened():
            failures.append(f"Could not open video: {video_path}")
            continue

        frame_index = 0
        try:
            while True:
                success, frame = capture.read()
                if not success:
                    break
                if frame_index % every_n_frames == 0:
                    frame_path = output_dir / (
                        f"{video_path.stem}_frame_{frame_index:06d}.jpg"
                    )
                    if not cv2.imwrite(str(frame_path), frame, write_options):
                        failures.append(f"Could not write frame: {frame_path}")
                    else:
                        written += 1
                frame_index += 1
        finally:
            capture.release()

    if failures:
        raise RuntimeError("; ".join(failures))

    print(f"Extracted {written} frames from {len(videos)} video files.")
    return written


def main() -> None:
    args = parse_args()
    extract_frames(
        input_dir=args.input_dir,
        output_dir=args.output_dir,
        every_n_frames=args.every_n_frames,
        jpeg_quality=args.jpeg_quality,
    )


if __name__ == "__main__":
    main()
