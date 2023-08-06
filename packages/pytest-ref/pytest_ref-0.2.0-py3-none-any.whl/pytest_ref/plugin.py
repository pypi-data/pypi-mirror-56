# -*- coding: utf-8 -*-

# Make fixtures available
from .fixtures import ref_path, ref, ref_serialize, ref_unserialize  # noqa


def pytest_addoption(parser):
    group = parser.getgroup("ref")

    group.addoption(
        "--create",
        action="store_true",
        dest="ref_create",
        default=False,
        help="Should the references files be created when missing",
    )

    group.addoption(
        "--update",
        action="store_true",
        dest="ref_update",
        default=False,
        help="Should the references files be updated when different or missing",
    )
