:warning: Work in progress :warning:  

Should work with `pyannote.database` `custom` branch

# Custom pyannote.database data loaders

`pyannote.database` provides built-in data loaders for most common speaker diarization file format: `RTTMLoader` for `.rttm` files and `UEMLoader` for `.uem` files.

In case those are not enough, `pyannote.database` supports the addition of custom data loaders using the `pyannote.database.loader` entry point.

## Defining custom data loaders

Here is an example of a Python package called `your_package` that defines two custom data loaders for files with `.ext1` and `.ext2` suffix respectively.

```python
# ~~~~~~~~~~~~~~~~ YourPackage/your_package/loader.py ~~~~~~~~~~~~~~~~
from pyannote.database import ProtocolFile
from pathlib import Path

class Ext1Loader:
    def __init__(self, ext1: Path):
        print(f'Initializing Ext1Loader with {ext1}')
        # your code should obviously do something smarter.
        # see pyannote.database.loader.RTTMLoader for an example.
        self.ext1 = ext1

    def __call__(self, current_file: ProtocolFile) -> Text:
        uri = current_file["uri"]
        print(f'Processing {uri} with Ext1Loader')
        # your code should obviously do something smarter.
        # see pyannote.database.loader.RTTMLoader for an example.
        return f'{uri}.ext1'

class Ext2Loader:
    def __init__(self, ext2: Path):
        print(f'Initializing Ext2Loader with {ext2}')
        # your code should obviously do something smarter.
        # see pyannote.database.loader.RTTMLoader for an example.
        self.ext2 = ext2

    def __call__(self, current_file: ProtocolFile) -> Text:
        uri = current_file["uri"]
        print(f'Processing {uri} with Ext2Loader')
        # your code should obviously do something smarter.
        # see pyannote.database.loader.RTTMLoader for an example.
        return f'{uri}.ext2'
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
```

The `__init__` method expects a unique positional argument of type `Path` that provides the path to the data file in the custom data format.

`__call__` expects a unique positional argument of type `ProtocolFile` and returns the data for the given file. 

It is recommended to make `__init__` as fast and light as possible and delegate all the data filtering and formatting to `__call__`. For instance, `RTTMLoader.__init__` uses `pandas` to load the full `.rttm` file as fast as possible in a `DataFrame`, while `RTTMLoader.__call__` takes care of selecting rows that correspond to the requested file and convert them into a `pyannote.core.Annotation`. 


## Registering custom data loaders

At this point, `pyannote.database` has no idea of the existence of these new custom data loaders. They must be registered using the `pyannote.database.loader` entry-point in `your_package`'s `setup.py`, and then install the library `pip install your_package` (or `pip install -e YourPackage/` if it is not published on PyPI yet).

```python
# ~~~~~~~~~~~~~~~~~~~~~~~ YourPackage/setup.py ~~~~~~~~~~~~~~~~~~~~~~~
from setuptools import setup, find_packages
setup(
    name="your_package",
    packages=find_packages(),
    install_requires=[
        "pyannote.database >= 4.0",
    ]
    entry_points={
        "pyannote.database.loader": [
            # load files with extension '.ext1' 
            # with your_package.loader.Ext1Loader
            ".ext1 = your_package.loader:Ext1Loader",
            # load files with extension '.ext2' 
            # with your_package.loader.Ext2Loader
            ".ext2 = your_package.loader:Ext2Loader",
        ],
    }
)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
```

## Testing custom data loaders

Now that `.ext1` and `.ext2` data loaders are registered, they will be used automatically by `pyannote.database` when parsing the sample `demo/database.yml` custom protocol configuration file.

```yaml
# ~~~~~~~~~~~~~~~~~~~~~~~~~~ demo/database.yml ~~~~~~~~~~~~~~~~~~~~~~~~~~
Protocols:
  MyDatabase:
    SpeakerDiarization:
      MyProtocol:
        train:
           uri: train.lst
           key1: train.ext1
           key2: train.ext2
```

```python
# tell pyannote.database about the configuration file
>>> import os
>>> os.environ['PYANNOTE_DATABASE_CONFIG'] = 'demo/database.yml'

# load custom protocol
>>> from pyannote.database import get_protocol
>>> protocol = get_protocol('MyDatabase.SpeakerDiarization.MyProtocol')

# get first file of training set
>>> first_file = next(protocol.train())
Initializing Ext1Loader with file train.ext1
Initializing Ext2Loader with file train.ext2

# access its "key1" and "key2" keys.
>>> assert first_file["key1"] == 'fileA.ext1'
Processing fileA with Ext1Loader
>>> assert first_file["key2"] == 'fileA.ext2'
Processing fileA with Ext2Loader
# note how __call__ is only called now (and not before)
# this is why it is better to delegate all the filtering and formatting to __call__

>>> assert first_file["key1"] == 'fileA.ext1'
# note how __call__ is not called the second time thanks to ProtocolFile built-in cache
```

