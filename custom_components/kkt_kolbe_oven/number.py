"""Number platform for KKT Kolbe Oven."""
import logging

from homeassistant.components.number import NumberEntity, NumberMode
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature, UnitOfTime
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, TEMP_MIN, TEMP_MAX, TIME_MIN, TIME_MAX

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the KKT Kolbe Oven number entities."""
    data = hass.data[DOMAIN][entry.entry_id]
    device = data["device"]
    coordinator = data["coordinator"]

    async_add_entities(
        [
            KKTOvenTemperature(coordinator, device, entry),
            KKTOvenTime(coordinator, device, entry),
        ]
    )


class KKTOvenTemperature(CoordinatorEntity, NumberEntity):
    """Representation of the KKT Kolbe Oven temperature control."""

    def __init__(self, coordinator, device, entry):
        """Initialize the number entity."""
        super().__init__(coordinator)
        self._device = device
        self._attr_name = f"{entry.data.get('name', 'KKT Kolbe Backofen')} Temperatur"
        self._attr_unique_id = f"{entry.data['device_id']}_temperature"
        self._attr_native_min_value = TEMP_MIN
        self._attr_native_max_value = TEMP_MAX
        self._attr_native_step = 1
        self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
        self._attr_mode = NumberMode.BOX
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.data["device_id"])},
        }

    @property
    def native_value(self) -> float:
        """Return the current temperature setting."""
        return self._device.current_temperature

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self._device.available

    async def async_set_native_value(self, value: float) -> None:
        """Set new temperature."""
        await self.hass.async_add_executor_job(self._device.set_temperature, int(value))
        await self.coordinator.async_request_refresh()


class KKTOvenTime(CoordinatorEntity, NumberEntity):
    """Representation of the KKT Kolbe Oven time control."""

    def __init__(self, coordinator, device, entry):
        """Initialize the number entity."""
        super().__init__(coordinator)
        self._device = device
        self._attr_name = f"{entry.data.get('name', 'KKT Kolbe Backofen')} Zeit"
        self._attr_unique_id = f"{entry.data['device_id']}_time"
        self._attr_native_min_value = TIME_MIN
        self._attr_native_max_value = TIME_MAX
        self._attr_native_step = 1
        self._attr_native_unit_of_measurement = UnitOfTime.MINUTES
        self._attr_mode = NumberMode.BOX
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.data["device_id"])},
        }

    @property
    def native_value(self) -> float:
        """Return the current time setting."""
        return self._device.current_time

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self._device.available

    async def async_set_native_value(self, value: float) -> None:
        """Set new time."""
        await self.hass.async_add_executor_job(self._device.set_time, int(value))
        await self.coordinator.async_request_refresh()
