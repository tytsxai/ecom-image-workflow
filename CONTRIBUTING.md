# Contributing

Thanks for taking the time to contribute.

## Development setup

- Python: 3.10+
- From the repo root, run tests with:

```bash
python3 -m unittest discover -s tests -p "test*.py" -v
```

## What to contribute

- Improvements to the Phase 1 image workflow docs.
- Improvements to the MVP packager (`mvp_image_workflow/`) and its tests.

## Style and constraints

- Keep changes minimal and focused.
- For docs that contain YAML front matter, update the `updated:` date when editing.
- Prefer reusing existing patterns in the codebase.

## Pull requests

- Describe *why* the change is needed and how to verify it.
- Ensure CI is green.
