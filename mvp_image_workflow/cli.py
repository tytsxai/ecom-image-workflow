from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .generator import generate_product_package
from .io_csv import read_products_csv
from .util import ValidationError, safe_id
from .validator import validate_product_package


def _cmd_generate(args: argparse.Namespace) -> int:
    products = read_products_csv(args.input)
    out_root = Path(args.out)
    out_root.mkdir(parents=True, exist_ok=True)

    created: list[Path] = []
    for p in products:
        created.append(generate_product_package(p, out_root, batch_id=args.batch_id))

    print(f"Generated {len(created)} product package(s) in {out_root}")
    return 0


def _cmd_validate(args: argparse.Namespace) -> int:
    out_root = Path(args.out)
    if not out_root.exists():
        raise ValidationError(f"Output root not found: {out_root}")

    if args.product_id:
        product_dir = out_root / safe_id(args.product_id)
        validate_product_package(product_dir, require_images=args.require_images)
        print(f"OK: {product_dir}")
        return 0

    # Validate all product folders that have a manifest.json.
    manifests = list(out_root.glob("*/manifest.json"))
    if not manifests:
        raise ValidationError(f"No product manifests found under: {out_root}")

    for m in manifests:
        validate_product_package(m.parent, require_images=args.require_images)
    print(f"OK: validated {len(manifests)} product package(s) under {out_root}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="mvp_image_workflow")
    sub = parser.add_subparsers(dest="cmd", required=True)

    g = sub.add_parser("generate", help="Generate per-product prompt/text packages")
    g.add_argument("--input", required=True, help="CSV file (utf-8) with product rows")
    g.add_argument("--out", required=True, help="Output root folder")
    g.add_argument(
        "--batch-id",
        default=None,
        help="Optional batch id appended to expected image filenames (e.g. 2025-12-26A)",
    )
    g.set_defaults(func=_cmd_generate)

    v = sub.add_parser("validate", help="Validate generated packages")
    v.add_argument("--out", required=True, help="Output root folder")
    v.add_argument("--product-id", default=None, help="Validate a single product id")
    v.add_argument(
        "--require-images",
        action="store_true",
        help="Also require expected .png images to exist",
    )
    v.set_defaults(func=_cmd_validate)

    return parser


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except ValidationError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
