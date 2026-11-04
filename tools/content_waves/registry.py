"""Registered content waves, in build order.

Each module provides KEY, NAME, WAVE, owner(), LEDGER, SOURCES, NEWS_ART,
OWNER_ART and either IMPORTS (tag -> import-block name for an existing tree)
or TREES (tag -> new tree ID). An owner-only module (no branches) instead
declares COUNTRIES (tag -> name, for category art) and may add EVENT_ART for
its own country events.
"""
from content_waves import aurelia, circum_pacific, estovakia, free_erusea, lighthouse, nordennavic

MODULES = (free_erusea, nordennavic, estovakia, aurelia, circum_pacific, lighthouse)
