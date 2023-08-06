from os import environ
from pathlib import Path

from pydantic import BaseModel


class ApeironConfig(BaseModel):
    storage_dir: Path = "~/apeiron/storage"
    modpack_index: str = "index.json"
    parallelism: int = 4
    debug: bool = False


_defaults = ApeironConfig()


cfg = ApeironConfig(
    storage_dir=Path(environ.get("APEIRON_STORAGE_DIR", _defaults.storage_dir)).expanduser().as_posix(),
    modpack_index=environ.get("APEIRON_MODPACK_INDEX", _defaults.modpack_index),
    parallelism=int(environ.get("APEIRON_PARALLELISM", _defaults.parallelism)),
    debug=("APEIRON_DEBUG" in environ),
)
