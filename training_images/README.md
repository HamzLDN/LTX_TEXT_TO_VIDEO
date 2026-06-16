# Training Images

Place your character training images here. Each image must have a matching `.txt` caption file with the same filename stem containing your trigger word.

## Example

```
training_images/
  ├── char_front.png
  ├── char_front.txt       ← "yourcharacter man, facing forward, dark hair"
  ├── char_side.png
  ├── char_side.txt        ← "yourcharacter man, side profile, wearing jacket"
  └── ...
```

## Trigger word

Set your trigger word as the **TRIGGER_WORD** secret in GitHub repository settings.
Settings → Secrets and variables → Actions → New repository secret

