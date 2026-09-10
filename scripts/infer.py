"""Run RF-DETR inference on one local image."""

from __future__ import annotations

import argparse
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run RF-DETR Medium inference on a local image."
    )
    parser.add_argument(
        "--checkpoint",
        type=Path,
        required=True,
        help="Path to a trained RF-DETR checkpoint.",
    )
    parser.add_argument(
        "--image",
        type=Path,
        required=True,
        help="Path to the image to analyze.",
    )
    return parser.parse_args()


def run_inference(checkpoint: Path, image: Path) -> object:
    if not checkpoint.is_file():
        raise FileNotFoundError(f"Checkpoint not found: {checkpoint}")
    if not image.is_file():
        raise FileNotFoundError(f"Image not found: {image}")

    from rfdetr import RFDETRMedium

    model = RFDETRMedium.from_checkpoint(str(checkpoint))
    return model.predict(str(image))


def main() -> None:
    args = parse_args()
    print(run_inference(args.checkpoint, args.image))


if __name__ == "__main__":
    main()
