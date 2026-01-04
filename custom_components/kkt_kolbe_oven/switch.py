"""Switch platform for KKT Kolbe Oven."""
import logging

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the KKT Kolbe Oven switch."""
    data = hass.data[DOMAIN][entry.entry_id]
    device = data["device"]
    coordinator = data["coordinator"]

    async_add_entities([KKTOvenSwitch(coordinator, device, entry)])


class KKTOvenSwitch(CoordinatorEntity, SwitchEntity):
    """Representation of the KKT Kolbe Oven power switch."""

    def __init__(self, coordinator, device, entry):
        """Initialize the switch."""
        super().__init__(coordinator)
        self._device = device
        self._attr_name = entry.data.get("name", "KKT Kolbe Backofen")
        self._attr_unique_id = f"{entry.data['device_id']}_switch"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.data["device_id"])},
            "name": self._attr_name,
            "manufacturer": "KKT Kolbe",
            "model": "EB8313HC",
        }

    @property
    def is_on(self) -> bool:
        """Return True if the oven is on."""
        return self._device.is_on

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self._device.available

    async def async_turn_on(self, **kwargs) -> None:
        """Turn the oven on."""
        await self.hass.async_add_executor_job(self._device.set_power, True)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs) -> None:
        """Turn the oven off."""
        await self.hass.async_add_executor_job(self._device.set_power, False)
        await self.coordinator.async_request_refresh()
