""" Module responsible for hosting all EVC imported from backend
or from YAML file. Any operation performed by evc_manager over an EVC
has to pass through this module to guarantee we have the right EVC. """


from .cli import CliOptions
from .evc_to_dict import convert_class


class EvcsList(object):
    """ List of EVCs """

    def __init__(self, evc_list=None):
        self._evcs = list()
        if evc_list:
            self.evcs = evc_list

    @property
    def evcs(self):
        """ Getter """
        return self._evcs

    @evcs.setter
    def evcs(self, evc_list):
        """ Setter """
        # TODO: Validate input
        self._evcs = self.filter(evc_list)

    def to_dict(self):
        """ Convert to self to dictionary """
        return convert_class(self.evcs)

    def find(self, target_evc):
        """ Return True if a specific EVC already exists """
        for evc in self.evcs:
            if target_evc == evc:
                return evc
        return False

    @staticmethod
    def has_device(evc_list):
        if CliOptions().has_uni_device:
            evcs_to_add = list()
            for evc in evc_list:
                for uni in evc.unis:
                    if uni.device == CliOptions().has_uni_device:
                        evcs_to_add.append(evc)
                        break

            return evcs_to_add
        else:
            return evc_list

    @staticmethod
    def has_interface(evc_list):
        if CliOptions().has_uni_interface:
            evcs_to_add = list()
            for evc in evc_list:
                for uni in evc.unis:
                    if uni.interface_name == CliOptions().has_uni_interface:
                        evcs_to_add.append(evc)
                        break

            return evcs_to_add
        else:
            return evc_list

    @staticmethod
    def has_tag_value(evc_list):
        if CliOptions().has_uni_tag_value:
            evcs_to_add = list()
            for evc in evc_list:
                for uni in evc.unis:
                    if uni.tag.value == CliOptions().has_uni_tag_value:
                        evcs_to_add.append(evc)
                        break

            return evcs_to_add
        else:
            return evc_list

    def filter(self, evc_list):
        if not CliOptions().has_uni_filters:
            return evc_list

        return self.has_tag_value(self.has_interface(self.has_device(evc_list)))
