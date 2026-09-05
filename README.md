# Godot Folder Structuring

A Python utility that analyzes files in a Godot project and generates a suggested folder structure as JSON.

## What it does

- Classifies files into categories such as Code, Scene, Asset, and Data.
- Applies keyword-based grouping (for example: UI, Manager, Resource, Level).
- Supports nested asset subcategories (Image, SFX, Font, SVG).
- Excludes common Godot/project metadata files based on config rules.
- Writes output JSON files under `FolderStructuringJson/`.

## Requirements

- Python 3.12+
- pip

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run from the repository root.

### Organize only top-level files

```bash
python organize_project.py --path /absolute/path/to/godot/project --daily
```

### Organize all files recursively

```bash
python organize_project.py --path /absolute/path/to/godot/project --daily-all
```

If `--path` is omitted, the current working directory is used.

## Output

Each run generates:

- `FolderStructuringJson/<date>_categorized_files.json`
- `FolderStructuringJson/<date>_files_to_path.json`

## Configuration

Default rules are in:

- `Configuration/default_config.json`

You can adjust:

- category patterns (`code`, `scene`, `asset`, `data`)
- keyword folders (`keywords.default`)
- excluded files/patterns (`exclude.default`)

## Notes

- This project currently generates organization suggestions as JSON output.
- It does not move files automatically.
