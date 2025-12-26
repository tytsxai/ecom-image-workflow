from __future__ import annotations

import json
from pathlib import Path

from .util import ValidationError


def _read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise ValidationError(f"Missing required file: {path}") from None
    except json.JSONDecodeError as e:
        raise ValidationError(f"Invalid JSON in {path}: {e}") from None


def validate_product_package(product_dir: str | Path, require_images: bool) -> None:
    root = Path(product_dir)
    manifest_path = root / "manifest.json"
    manifest = _read_json(manifest_path)

    prompts_dir = root / "prompts"
    texts_dir = root / "texts"
    meta_dir = root / "meta"

    required_files = [
        manifest_path,
        prompts_dir / "showcase_01_clean_main.txt",
        prompts_dir / "showcase_02_lifestyle_A.txt",
        prompts_dir / "showcase_03_lifestyle_B.txt",
        prompts_dir / "spec_01_dimensions_background.txt",
        prompts_dir / "spec_02_specs_background.txt",
        prompts_dir / "howto_01_steps_background.txt",
        prompts_dir / "howto_02_tips_background.txt",
        texts_dir / "spec_01.txt",
        texts_dir / "spec_02.txt",
        texts_dir / "howto_01.txt",
        texts_dir / "howto_02.txt",
        meta_dir / "qc_checklist.json",
        meta_dir / "product.json",
    ]

    missing = [str(p) for p in required_files if not p.exists()]
    if missing:
        raise ValidationError("Missing required files:\n- " + "\n- ".join(missing))

    if not require_images:
        return

    expected_outputs = manifest.get("expected_outputs")
    if not isinstance(expected_outputs, dict):
        raise ValidationError("manifest.json missing 'expected_outputs' dict")

    for category in ("showcase", "spec", "howto"):
        files = expected_outputs.get(category)
        if not isinstance(files, list):
            raise ValidationError(f"manifest.json expected_outputs.{category} must be a list")

        category_dir = root / category
        for fname in files:
            if not isinstance(fname, str):
                raise ValidationError(f"manifest.json expected_outputs.{category} contains non-string")
            if not (category_dir / fname).exists():
                raise ValidationError(f"Missing expected image: {category_dir / fname}")
