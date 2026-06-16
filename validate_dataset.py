#!/usr/bin/env python3
"""
validate_dataset.py
-------------------
Validates that every image in the training dataset folder has:
  1. A matching .txt caption file with the same stem name
  2. The trigger word present in that caption file

Usage:
  python validate_dataset.py --folder training_images --trigger yourcharacter

Exit codes:
  0 = all images valid
  1 = one or more validation errors found
"""

import os
import sys
import argparse
from pathlib import Path

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}


def validate(folder: Path, trigger: str) -> bool:
    if not folder.exists():
        print(f"ERROR: Folder '{folder}' does not exist.")
        print(f"  Create it and add your training images there.")
        return False

    images = [f for f in folder.iterdir() if f.suffix.lower() in IMAGE_EXTENSIONS]

    if not images:
        print(f"WARNING: No images found in '{folder}'.")
        print(f"  Supported formats: {', '.join(IMAGE_EXTENSIONS)}")
        # Not a hard failure — dataset may not be added yet
        return True

    errors = []
    warnings = []
    passed = []

    for img in sorted(images):
        caption_path = img.with_suffix(".txt")

        # Check 1: caption file exists
        if not caption_path.exists():
            errors.append(
                f"  MISSING CAPTION: '{img.name}' has no matching '{caption_path.name}'"
            )
            continue

        # Check 2: caption is not empty
        caption_text = caption_path.read_text(encoding="utf-8").strip()
        if not caption_text:
            errors.append(
                f"  EMPTY CAPTION: '{caption_path.name}' exists but contains no text"
            )
            continue

        # Check 3: trigger word present (case-insensitive)
        if trigger.lower() not in caption_text.lower():
            errors.append(
                f"  MISSING TRIGGER: '{caption_path.name}' does not contain "
                f"trigger word '{trigger}'"
                f"\n    Caption: {caption_text[:120]}"
            )
            continue

        # Check 4: warn if caption is suspiciously short
        if len(caption_text.split()) < 3:
            warnings.append(
                f"  SHORT CAPTION: '{caption_path.name}' has fewer than 3 words "
                f"— consider adding more descriptive text"
            )

        passed.append(img.name)

    # ── Report ────────────────────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print(f"Dataset Validation Report")
    print(f"Folder:      {folder.resolve()}")
    print(f"Trigger:     '{trigger}'")
    print(f"Images:      {len(images)}")
    print(f"{'='*60}")

    if passed:
        print(f"\n✓ PASSED ({len(passed)}/{len(images)}):")
        for name in passed:
            print(f"  ✓ {name}")

    if warnings:
        print(f"\n⚠ WARNINGS ({len(warnings)}):")
        for w in warnings:
            print(w)

    if errors:
        print(f"\n✗ ERRORS ({len(errors)}):")
        for e in errors:
            print(e)
        print(f"\n{'='*60}")
        print(f"RESULT: FAILED — fix the {len(errors)} error(s) above before training.")
        print(f"{'='*60}\n")
        return False

    print(f"\n{'='*60}")
    print(f"RESULT: ALL {len(passed)} IMAGE(S) VALID — dataset is ready for training.")
    print(f"{'='*60}\n")
    return True


def main():
    parser = argparse.ArgumentParser(description="Validate LoRA training dataset captions")
    parser.add_argument(
        "--folder",
        type=Path,
        default=Path("training_images"),
        help="Path to folder containing images and caption .txt files (default: training_images)"
    )
    parser.add_argument(
        "--trigger",
        type=str,
        required=True,
        help="Trigger word that must appear in every caption file"
    )
    args = parser.parse_args()

    ok = validate(args.folder, args.trigger)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
