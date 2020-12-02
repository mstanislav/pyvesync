"""Support for Etekcity VeSync scales"""
import logging

from . import DOMAIN

_LOGGER = logging.getLogger(__name__)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the VeSync scale platform."""

    if discovery_info is None:
        return

    scales = []

    manager = hass.data[DOMAIN]['manager']

    if manager.scales is not None and manager.scales:
        if len(manager.scales) == 1:
            count_string = "scale"
        else:
            count_string = "scales"

        for scale in manager.scales:
            scales.append(VeSyncScaleHA(scale))
            _LOGGER.info("Added a VeSync scale named '%s'",
                         scale.device_name)
    else:
        _LOGGER.info("No VeSync scales found")

    add_entities(scales)


class VeSyncScaleHA(ScaleEntity):
    """Representation of a VeSync scale."""

    def __init__(self, scale):
        """Initialize the VeSync scale device."""
        self.smartscale = scale

    @property
    def is_on(self):
        """Return True if device is on"""
        return self.smartscale.device_status == "on"

    @property
    def unique_info(self):
        """Return the ID of this scale."""
        return self.smartscale.uuid

    @property
    def name(self):
        """Return the name of the scale."""
        return self.smartscale.device_name

    @property
    def device_state_attributes(self):
        """Return the state attributes of the scale."""
        attr = {}
        attr['weight'] = self.smartscale.weight
        return attr

    def update(self):
        self.smartscale.update()
