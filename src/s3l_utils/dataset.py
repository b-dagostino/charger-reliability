from pathlib import Path
from types import SimpleNamespace

import pandas as pd
from schema import Schema, And, Use, Or
import yaml


# Schemas
## Existing file
class PathPrefixPrepender:
    def validate(self, data, path_prefix: Path = Path()):
        return path_prefix / data


existing_file_path_schema = Schema(And(Use(Path), PathPrefixPrepender(), Path.is_file))

## Dataset manifest
dataset_manifest_schema_dict = {}
dataset_manifest_schema = Schema(dataset_manifest_schema_dict)
dataset_manifest_schema_dict.update(
    {str: Or(existing_file_path_schema, dataset_manifest_schema)}
)

## Easy access of schemas through namespace
schemas = SimpleNamespace(dataset_manifest=dataset_manifest_schema)


# Dataset wrapper class
class Dataset:
    """Convenience wrapper for datasets described by manifest.yml"""

    def __init__(self, manifest_path: Path | str) -> None:
        if isinstance(manifest_path, str):
            manifest_path = Path(manifest_path)

        # Open manifest
        with open(manifest_path) as f:
            manifest = yaml.safe_load(f)

        # Validate manifest
        manifest = schemas.dataset_manifest.validate(
            manifest, path_prefix=manifest_path.parent
        )

        # Create namespaces attributes for easy access and pandas dataframes from CSVs
        def dict_to_namespace(d: dict):
            for k, v in d.items():
                if isinstance(v, dict):
                    d[k] = dict_to_namespace(v)
                elif isinstance(v, Path) and v.suffix.lower() == ".csv":
                    d[k] = pd.read_csv(v, keep_default_na=False)
            return SimpleNamespace(**d)

        self.__dict__.update(dict_to_namespace(manifest).__dict__)
