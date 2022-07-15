# Anti Malware Policy Manager for Cloud One Workload Security
import logging
import sys
from pprint import pprint as pp
from typing import Optional


from const import (
    LIST_TYPES,
    SCAN_CONFIGURATIONS,
    DEFAULT_REALTIME_POLICY,
    DEFAULT_SCHEDULED_POLICY,
)
from config import Config
from connector import CloudOneConnector
from antimalwarelists import AntiMalwareLists
from antimalwareconfigurations import AntiMalwareConfigurations

_LOGGER = logging.getLogger(__name__)
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s (%(threadName)s) [%(funcName)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


class AntiMalwarePolicyManager:
    """AntiMalwarePolicyManager - creates and maintains anti malware lists and policies.

    Attributes:
        configuration (Config): Optional configuration, by default configuration will be loaded from following files:
              ~/policymgr.cfg.yaml
              ./policymgr.cfg.yaml
              <package_path>/policymgr/policymgr.cfg.yaml
            Later overwrites former
    """

    def __init__(self, configuration: Optional[Config] = None):
        if configuration is None:
            configuration = Config.global_instance()
        self.config = configuration
        self.connector = CloudOneConnector()
        self.antimalwareconfigurations = AntiMalwareConfigurations(self.connector)
        self.antimalwarelists = AntiMalwareLists(self.connector)
        
        pp("# Configurations")
        pp(self.antimalwareconfigurations.configurations)
        pp("# Lists")
        pp(self.antimalwarelists.lists)
        

    def build_config(self, scan_configuration, scan_config, scan_type):
        """Main worker method. Builds the inclusion and exclusion lists as
           defined in the config.yaml. Exclusion lists are named as
           exclusion_<LISTNAME>, inclusion lists as inclusion_<LISTNAME>.
           Eventually existing lists are updated, missing lists are created.

        Example nanming:
            realtime_scan_configuration:
              - name: windows_server_2016_domain_controller
                ## Inclusion Lists
                inclusions: []
                ## Exclusion Lists
                exclusions: []

            results in
            inclusion_realtime_windows_server_2016_domain_controller
            exclusion_realtime_windows_server_2016_domain_controller

        Args:
            scan_config (dict): Dictionary based on the config.yaml
            scan_type (str): First word of the scan configuration as defined in SCAN_CONFIGURATIONS

        """

        exclusions = scan_config["exclusions"][0]
        inclusions = scan_config["inclusions"][0]
        # This is the dict of inclusion and exclusion lists assigned to the scan configuration
        list_ids = {}

        # Exclusions
        for list_type in LIST_TYPES:
            exclusion_list = []
            # Build concatenated list of items
            if exclusions.get(list_type) != None:
                exclusion_list = self.antimalwarelists.concat_lists(
                    "exclusion_lists", list_type, exclusions.get(list_type)
                )
            _LOGGER.debug(
                f"Exclusion {list_type} for {scan_config['name']}: {exclusion_list}"
            )
            # If the list is not empty, manage the list entity in Cloud One
            if len(exclusion_list) > 0:
                list_id = self.antimalwarelists.query_list(
                    list_type,
                    f"exclusion_{scan_type}_{scan_config['name']}",
                )
                body = {
                    "name": f"exclusion_{scan_type}_{scan_config['name']}",
                    "items": exclusion_list,
                }
                result = 0
                if list_id == None:
                    _LOGGER.info(
                        f"Creating exclusion {list_type} for {scan_config['name']} with id {list_id}"
                    )
                    result = self.connector.post(
                        list_type.replace("_", ""), "", data=body
                    )
                    _LOGGER.info(
                        f"Exclusion {list_type} for {scan_config['name']} has id {result.get('ID', -1)}"
                    )
                else:
                    _LOGGER.info(
                        f"Updating exclusion {list_type} for {scan_config['name']} with id {list_id}"
                    )
                    result = self.connector.post(
                        list_type.replace("_", ""), variable=str(list_id), data=body
                    )
                    _LOGGER.info(
                        f"Exclusion {list_type} for {scan_config['name']} has id {result.get('ID', -1)}"
                    )
                list_ids[LIST_TYPES[list_type]["exclude"]] = result.get("ID", 0)
            else:
                list_ids[LIST_TYPES[list_type]["exclude"]] = 0

        # Inclusions
        for list_type in LIST_TYPES:
            # There is no file list for includes
            if list_type == "file_lists":
                continue

            # Build concatenated list of items
            inclusion_list = []
            if inclusions.get(list_type) != None:
                inclusion_list = self.antimalwarelists.concat_lists(
                    "inclusion_lists", list_type, inclusions.get(list_type)
                )
            _LOGGER.debug(
                f"Inclusion {list_type} for {scan_config['name']}: {inclusion_list}"
            )
            # If the list is not empty, manage the list entity in Cloud One
            if len(inclusion_list) > 0:
                list_id = self.antimalwarelists.query_list(
                    list_type,
                    f"inclusion_{scan_type}_{scan_config['name']}",
                )
                body = {
                    "name": f"inclusion_{scan_type}_{scan_config['name']}",
                    "items": inclusion_list,
                }
                result = 0
                if list_id == None:
                    _LOGGER.info(
                        f"Creating inclusion {list_type} for {scan_config['name']} with id {list_id}"
                    )
                    result = self.connector.post(
                        list_type.replace("_", ""), "", data=body
                    )
                    _LOGGER.info(
                        f"Inclusion {list_type} for {scan_config['name']} has id {result.get('ID', -1)}"
                    )
                else:
                    _LOGGER.info(
                        f"Updating inclusion {list_type} for {scan_config['name']} with id {list_id}"
                    )
                    result = self.connector.post(
                        list_type.replace("_", ""), variable=str(list_id), data=body
                    )
                    _LOGGER.info(
                        f"Inclusion {list_type} for {scan_config['name']} has id {result.get('ID', -1)}"
                    )
                list_ids[LIST_TYPES[list_type]["include"]] = result.get("ID", 0)
            else:
                list_ids[LIST_TYPES[list_type]["include"]] = 0

        configuration_name = f"{scan_type}_{scan_config['name']}_configuration"
        configuration_id = self.antimalwareconfigurations.query_configuration(
            configuration_name
        )
        if scan_configuration == "realtime_scan_configuration":
            body = {**DEFAULT_REALTIME_POLICY, **list_ids}
        else:
            body = {**DEFAULT_SCHEDULED_POLICY, **list_ids}
        body["name"] = configuration_name

        result = 0
        if configuration_id == None:
            _LOGGER.info(
                f"Creating scan configuration {configuration_name} with id {configuration_id}"
            )
            result = self.connector.post("antimalwareconfigurations", "", data=body)
            _LOGGER.info(
                f"Scan configuration {configuration_name} has id {result.get('ID', -1)}"
            )
        else:
            _LOGGER.info(
                f"Updating scan configuration {configuration_name} with id {configuration_id}"
            )
            result = self.connector.post(
                "antimalwareconfigurations", variable=str(configuration_id), data=body
            )
            _LOGGER.info(
                f"Scan configuration {configuration_name} has id {result.get('ID', -1)}"
            )

    def build_scan_configurations(self):
        """Main loop running over all scan configurations"""

        for scan_configuration in SCAN_CONFIGURATIONS:
            for configuration in self.config.data["malware_scan_configuration"][
                scan_configuration
            ]:
                print()
                _LOGGER.info(
                    f"Building {scan_configuration} configuration for {configuration['name']}"
                )
                self.build_config(
                    scan_configuration, configuration, scan_configuration.split("_")[0]
                )


def main():
    """Main"""

    builder = AntiMalwarePolicyManager()
    builder.build_scan_configurations()


if __name__ == "__main__":
    main()
