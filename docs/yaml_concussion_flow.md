
# YAML Schema for Concussion Protocol Flow

This file defines the structure used by the Concussion Agent to drive its question flow.

## Root Structure

```yaml
stages:
  - name: "Stage Name"
    description: "Optional human-readable explanation"
    questions: [ ... ]
```

## Question Fields

Each question object contains:

| Field       | Type     | Description |
|-------------|----------|-------------|
| `id`        | string   | Unique key used in JSON output |
| `prompt`    | string   | Text shown to the user |
| `type`      | string   | One of: `text`, `date`, `boolean`, `list` |
| `parse_with`| string?  | Optional function name to use for custom parsing |

Example:

```yaml
- id: symptoms
  prompt: "What symptoms did the player experience?"
  type: list
  parse_with: symptom_extractor
```

## Future Enhancements

- Add `follow_ups` or `conditional_on` logic
- Add `stage_guidance` metadata for return-to-play triggers
