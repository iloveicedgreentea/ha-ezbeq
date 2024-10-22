from __future__ import annotations

import logging
from typing import Any

from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.exceptions import HomeAssistantError
from pyezbeq.models import SearchRequest

from .coordinator import EzBEQCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_services(
    hass: HomeAssistant, coordinator: EzBEQCoordinator, domain: str
) -> None:
    """Set up the EzBEQ services."""

    async def load_beq_profile(call: ServiceCall) -> None:
        """Load a BEQ profile."""

        def get_sensor_state(entity_id: str) -> Any:
            """Get the state of a sensor entity."""
            state = hass.states.get(entity_id)
            if state is None:
                raise HomeAssistantError(f"Sensor {entity_id} not found")
            return state.state

        try:
            search_request = SearchRequest(
                tmdb=get_sensor_state(call.data["tmdb_sensor"]),
                year=int(get_sensor_state(call.data["year_sensor"])),
                codec=get_sensor_state(call.data["codec_sensor"]),
                preferred_author=call.data.get("preferred_author", ""),
                edition=(
                    get_sensor_state(call.data["edition_sensor"])
                    if "edition_sensor" in call.data
                    else ""
                ),
                slots=call.data.get("slots", [1]),
                title=(
                    get_sensor_state(call.data["title_sensor"])
                    if "title_sensor" in call.data
                    else ""
                ),
            )
        except ValueError as e:
            raise HomeAssistantError(f"Invalid sensor data: {e}") from e

        try:
            await coordinator.client.load_beq_profile(search_request)
            _LOGGER.info("Successfully loaded BEQ profile")
        except Exception as e:
            _LOGGER.error("Failed to load BEQ profile: %s", e)
            raise HomeAssistantError(f"Failed to load BEQ profile: {e}") from e

    async def unload_beq_profile(call: ServiceCall) -> None:
        """Unload the BEQ profile."""
        try:
            slots = call.data.get("slots", [1])
            search_request = SearchRequest(
                preferred_author="",
                edition="",
                tmdb="",  # These fields are not used for unloading, but are required by the SearchRequest model
                year=0,
                codec="",
                slots=slots,
            )
            await coordinator.client.unload_beq_profile(search_request)
            _LOGGER.info("Successfully unloaded BEQ profile")
        except Exception as e:
            _LOGGER.error("Failed to unload BEQ profile: %s", e)
            raise HomeAssistantError(f"Failed to unload BEQ profile: {e}") from e

    hass.services.async_register(domain, "load_beq_profile", load_beq_profile)
    hass.services.async_register(domain, "unload_beq_profile", unload_beq_profile)


async def async_unload_services(hass: HomeAssistant, domain: str) -> None:
    """Unload EzBEQ services."""
    hass.services.async_remove(domain, "load_beq_profile")
