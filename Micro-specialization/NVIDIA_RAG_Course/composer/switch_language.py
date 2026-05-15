#!/usr/bin/env python3
"""
switch_language.py (v3) — Switch all course notebooks to a target language.

Works with translation_web.json v4 format:
- Each cell has a role (header/footer/button/code/content)
- Shared cells (code/button) are language-independent
- Translated cells have per-language content dicts
- Language extras are inserted only for the target language

Usage:
    python3 switch_language.py en     # Switch to English
    python3 switch_language.py tw     # Switch to Traditional Chinese
    python3 switch_language.py zh     # Switch to Simplified Chinese
    python3 switch_language.py ja     # Switch to Japanese
"""

import json, os, sys
from pathlib import Path

LANGUAGES = ["en", "tw", "zh", "ja"]


def switch_language(lang, nb_dir=".", web_path="composer/translation_web.json"):
    """Switch all notebooks to the specified language."""
    if lang not in LANGUAGES:
        print(f"Error: unknown language '{lang}'. Choose from: {', '.join(LANGUAGES)}")
        return False
    
    if nb_dir is None:
        nb_dir = str(Path(__file__).parent)
    nb_dir = Path(nb_dir)

    web_path = Path(web_path)
    if not web_path.exists():
        print(f"Error: {web_path} not found")
        return False
    
    with open(web_path) as f:
        web = json.load(f)
    
    lang_name = web.get("lang_names", {}).get(lang, lang)
    print(f"Switching to {lang_name} ({lang})...")
    
    changed = 0
    for nb_name, entry in web["notebooks"].items():
        nb_path = nb_dir / nb_name
        if not nb_path.exists():
            # Check solutions
            sol_path = nb_dir / nb_name
            if not sol_path.exists():
                continue
        
        # Load the notebook
        with open(nb_path) as f:
            nb = json.load(f)
        
        # Build the cell list for this language
        cells = []
        cell_defs = entry["cells"]
        extras = entry.get("lang_extras", {}).get(lang, [])
        
        # Index extras by "after_cell"
        extras_by_pos = {}
        for ex in extras:
            pos = ex["after_cell"]
            extras_by_pos.setdefault(pos, []).append(ex)
        
        # Insert any extras that go before all cells (after_cell = -1)
        for ex in extras_by_pos.get(-1, []):
            cells.append(_make_cell(ex["cell_type"], ex["content"], nb))
        
        for i, cell_def in enumerate(cell_defs):
            # Create the cell
            cell = _make_cell_from_def(cell_def, lang, nb, i)
            cells.append(cell)
            
            # Insert any extras after this cell
            for ex in extras_by_pos.get(i, []):
                cells.append(_make_cell(ex["cell_type"], ex["content"], nb))
        
        # Preserve notebook metadata
        nb["cells"] = cells
        
        with open(nb_path, "w") as f:
            json.dump(nb, f, ensure_ascii=False, indent=1)
        
        changed += 1
    
    print(f"Done! Switched {changed} notebooks to {lang_name}.")
    return True


def _make_cell_from_def(cell_def, lang, nb, index):
    """Create a notebook cell from a web cell definition."""
    content = cell_def["content"]
    
    if isinstance(content, dict):
        # Per-language content — pick the right one, fallback to en
        text = content.get(lang, content.get("en", ""))
    else:
        # Shared content (code, button)
        text = content
    
    return _make_cell(cell_def["cell_type"], text, nb)


def _make_cell(cell_type, text, nb):
    """Create a raw notebook cell."""
    if cell_type == "code":
        cell = {
            "cell_type": "code",
            "metadata": {},
            "source": _text_to_source(text),
            "execution_count": None,
            "outputs": [],
        }
    else:
        cell = {
            "cell_type": "markdown",
            "metadata": {},
            "source": _text_to_source(text),
        }
    return cell


def _text_to_source(text):
    """Convert text string to notebook source format (list of lines)."""
    if "\n" not in text:
        return [text] if text else [""]
    
    lines = text.split("\n")
    result = []
    for i, line in enumerate(lines):
        if i < len(lines) - 1:
            result.append(line + "\n")
        else:
            result.append(line)
    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: switch_language.py <en|tw|zh|ja>")
        sys.exit(1)
    
    lang = sys.argv[1].lower().strip()
    ok = switch_language(lang)
    sys.exit(0 if ok else 1)