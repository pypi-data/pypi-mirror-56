import collections
import json
import sys


def _try_import_yaml():
    try:
        import yaml
    except ImportError:
        print("ERROR: yaml support requires 'resolvref[yaml]'", file=sys.stderr)
        sys.exit(2)
    return yaml


def load_yaml(filename):
    yaml = _try_import_yaml()

    class OrderedLoader(yaml.Loader):
        pass

    def dict_constructor(loader, node):
        loader.flatten_mapping(node)
        return collections.OrderedDict(loader.construct_pairs(node))

    OrderedLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, dict_constructor
    )

    with open(filename, "r") as fp:
        return yaml.load(fp, Loader=OrderedLoader)


def write_yaml(data, stream):
    yaml = _try_import_yaml()

    class OrderedDumper(yaml.Dumper):
        pass

    def dict_representer(dumper, data):
        return dumper.represent_dict(data.items())

    OrderedDumper.add_representer(collections.OrderedDict, dict_representer)

    yaml.dump(data, stream, Dumper=OrderedDumper)


def load_json(filename):
    with open(filename, "r") as fp:
        return json.load(fp, object_pairs_hook=collections.OrderedDict)


def write_json(data, stream):
    json.dump(data, stream)
