"""Binary sensor platform for KKT Kolbe Oven."""
import logging

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorDeviceClass,
)
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
    """Set up the KKT Kolbe Oven binary sensors."""
    data = hass.data[DOMAIN][entry.entry_id]
    device = data["device"]
    coordinator = data["coordinator"]

    async_add_entities([KKTOvenDoorSensor(coordinator, device, entry)])


class KKTOvenDoorSensor(CoordinatorEntity, BinarySensorEntity):
    """Representation of the KKT Kolbe Oven door sensor."""

    _attr_device_class = BinarySensorDeviceClass.DOOR

    def __init__(self, coordinator, device, entry):
        """Initialize the binary sensor."""
        super().__init__(coordinator)
        self._device = device
        self._attr_name = f"{entry.data.get('name', 'KKT Kolbe Backofen')} Tür"
        self._attr_unique_id = f"{entry.data['device_id']}_door"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.data["device_id"])},
        }

    @property
    def is_on(self) -> bool:
        """Return True if the door is open."""
        return self._device.door_open

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self._device.available
