from __future__ import annotations

import csv
import tempfile
import unittest
from pathlib import Path

from mvp_image_workflow.generator import generate_product_package
from mvp_image_workflow.io_csv import read_products_csv
from mvp_image_workflow.validator import validate_product_package
from mvp_image_workflow.util import ValidationError


class TestMvpImageWorkflow(unittest.TestCase):
    def test_generate_and_validate_minimum(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            csv_path = root / "in.csv"

            with csv_path.open("w", encoding="utf-8", newline="") as f:
                w = csv.writer(f)
                w.writerow(
                    [
                        "product_id",
                        "product_name_en",
                        "style_pack",
                        "output_set",
                        "units",
                        "dimensions_l",
                        "dimensions_w",
                        "dimensions_h",
                        "spec_1",
                        "spec_2",
                        "spec_3",
                        "howto_title",
                        "step_1",
                        "step_2",
                        "step_3",
                    ]
                )
                w.writerow(
                    [
                        "SKU123",
                        "Stainless Steel Insulated Tumbler",
                        "minimal_white",
                        "minimum",
                        "cm",
                        "20",
                        "8",
                        "8",
                        "Capacity: 500 ml",
                        "Double-wall insulation",
                        "Leak-proof lid",
                        "How to Use",
                        "Fill with your drink",
                        "Close the lid firmly",
                        "Enjoy hot or cold beverages",
                    ]
                )

            products = read_products_csv(csv_path)
            self.assertEqual(len(products), 1)
            product_dir = generate_product_package(products[0], root / "out", batch_id="B1")

            validate_product_package(product_dir, require_images=False)

            # Require images: should fail until we create empty placeholders.
            with self.assertRaises(ValidationError):
                validate_product_package(product_dir, require_images=True)

            manifest = (product_dir / "manifest.json").read_text(encoding="utf-8")
            self.assertIn("expected_outputs", manifest)

            import json

            expected = json.loads(manifest)["expected_outputs"]
            for category, files in expected.items():
                for fname in files:
                    (product_dir / category / fname).write_bytes(b"")

            validate_product_package(product_dir, require_images=True)


if __name__ == "__main__":
    unittest.main()
