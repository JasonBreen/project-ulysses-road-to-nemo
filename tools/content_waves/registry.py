"""Registered content waves, in build order.

Each module provides KEY, NAME, WAVE, owner(), LEDGER, SOURCES, NEWS_ART,
OWNER_ART and either IMPORTS (tag -> import-block name for an existing tree)
or TREES (tag -> new tree ID).
"""
from content_waves import aurelia, estovakia, free_erusea, nordennavic

MODULES = (free_erusea, nordennavic, estovakia, aurelia)
