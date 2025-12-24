"""
System-wide configuration.

This file is intentionally minimal.
It serves as a central location for:
- Feature flags
- Agent enable/disable switches
- Environment-specific defaults

Currently, configuration is handled directly
inside the orchestrator for simplicity.
"""

USE_LLM = True
DEFAULT_CURRENCY = "INR"
