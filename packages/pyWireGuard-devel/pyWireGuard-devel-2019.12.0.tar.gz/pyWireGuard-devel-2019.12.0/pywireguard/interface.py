import subprocess
import os
import typing

from pywireguard.wg_configparser import ConfigParser
from pywireguard.exceptions import WGError
from pywireguard.peer import Peer
from pywireguard.constants import WG_PATH, WG_PEER


class Interface:

    def __init__(self):
        self._peers = []

    @classmethod
    def new(cls,
        interface: str,
        address: str,
        private_key: str = None,
        listen_port: int = 51820,
        save_config: bool = True,
        post_up: str = None,
        post_down: str = None,
        fw_mark: str = None) -> "Interface":
        """
        Creates new interface.
        :return: Interface
        """

        file_path = os.path.join(WG_PATH, interface + ".conf")

        if not os.path.exists(WG_PATH):
            raise WGError("Seems like wireguard is missing")

        if os.path.exists(file_path):
            raise WGError("Interface already exist")

        if not private_key:
            private_key = subprocess.check_output(["wg", "genkey"]).strip()

        config = ConfigParser()
        config["Interface"] = {
            "Address": address,
            "ListenPort": listen_port,
            "PrivateKey": private_key.decode() if isinstance(private_key, bytes) else private_key,
            "SaveConfig": save_config
        }
        if post_up:
            config["Interface"]["PostUp"] = post_up
        if post_down:
            config["Interface"]["PostDown"] = post_down
        if fw_mark:
            config["Interface"]["FwMark"] = fw_mark

        with open(file_path, "w") as interface_config:
            config.write(interface_config)
        return config

    @classmethod
    def import_(cls, config) -> "Interface":
        """
        Import interface from config string.
        :param config: str
        :return: Interface
        """
        instance = cls()
        for line in config.split():
            line = line.strip()
            key = line.split(":")[0].strip().replace(" ", "_")
            value = line.split(":")[1].strip()
            setattr(instance, key, value)
        return instance

    def import_peer(self, config):
        """
        Import peer from a config section.
        :param config:
        :return:
        """
        peer = Peer.import_(config)
        for _peer in self._peers:
            if _peer.public_key == peer.public_key:
                raise WGError("Peer already exist")
        self.add_peer(**peer.export())
        self._peers.append(Peer.import_(config))

    @classmethod
    def parse_config(cls, config_name: str, config_path: str) -> "Interface":
        """
        Parse wg.conf file.
        :param config_name: Name of interface
        :param config_path: Path to config file
        :return: None
        """
        instance = cls()

        instance.interface = config_name

        instance._config = ConfigParser()
        instance._config.read(config_path)

        for key, value in instance._config["Interface"].info.items():
            setattr(instance, key, value)

        if instance._config.has_section("Peer"):
            for peer in instance._config["Peer"]:
                instance._peers.append(Peer.parse_config(peer._config))

        return instance

    @property
    def state(self) -> bool:
        """
        Checks state of interface.
        :return: bool: up -> True, down -> False
        """
        wg = subprocess.check_output(["wg"]).decode()
        for item in wg.split("\n\n"):
            if item.startswith("interface"):
                iface = item.split("\n")[0].split(":")[1].strip()
                if iface == self.interface:
                    return True
        return False

    def up(self) -> typing.Union[str, bool]:
        """
        Turn interface on.
        :return: False if already up. Else output of wg command.
        """
        if self.state:
            return False
        return subprocess.check_output(["wg-quick", "up", self.interface]).decode()

    def down(self) -> typing.Union[str, bool]:
        """
        Turns off interface.
        :return: False if already down. Else output of wg command.
        """
        if not self.state:
            return False
        return subprocess.check_output(["wg-quick", "down", self.interface]).decode()

    def save(self):
        """
        Save interface. IMPORTANT: REQUIRES INTERFACE TO BE DOWN!
        :return:
        """

        bring_up = False
        if self.state:
            bring_up = True
            self.down()

        config = ConfigParser()
        iface = {}

        for attr in self.__dict__:
            if not attr.startswith("_") and attr != "interface":
                iface[attr] = getattr(self, attr)
        config["Interface"] = iface

        conf_path = os.path.join(WG_PATH, self.interface + ".conf")

        with open(conf_path, "w") as interface_config:
            config.write(interface_config)

        with open(conf_path, "a") as interface_config:
            for peer in self._peers:
                peer._config.write(interface_config)

        if bring_up:
            self.up()

    def add_peer(self, public_key, allowed_ips, address=None):
        """
        Add peer to interface.
        :param public_key:
        :param allowed_ips:
        :param address:
        :return:
        """

        command = WG_PEER + "{public_key} allowed-ips {allowed_ips}"
        if address:
            command += " endpoint {address}"

        return subprocess.check_output(command.format(
            interface=self.interface,
            public_key=public_key,
            allowed_ips=allowed_ips,
            address=address
        ), shell=True)

    def delete_peer(self, public_key):
        """
        Delete peer from interface.
        :param public_key:
        :return:
        """

        command = WG_PEER + "{public_key} remove"

        return subprocess.check_output(command.format(
            interface=self.interface,
            public_key=public_key
        ), shell=True)
