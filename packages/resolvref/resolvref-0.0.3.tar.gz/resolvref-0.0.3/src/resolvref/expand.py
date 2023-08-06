#!/usr/bin/env python

import contextlib

from resolvref.exceptions import RecursiveExpansionForbiddenError


def _is_ref(item):
    return isinstance(item, dict) and "$ref" in item


def _is_internal_ref(refpath):
    return str(refpath).startswith("#/")


class Resolver:
    def __init__(self, document, allow_recursive=True):
        self.document = document
        self.allow_recursive = allow_recursive
        # cache which maps known refs to parts of the document
        self._cache = {}
        self._refpaths = ["#"]

    @property
    def current_path(self):
        return self._refpaths[-1]

    @contextlib.contextmanager
    def _pathctx(self, refpath):
        if not _is_internal_ref(refpath):
            refpath = "/".join((self.current_path, str(refpath)))

        self._refpaths.append(refpath)
        yield
        self._refpaths.pop()

    def _resolve_refpath(self, refpath):
        if refpath in self._refpaths and not self.allow_recursive:
            raise RecursiveExpansionForbiddenError(
                "recursion detected with allow_recursive=False"
            )

        if refpath in self._cache:
            return self._cache[refpath]

        with self._pathctx(refpath):
            if _is_internal_ref(self.current_path):
                cur = self.document
            else:
                raise NotImplementedError("External references not yet supported.")

            for step in self.current_path.split("/")[1:]:
                cur = cur[step]

            self._cache[self.current_path] = cur
            return cur

    def _namespaced_resolution(self, namespace, data):
        with self._pathctx(namespace):
            return self._resolve_references(data)

    def _resolve_references(self, data):
        if _is_ref(data):
            return self._resolve_refpath(data["$ref"])

        if isinstance(data, dict):
            for k, v in data.items():
                data[k] = self._namespaced_resolution(k, v)
        elif isinstance(data, list):
            for i, v in enumerate(data):
                data[i] = self._namespaced_resolution(str(i), v)

        return data

    def resolve_references(self):
        return self._resolve_references(self.document)


def resolve_references(data, allow_recursive=True):
    resolver = Resolver(data, allow_recursive=allow_recursive)
    return resolver.resolve_references()
