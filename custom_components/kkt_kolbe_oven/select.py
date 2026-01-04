"""Select platform for KKT Kolbe Oven."""
import logging

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, COOKING_PROGRAMS, PROGRAM_TO_CODE

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the KKT Kolbe Oven program selector."""
    data = hass.data[DOMAIN][entry.entry_id]
    device = data["device"]
    coordinator = data["coordinator"]

    async_add_entities([KKTOvenProgramSelect(coordinator, device, entry)])


class KKTOvenProgramSelect(CoordinatorEntity, SelectEntity):
    """Representation of the KKT Kolbe Oven program selector."""

    def __init__(self, coordinator, device, entry):
        """Initialize the select entity."""
        super().__init__(coordinator)
        self._device = device
        self._attr_name = f"{entry.data.get('name', 'KKT Kolbe Backofen')} Programm"
        self._attr_unique_id = f"{entry.data['device_id']}_program"
        self._attr_options = list(COOKING_PROGRAMS.values())
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.data["device_id"])},
        }

    @property
    def current_option(self) -> str:
        """Return the current selected program."""
        mode_code = str(self._device.current_mode)
        return COOKING_PROGRAMS.get(mode_code, "Unbekannt")

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self._device.available

    async def async_select_option(self, option: str) -> None:
        """Change the selected program."""
        mode_code = PROGRAM_TO_CODE.get(option)
        if mode_code:
            await self.hass.async_add_executor_job(self._device.set_mode, mode_code)
            await self.coordinator.async_request_refresh()
        else:
            _LOGGER.error("Invalid program option: %s", option)
