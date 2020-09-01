from pyannote.database import ProtocolFile
from pathlib import Path


class Ext1Loader:
    def __init__(self, ext1: Path):
        print(f"Initializing Ext1Loader with {ext1}")
        # your code should obviously do something smarter.
        # see pyannote.database.loader.RTTMLoader for an example.
        self.ext1 = ext1

    def __call__(self, current_file: ProtocolFile):
        uri = current_file["uri"]
        print(f"Processing {uri} with Ext1Loader")
        # your code should obviously do something smarter.
        # see pyannote.database.loader.RTTMLoader for an example.
        return f"{uri}.ext1"


class Ext2Loader:
    def __init__(self, ext2: Path):
        print(f"Initializing Ext2Loader with {ext2}")
        # your code should obviously do something smarter.
        # see pyannote.database.loader.RTTMLoader for an example.
        self.ext2 = ext2

    def __call__(self, current_file: ProtocolFile):
        uri = current_file["uri"]
        print(f"Processing {uri} with Ext2Loader")
        # your code should obviously do something smarter.
        # see pyannote.database.loader.RTTMLoader for an example.
        return f"{uri}.ext2"
