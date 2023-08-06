import configparser


class Peer:

    def __init__(self):
        self._config = configparser.RawConfigParser()

    @classmethod
    def import_(cls, config):
        """
        Imports peer from string.
        :param config:
        :return:
        """
        instnace = cls()
        for line in config:
            line = line.strip()
            setattr(instnace, line.split(":")[0].replace(" ", "_"), line.split(":")[1])
        return instnace

    @classmethod
    def parse_config(cls, peer_config):
        """
        Imports Peer from config.
        :param peer_config:
        :return:
        """
        instance = cls()
        instance._config["Peer"] = peer_config["Peer"]
        for key, value in peer_config.items("Peer"):
            setattr(instance, key, value)
        return instance

    def __repr__(self):
        return str(self.export())

    def export(self) -> dict:
        """
        Export peer.
        :return: Public attrs of a Peer
        """

        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}
