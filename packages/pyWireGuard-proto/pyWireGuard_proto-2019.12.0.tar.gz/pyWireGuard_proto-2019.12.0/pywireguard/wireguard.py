import subprocess
import os

from os import listdir
from os.path import isfile, join

from pywireguard.exceptions import WGError
from pywireguard.interface import Interface


class WireGuard:

    def __init__(self):
        try:
            subprocess.check_output(["wg"])
        except Exception as e:
            raise WGError("Seems like WireGuard is not installed")

        self.interfaces = []

    @classmethod
    def _import(cls):
        """
        Import all configs from wg path.
        :return:
        """
        instance = cls()
        wg_path = os.path.join("/", "etc", "wireguard")
        interface_configs = [(f, os.path.join(wg_path, f)) for f in listdir(wg_path)
             if isfile(join(wg_path, f)) and f.endswith(".conf")]
        for config_name, config_path in interface_configs:
            instance.interfaces.append(Interface.parse_config(config_name.split(".")[0], config_path))
        return instance

    @classmethod
    def check_status(cls):
        """
        Check wg status.
        :return:
        """
        instance = cls()
        wg = subprocess.check_output(["wg"]).decode()
        interface = None
        for item in wg.split("\n\n"):
            if item.startswith("interface"):
                interface = Interface.import_(item.strip())
                instance.interfaces.append(interface)
            if item.startswith("peer") and interface:
                interface.import_peer(item.strip())
        return instance
