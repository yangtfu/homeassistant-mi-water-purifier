"""Support for Xiaomi water purifier."""

import logging

import voluptuous as vol

from config.custom_components.mi_water_purifier.const import DOMAIN, SENSORS
from config.custom_components.mi_water_purifier.coordinator import MiioCoordinator
from homeassistant.components.sensor import (
    PLATFORM_SCHEMA as SENSOR_PLATFORM_SCHEMA,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import (
    CONF_HOST,
    CONF_SCAN_INTERVAL,
    CONF_TOKEN,
    CONF_UNIQUE_ID,
    PERCENTAGE,
)
from homeassistant.core import HomeAssistant, callback
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.helpers.update_coordinator import CoordinatorEntity

_LOGGER = logging.getLogger(__name__)

# Validation of the user's configuration
SENSOR_PLATFORM_SCHEMA = SENSOR_PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_HOST): cv.string,
        vol.Required(CONF_TOKEN): cv.string,
        vol.Optional(CONF_SCAN_INTERVAL): cv.time_period,
        vol.Optional(CONF_UNIQUE_ID): cv.string,
    }
)


async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Perform the setup for Xiaomi water purifier."""
    coordinator = MiioCoordinator(hass, config)
    # await coordinator.async_config_entry_first_refresh()
    add_entities([XiaomiWaterPurifierSensor(coordinator, name) for name in SENSORS])


class XiaomiWaterPurifierSensor(SensorEntity, CoordinatorEntity):
    """Representation of a XiaomiWaterPurifierSensor."""

    def __init__(self, coordinator: MiioCoordinator, name: str) -> None:
        """Initialize the XiaomiWaterPurifierSensor."""
        super().__init__(coordinator)
        self._attr_should_poll = False
        self.name = name
        self._attr_unique_id = f"{coordinator.info.data['mac']}-{name}"
        self._attr_device_info = DeviceInfo(
            name="Xiaomi water purifier",
            manufacturer="Xiaomi",
            model=coordinator.info.data["model"],
            sw_version=coordinator.info.data["fw_ver"],
            identifiers={
                (
                    DOMAIN,
                    self.unique_id,
                )
            },
        )
        self._attr_state_class = SensorStateClass.MEASUREMENT
        if "TDS" in self.name:
            self._attr_icon = "mdi:water"
        else:
            self._attr_native_unit_of_measurement = PERCENTAGE
            self._attr_icon = "mdi:filter-outline"

    @callback
    def _handle_coordinator_update(self):
        """Get the latest data and updates the states."""
        _LOGGER.debug("[%s] updated", self.name)
        self._attr_native_value = self.coordinator.data[self.name][0]
        self.async_write_ha_state()
