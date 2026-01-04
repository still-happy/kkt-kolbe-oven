"""Tuya local device communication for KKT Kolbe Oven."""
import logging
import tinytuya

from .const import (
    DP_SWITCH,
    DP_MODE,
    DP_TEMPERATURE,
    DP_TIME,
    DP_DOOR_STATE,
    DP_STATUS,
)

_LOGGER = logging.getLogger(__name__)


class KKTOvenDevice:
    """Representation of a KKT Kolbe Oven using local Tuya protocol."""

    def __init__(self, device_id: str, local_key: str, ip_address: str):
        """Initialize the oven device."""
        self.device_id = device_id
        self.local_key = local_key
        self.ip_address = ip_address
        self._device = None
        self._status = {}
        self._connect()

    def _connect(self):
        """Connect to the device."""
        try:
            self._device = tinytuya.Device(
                dev_id=self.device_id,
                address=self.ip_address,
                local_key=self.local_key,
                version=3.3,
            )
            self._device.set_socketPersistent(True)
            _LOGGER.info("Connected to KKT Kolbe Oven at %s", self.ip_address)
        except Exception as err:
            _LOGGER.error("Failed to connect to device: %s", err)
            raise

    def update_status(self) -> dict:
        """Update device status."""
        try:
            status = self._device.status()
            _LOGGER.debug("Raw status from device: %s", status)
            
            if status and "dps" in status:
                self._status = status["dps"]
                return self._status
            else:
                _LOGGER.warning("No valid status received from device")
                return self._status
        except Exception as err:
            _LOGGER.error("Error updating status: %s", err)
            # Try to reconnect
            self._connect()
            return self._status

    def set_power(self, state: bool) -> bool:
        """Turn the oven on or off."""
        try:
            result = self._device.set_value(DP_SWITCH, state)
            _LOGGER.debug("Set power to %s: %s", state, result)
            return True
        except Exception as err:
            _LOGGER.error("Error setting power: %s", err)
            return False

    def set_mode(self, mode: str) -> bool:
        """Set cooking program."""
        try:
            result = self._device.set_value(DP_MODE, mode)
            _LOGGER.debug("Set mode to %s: %s", mode, result)
            return True
        except Exception as err:
            _LOGGER.error("Error setting mode: %s", err)
            return False

    def set_temperature(self, temperature: int) -> bool:
        """Set target temperature."""
        try:
            result = self._device.set_value(DP_TEMPERATURE, temperature)
            _LOGGER.debug("Set temperature to %s: %s", temperature, result)
            return True
        except Exception as err:
            _LOGGER.error("Error setting temperature: %s", err)
            return False

    def set_time(self, minutes: int) -> bool:
        """Set timer in minutes."""
        try:
            result = self._device.set_value(DP_TIME, minutes)
            _LOGGER.debug("Set time to %s minutes: %s", minutes, result)
            return True
        except Exception as err:
            _LOGGER.error("Error setting time: %s", err)
            return False

    @property
    def is_on(self) -> bool:
        """Return True if oven is on."""
        return self._status.get(DP_SWITCH, False)

    @property
    def current_mode(self) -> str:
        """Return current cooking mode."""
        return self._status.get(DP_MODE, "0")

    @property
    def current_temperature(self) -> int:
        """Return current temperature setting."""
        return self._status.get(DP_TEMPERATURE, 0)

    @property
    def current_time(self) -> int:
        """Return current time setting in minutes."""
        return self._status.get(DP_TIME, 0)

    @property
    def door_open(self) -> bool:
        """Return True if door is open."""
        return self._status.get(DP_DOOR_STATE, False)

    @property
    def status(self) -> str:
        """Return current status."""
        return self._status.get(DP_STATUS, "unknown")

    @property
    def available(self) -> bool:
        """Return True if device is available."""
        return bool(self._status)
