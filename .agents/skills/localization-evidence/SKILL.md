---
name: localization-evidence
description: Add and audit Project Ulysses localization with stable keys, correct encoding, provenance-aware wording, and static reference coverage.
---

# Localization and evidence

Use this skill whenever events, focuses, decisions, ideas, characters, equipment, or country names gain new text.

- Follow the existing `l_english:` YAML style and preserve UTF-8 BOM on `country_BLK_continuation_l_english.yml`.
- Add every new title, description, option, focus, decision, idea, and tooltip key in the same change as its definition.
- Use neutral language for provisional gameplay branches; do not turn archive flavor text or an unresolved claim into official canon.
- Search for missing keys before validation and avoid changing unrelated localization.

Acceptance:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\Test-UlyssesStatic.ps1 -ModRoot (Join-Path $PWD 'mod\2985041246')
```

The result must include no new missing references and the Belkan continuation file must retain its BOM.
