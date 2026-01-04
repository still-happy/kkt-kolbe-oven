"""Config flow for KKT Kolbe Oven integration."""
import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
import homeassistant.helpers.config_validation as cv

from .const import DOMAIN, CONF_DEVICE_ID, CONF_LOCAL_KEY, CONF_IP_ADDRESS
from .tuya_device import KKTOvenDevice

_LOGGER = logging.getLogger(__name__)

DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_DEVICE_ID): cv.string,
        vol.Required(CONF_LOCAL_KEY): cv.string,
        vol.Required(CONF_IP_ADDRESS): cv.string,
        vol.Optional("name", default="KKT Kolbe Backofen"): cv.string,
    }
)


async def validate_input(hass: HomeAssistant, data: dict) -> dict:
    """Validate the user input allows us to connect."""
    
    device = KKTOvenDevice(
        device_id=data[CONF_DEVICE_ID],
        local_key=data[CONF_LOCAL_KEY],
        ip_address=data[CONF_IP_ADDRESS],
    )

    # Test connection
    try:
        status = await hass.async_add_executor_job(device.update_status)
        if not status:
            raise ConnectionError("Could not connect to device")
    except Exception as err:
        _LOGGER.error("Validation failed: %s", err)
        raise

    return {"title": data.get("name", "KKT Kolbe Backofen")}


class KKTOvenConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for KKT Kolbe Oven."""

    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
                
                await self.async_set_unique_id(user_input[CONF_DEVICE_ID])
                self._abort_if_unique_id_configured()

                return self.async_create_entry(title=info["title"], data=user_input)
            except ConnectionError:
                errors["base"] = "cannot_connect"
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user",
            data_schema=DATA_SCHEMA,
            errors=errors,
            description_placeholders={
                "device_id_example": "bfb4f01ea3d224d9a2vbdh",
                "local_key_example": "P-m]sOpKR0e5D[wK",
                "ip_example": "192.168.1.100",
            },
        )
