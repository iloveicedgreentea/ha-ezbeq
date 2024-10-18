"""Tests for the ezbeq integration setup."""

from unittest.mock import AsyncMock

import pytest

from custom_components.ezbeq.const import DOMAIN
from homeassistant.config_entries import ConfigEntryState
from homeassistant.core import HomeAssistant

from .conftest import setup_integration

from pytest_homeassistant_custom_component.common import MockConfigEntry

pytestmark = pytest.mark.asyncio
