"""Tests for the ezbeq Profile Loader services."""

from unittest.mock import AsyncMock, patch

import pytest
from pyezbeq.models import SearchRequest

from custom_components.ezbeq.const import DOMAIN
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError

from .conftest import setup_integration

from pytest_homeassistant_custom_component.common import MockConfigEntry

pytestmark = pytest.mark.asyncio


async def test_load_beq_profile_service(
    hass: HomeAssistant,
    mock_ezbeq_client: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test the load_beq_profile service."""
    await setup_integration(hass, mock_config_entry)

    # Ensure the service was registered
    assert hass.services.has_service(DOMAIN, "load_beq_profile")

    # Set up mock sensors
    hass.states.async_set("sensor.tmdb_id", "123456")
    hass.states.async_set("sensor.year", "2023")
    hass.states.async_set("sensor.codec", "Atmos")
    hass.states.async_set("sensor.edition", "Director's Cut")
    hass.states.async_set("sensor.mv_adjust", "0.5")
    hass.states.async_set("sensor.media_type", "Movie")
    hass.states.async_set("sensor.title", "Test Movie Title")

    # Mock the load_beq_profile method of the client
    mock_ezbeq_client.load_beq_profile = AsyncMock()

    # Call the service
    await hass.services.async_call(
        DOMAIN,
        "load_beq_profile",
        {
            "tmdb_sensor": "sensor.tmdb_id",
            "year_sensor": "sensor.year",
            "codec_sensor": "sensor.codec",
            "preferred_author": "test_author",
            "edition_sensor": "sensor.edition",
            "mv_adjust_sensor": "sensor.mv_adjust",
            "media_type_sensor": "sensor.media_type",
            "title_sensor": "sensor.title",
            "slots": [1],
            "dry_run_mode": False,
            "skip_search": False,
        },
        blocking=True,
    )

    # Check if the load_beq_profile method was called with the correct arguments
    mock_ezbeq_client.load_beq_profile.assert_called_once()
    call_args = mock_ezbeq_client.load_beq_profile.call_args[0][0]
    assert isinstance(call_args, SearchRequest)
    assert call_args.tmdb == "123456"
    assert call_args.year == 2023
    assert call_args.codec == "Atmos"
    assert call_args.preferred_author == "test_author"
    assert call_args.edition == "Director's Cut"
    assert call_args.mvAdjust == 0.5
    assert call_args.dry_run_mode == False
    assert call_args.media_type == "Movie"
    assert call_args.slots == [1]
    assert call_args.title == "Test Movie Title"


async def test_load_beq_profile_service_error_handling(
    hass: HomeAssistant,
    mock_ezbeq_client: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test error handling in the load_beq_profile service."""
    await setup_integration(hass, mock_config_entry)

    # Set up mock sensors
    hass.states.async_set("sensor.tmdb_id", "123456")
    hass.states.async_set("sensor.year", "2023")
    hass.states.async_set("sensor.codec", "Atmos")

    # Mock the load_beq_profile method to raise an exception
    mock_ezbeq_client.load_beq_profile.side_effect = Exception("Test error")

    with pytest.raises(HomeAssistantError):
        await hass.services.async_call(
            DOMAIN,
            "load_beq_profile",
            {
                "tmdb_sensor": "sensor.tmdb_id",
                "year_sensor": "sensor.year",
                "codec_sensor": "sensor.codec",
            },
            blocking=True,
        )


async def test_load_beq_profile_service_missing_sensor(
    hass: HomeAssistant,
    mock_ezbeq_client: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test error handling when a required sensor is missing."""
    await setup_integration(hass, mock_config_entry)

    with pytest.raises(HomeAssistantError):
        await hass.services.async_call(
            DOMAIN,
            "load_beq_profile",
            {
                "tmdb_sensor": "sensor.non_existent_sensor",
                "year_sensor": "sensor.year",
                "codec_sensor": "sensor.codec",
            },
            blocking=True,
        )


async def test_load_beq_profile_service_unload(
    hass: HomeAssistant,
    mock_ezbeq_client: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test that the load_beq_profile service is removed when the config entry is unloaded."""
    await setup_integration(hass, mock_config_entry)

    # Ensure the service is initially registered
    assert hass.services.has_service(DOMAIN, "load_beq_profile")

    # Unload the entry
    await hass.config_entries.async_unload(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    # Ensure the service was removed
    assert not hass.services.has_service(DOMAIN, "load_beq_profile")


async def test_unload_beq_profile_service(
    hass: HomeAssistant,
    mock_ezbeq_client: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test the unload_beq_profile service."""
    await setup_integration(hass, mock_config_entry)

    # Ensure the service was registered
    assert hass.services.has_service(DOMAIN, "unload_beq_profile")

    # Mock the unload_beq_profile method of the client
    mock_ezbeq_client.unload_beq_profile = AsyncMock()

    # Call the service
    await hass.services.async_call(
        DOMAIN,
        "unload_beq_profile",
        {
            "slots": [1, 2],
            "dry_run_mode": False,
        },
        blocking=True,
    )

    # Check if the unload_beq_profile method was called with the correct arguments
    mock_ezbeq_client.unload_beq_profile.assert_called_once()
    call_args = mock_ezbeq_client.unload_beq_profile.call_args[0][0]
    assert isinstance(call_args, SearchRequest)
    assert call_args.slots == [1, 2]
    assert call_args.dry_run_mode == False


async def test_unload_beq_profile_service_error_handling(
    hass: HomeAssistant,
    mock_ezbeq_client: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test error handling in the unload_beq_profile service."""
    await setup_integration(hass, mock_config_entry)

    # Mock the unload_beq_profile method to raise an exception
    mock_ezbeq_client.unload_beq_profile.side_effect = Exception("Test error")

    with pytest.raises(HomeAssistantError):
        await hass.services.async_call(
            DOMAIN,
            "unload_beq_profile",
            {"slots": [1]},
            blocking=True,
        )
