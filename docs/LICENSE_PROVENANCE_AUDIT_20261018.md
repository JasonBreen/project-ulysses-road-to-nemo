# License and provenance audit — 2026-10-18

This is a read-only audit of the current private continuation checkout. It does not grant rights, relicense inherited content, or authorize public distribution.

## Findings

- No root `LICENSE`, `NOTICE`, `COPYING`, or `CREDITS` file was present in this checkout.
- `docs/licenses/MD-CC-BY-SA-4.0.txt` and `docs/ECONOMY_PROVENANCE.md` scope CC BY-SA 4.0 to the newly authored Millennium Dawn-inspired economy adaptation and its supporting documentation/tooling only.
- That scoped notice explicitly does not relicense inherited Project Ulysses files, ACE COMBAT/Strangereal names or art, third-party assets, or Paradox material.
- `inventory/SOURCE_EVIDENCE.md` records the April 5, 2024 archive and its SHA-256, but it does not establish a license grant from the original Project Ulysses team.
- `README.md` credits the original Project Ulysses team and states that ACE COMBAT/Strangereal are properties of Bandai Namco Entertainment and Project Aces; it also describes this work as private, unofficial, and fan-made.
- Repository references to official Project Aces/ACE COMBAT sources are lore provenance, not asset licenses or endorsement.

## Working rule

Keep inherited archive content, Project Aces/Bandai Namco material, Paradox/HOI4 engine dependencies, third-party assets, and the scoped economy adaptation as separate provenance layers. Do not add a broad repository license or imply that the MD license covers the archive or game assets without a verified rights decision.

## Open blocker

The inherited archive’s redistribution permissions and the provenance/permissions for all non-code art, audio, portraits, and extracted game-facing assets remain unverified. Preserve credits and private visibility; do not publish a release package or claim permission based only on repository presence.
