#!/usr/bin/env python

import collections


def _read_ref(data, refpath):
    if not refpath.startswith("#/"):
        raise NotImplementedError

    refpath = refpath.split("/")[1:]
    cur = data
    for step in refpath:
        cur = cur[step]
    return cur


def resolve_references(data, original=None):
    if original is None:
        original = data

    if isinstance(data, dict):
        if "$ref" not in data:
            return collections.OrderedDict(
                [(k, resolve_references(v, original)) for (k, v) in data.items()]
            )
        else:
            return _read_ref(original, data["$ref"])
    elif isinstance(data, list):
        return [resolve_references(v, original) for v in data]
    else:
        return data
