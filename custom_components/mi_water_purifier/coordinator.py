"""Xiaomi water purifier miio coordinator."""

from datetime import timedelta
import logging
import math

from miio import Device, DeviceException

from homeassistant.const import CONF_HOST, CONF_SCAN_INTERVAL, CONF_TOKEN
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import PlatformNotReady
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)


class MiioCoordinator(DataUpdateCoordinator):
    """Miio coordinator."""

    def __init__(
        self,
        hass: HomeAssistant,
        config: ConfigType,
    ) -> None:
        """Initialize."""

        super().__init__(
            hass,
            _LOGGER,
            name="Xiaomi water purifier miio coordinator",
            always_update=False,
            update_method=self.async_update_data,
            # setup_method=self.async_setup,
            update_interval=config.get(CONF_SCAN_INTERVAL, SCAN_INTERVAL),
        )
        self._hass = hass
        try:
            self._device = Device(config[CONF_HOST], config[CONF_TOKEN])
        except DeviceException:
            _LOGGER.exception("Fail to setup Xiaomi water purifier")
            raise PlatformNotReady from None
        self.info = self._device.info()

    def get_status(self) -> list[int]:
        """Get miio data."""
        return self._device.send("get_prop", [])

    async def async_update_data(self):
        """Fetch data from API endpoint.

        This is the place to pre-process the data to lookup tables
        so entities can quickly look up their data.
        """
        status = await self.hass.async_add_executor_job(self.get_status)

        return {
            "TDS in": [status[0]],
            "TDS out": [status[1]],
            "PP filter": [
                int((status[11] - status[3]) / status[11] * 100),
                math.floor((status[11] - status[3]) / 24),
            ],
            "Front carbon filter": [
                int((status[13] - status[5]) / status[13] * 100),
                math.floor((status[13] - status[5]) / 24),
            ],
            "RO filter": [
                int((status[15] - status[7]) / status[15] * 100),
                math.floor((status[13] - status[5]) / 24),
            ],
            "Rear carbon filter": [
                int((status[17] - status[9]) / status[17] * 100),
                math.floor((status[13] - status[5]) / 24),
            ],
        }
