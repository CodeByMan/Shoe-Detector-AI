import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {".json", ".md", ".py", ".txt", ".yml", ".yaml", ".ipynb"}


class RepositoryContractTests(unittest.TestCase):
    def test_required_project_files_exist(self):
        required = (
            "README.md",
            "LICENSE",
            "requirements.txt",
            "config.sample.json",
            "docker-compose.yml",
            ".env.example",
            "scripts/extract_frames.py",
            "scripts/infer.py",
            "notebooks/train-rfdetr.ipynb",
            "docs/REPRODUCIBILITY.md",
        )
        for relative_path in required:
            self.assertTrue((ROOT / relative_path).is_file(), relative_path)

    def test_config_uses_english_model_labels(self):
        config = json.loads((ROOT / "config.sample.json").read_text())
        self.assertEqual(config["categories"]["1"], "Slipper")
        self.assertEqual(config["categories"]["2"], "Sneaker")

    def test_public_text_has_no_legacy_owner_or_language_markers(self):
        forbidden = (
            "Stepan Svarc",
            "Štěpán Švarc",
            "Pantofle",
            "Teniska",
            "moje-prostredi",
            "zaverecna-zprava",
        )
        for path in ROOT.rglob("*"):
            if (
                path.is_file()
                and path != Path(__file__)
                and path.suffix.lower() in TEXT_SUFFIXES
            ):
                content = path.read_text(encoding="utf-8")
                for marker in forbidden:
                    self.assertNotIn(marker, content, str(path))

    def test_python_sources_compile(self):
        result = subprocess.run(
            [sys.executable, "-m", "compileall", "-q", "scripts"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_inference_validates_missing_checkpoint_before_importing_model(self):
        sys.path.insert(0, str(ROOT))
        from scripts.infer import run_inference

        with self.assertRaises(FileNotFoundError):
            run_inference(ROOT / "missing.pth", ROOT / "missing.jpg")

    def test_compose_is_local_and_requires_explicit_images(self):
        compose = (ROOT / "docker-compose.yml").read_text()
        self.assertNotIn(":latest", compose)
        self.assertIn("127.0.0.1:8000:8000", compose)
        self.assertIn("127.0.0.1:3000:3000", compose)
        self.assertIn("RFDETR_BACKEND_IMAGE", compose)
        self.assertIn("RFDETR_FRONTEND_IMAGE", compose)

    def test_training_notebook_validates_annotations_and_enables_early_stopping(self):
        notebook = json.loads((ROOT / "notebooks/train-rfdetr.ipynb").read_text())
        source = "\n".join(
            line
            for cell in notebook["cells"]
            if cell["cell_type"] == "code"
            for line in cell["source"]
        )
        self.assertIn("_validate_coco_split", source)
        self.assertIn("x + width > image_width", source)
        self.assertIn('"early_stopping": not no_early_stopping', source)

    def test_direct_dependencies_are_version_pinned(self):
        requirements = [
            line.strip()
            for line in (ROOT / "requirements.txt").read_text().splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        ]
        self.assertTrue(requirements)
        self.assertTrue(all("==" in requirement for requirement in requirements))


if __name__ == "__main__":
    unittest.main()
