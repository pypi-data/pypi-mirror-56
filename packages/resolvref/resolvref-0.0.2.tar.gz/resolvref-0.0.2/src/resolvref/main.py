#!/usr/bin/env python3
"""
Expand references inside of a JSON or YAML file

Preserves order
"""
import argparse
import sys

from resolvref.expand import resolve_references
from resolvref.formats import load_json, load_yaml, write_json, write_yaml


def _load_doc(filename, fileformat):
    if fileformat == "json":
        return load_json(filename)
    elif fileformat == "yaml":
        return load_yaml(filename)
    else:
        raise NotImplementedError


def _write_doc(data, filename_or_stream, fileformat):
    stream = filename_or_stream
    willopen = isinstance(filename_or_stream, str)
    try:
        if willopen:
            stream = open(filename_or_stream, "w")
        # write to stream
        if fileformat == "json":
            write_json(data, stream)
        elif fileformat == "yaml":
            write_yaml(data, stream)
        else:
            raise NotImplementedError
    finally:
        if willopen:
            stream.close()


def _detect_file_format(args):
    fileformat = args.format
    infile = args.INPUT_FILE
    if fileformat is None:
        if infile.endswith(".yml") or infile.endswith(".yaml"):
            fileformat = "yaml"
        else:
            fileformat = "json"
    return fileformat


def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("INPUT_FILE")
    parser.add_argument(
        "-o",
        "--output",
        default=sys.stdout,
        help="Output filename. Defaults to stdout.",
    )
    parser.add_argument(
        "-f",
        "--format",
        type=str.lower,
        choices=("json", "yaml"),
        default=None,
        help="File format, defaults to guessing by extension (and falling back to json)",
    )
    args = parser.parse_args(argv)
    fileformat = _detect_file_format(args)
    newdata = resolve_references(_load_doc(args.INPUT_FILE, fileformat))
    _write_doc(newdata, args.output, fileformat)


if __name__ == "__main__":
    main()
