# Reproducibility and evaluation

This repository contains the RF-DETR training and inference code, but the
training dataset and trained checkpoint are not included. The recorded metrics
must therefore be treated as historical project notes until they are regenerated
from the required assets.

## Required assets

1. A licensed COCO-format dataset at `synthetic-shoe-dataset/` with a `train/`
   split and optional `valid/` and `test/` splits.
2. `_annotations.coco.json` in each provided split.
3. Exactly the English category labels `Slipper` and `Sneaker`.
4. A compatible RF-DETR checkpoint for `scripts/infer.py` after training.

The notebook validates image references, category references, positive bounding
boxes, and image bounds before training. It enables early stopping unless
`no_early_stopping` is explicitly set to `True` for an intentional experiment.

## Re-run

From the project root, install the pinned dependencies, open
`notebooks/train-rfdetr.ipynb`, and run all cells. Then run inference with a
checkpoint produced by that training run:

```bash
python scripts/infer.py --checkpoint path/to/checkpoint.pth --image path/to/image.jpg
```

Report the dataset version, split sizes, training configuration, checkpoint
path, and fresh validation metrics. Do not publish a new accuracy or mAP value
unless it was produced by that run.
