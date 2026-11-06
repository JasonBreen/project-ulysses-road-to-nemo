"""Explicit frontend owner import without ambiguous build.py module names."""
import importlib.util
from pathlib import Path

path = Path(__file__).resolve().parents[1] / 'frontend_briefing/responsive.py'
spec = importlib.util.spec_from_file_location('ulysses_responsive_frontend', path)
responsive = importlib.util.module_from_spec(spec)
spec.loader.exec_module(responsive)
