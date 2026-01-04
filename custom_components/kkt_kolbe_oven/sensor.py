"""Sensor platform for KKT Kolbe Oven."""
import logging

from homeassistant.components.sensor import SensorEntity
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
    """Set up the KKT Kolbe Oven sensors."""
    data = hass.data[DOMAIN][entry.entry_id]
    device = data["device"]
    coordinator = data["coordinator"]

    async_add_entities([KKTOvenStatusSensor(coordinator, device, entry)])


class KKTOvenStatusSensor(CoordinatorEntity, SensorEntity):
    """Representation of the KKT Kolbe Oven status sensor."""

    def __init__(self, coordinator, device, entry):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device = device
        self._attr_name = f"{entry.data.get('name', 'KKT Kolbe Backofen')} Status"
        self._attr_unique_id = f"{entry.data['device_id']}_status"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.data["device_id"])},
        }

    @property
    def native_value(self) -> str:
        """Return the state of the sensor."""
        return str(self._device.status)

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self._device.available
