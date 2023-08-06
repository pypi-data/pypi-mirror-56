# -*- coding: utf-8 -*-

import os
import tempfile

import pytest


class ReferenceRetriever(object):
    def __init__(self, request, references_path, serializer, unserializer):
        self.request = request
        self.references_path = references_path
        self.serializer = serializer
        self.unserializer = unserializer

    @property
    def opt_create(self):
        return self.request.config.getoption("--create")

    def __setitem__(self, key, value):
        raise NotImplementedError()

    def __getitem__(self, key):
        raise NotImplementedError()

    def realpath(self, filename):
        ref_path = self.references_path
        ref_path = ref_path + os.sep if not ref_path.endswith(os.sep) else ref_path

        full_path = os.path.join(ref_path, filename)
        real_path = os.path.realpath(full_path)

        assert real_path.startswith(ref_path)

        return real_path

    def read(self, filename):
        real_path = self.realpath(filename)

        with open(real_path, "r") as f:
            return self.unserializer(f.read())

    def create(self, filename, content):
        real_path = self.realpath(filename)

        if not os.path.exists(self.references_path):
            os.mkdir(self.references_path)

        assert not os.path.exists(real_path)

        # TODO Py3: use 'x'
        with open(real_path, "w") as f:
            data = self.serializer(content)
            return f.write(data)

    def test_key(self):
        # Shall we build the fullpath? (with request.node.location or similar)
        module = self.request.node.module.__name__
        test_name = self.request.node.name
        return "{}__{}".format(module, test_name)

    def get(self, key=None, default=None):
        filename = self.test_key() if key is None else key
        try:
            return self.read(filename)
        except IOError:
            # Let's suppose it is a " IOError: [Errno 2] No such file or directory"
            if self.opt_create and default is not None:
                self.create(filename, default)
            return default

    def compare(self, expected, key=None):
        value = self.get(key, default=None)
        ret = value == expected

        if not ret and self.opt_create:
            filename = self.test_key() if key is None else key
            self.create(filename, expected)
            ret = True

        return ret


@pytest.fixture
def ref_path():
    return os.path.join(tempfile.gettempdir(), "pytest_ref")


@pytest.fixture
def ref_serialize():
    return lambda x: x


@pytest.fixture
def ref_unserialize():
    return lambda x: x


@pytest.fixture
def ref(request, ref_path, ref_serialize, ref_unserialize):
    return ReferenceRetriever(request, ref_path, ref_serialize, ref_unserialize)
