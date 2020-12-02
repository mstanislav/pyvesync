"""VeSync API for smart scales."""

import json
from pyvesync.vesyncbasedevice import VeSyncBaseDevice
from pyvesync.helpers import Helpers as helpers
import logging

logger = logging.getLogger(__name__)

def grams_to_pounds(grams):
    """Convert grams to pounds."""
    pounds = round(grams * 0.00220462, 1)
    return pounds

class VeSyncScaleESF14(VeSyncBaseDevice):
    """Etekcity Smart Scale Class."""

    def __init__(self, details, manager):
        """Initilize smart scale class."""
        super(VeSyncScaleESF14, self).__init__(details, manager)

        self.details = {}

    def get_details(self):
        """Build details dictionary."""
        body = helpers.req_body(self.manager, 'devicedetail')
        body['uuid'] = self.uuid
        body['page'] = '1'
        body['pageSize'] = '100'
        body['allData'] = 'true'
        body['method'] = 'getWeighingDataV2'
        body['configModule'] = 'BT_Scale_ESF14_US'
        head = helpers.req_headers(self.manager)

        r, _ = helpers.call_api(
            '/cloud/v2/deviceManaged/getWeighingDataV2',
            method='post',
            headers=head,
            json=body
        )

        data = r['result']['weightDatas'][-1]

        if data is not None and helpers.code_check(r):
            self.weight = grams_to_pounds(data['weightG'])
            self.date = data['uploadTimestamp']
        else:
            logger.debug('Error getting %s details', self.device_name)

    def get_config(self):
        """Get configuration info for scale."""
        body = helpers.req_body(self.manager, 'devicedetail')
        body['uuid'] = self.uuid
        body['method'] = 'configurations'

        r, _ = helpers.call_api(
            '/cloud/v2/deviceManaged/devices',
            'post',
            headers=helpers.req_headers(self.manager),
            json=body)

        if helpers.code_check(r):
            self.config = helpers.build_config_dict(r)
        else:
            logger.warning("Unable to get config info for %s",
                           self.device_name)

    def update(self):
        """Run function to get device details."""
        self.get_details()

    def display(self):
        """Return formatted device info to stdout."""
        super(VeSyncScaleESF14, self).display()
        disp1 = [("Weight : ", self.weight, 'lbs'),("Date : ", self.date, "")]
        for line in disp1:
            print("{:.<15} {} {}".format(line[0], line[1], line[2]))

    def displayJSON(self):
        """Return air purifier status and properties in JSON output."""
        sup = super().displayJSON()
        supVal = json.loads(sup)
        supVal.append({
            "Weight": self.weight,
            "Date": self.date
            })
        return supVal
