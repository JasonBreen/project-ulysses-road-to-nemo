# AI path auditor

Audit the AI-facing campaign path without launching HOI4. Confirm that the AI
has a bounded fallback for each war stage, that repeat events are prevented by
country flags, and that the weekly hook is limited to the Belkan campaign
contract. Use `tools/analysis/campaign_path_report.py` and the native checklist
to identify what still needs real-save verification.
