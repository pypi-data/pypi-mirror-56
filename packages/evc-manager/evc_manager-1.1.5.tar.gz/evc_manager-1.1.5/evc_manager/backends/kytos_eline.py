""" Kytos MEF E-Line application's backend """


import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning  # pylint: disable=E1101
import sys
import time
import copy
from ..libs.core.cli import CliOptions
from ..libs.core.log import info
from ..libs.core.log import warn
from ..libs.core.log import debug
from .generic_backend import Backend


class KytosEline(Backend):
    """ Kytos MEF E-Line application's backend. Kytos does not have authentication yet. """

    def get_evcs(self):
        """ Returns a list of all EVCs """
        return []

    def add_evc(self, new_evc):
        """ Add EVC
        Args:
            new_evc:
        """

        warn("Provisioning circuit...")
        if self.provision_circuit(new_evc):
            msg = {'result': 'created',
                   'msg': 'EVC %s provisioned.' % new_evc.name}
            return msg

        return {'result': 'error',
                'msg': 'Error provisioning EVC %s' % new_evc.name}

    def delete_evc(self, evc_to_delete):
        """ Delete EVC with the provided EVC(s) name(s) """
        pass
