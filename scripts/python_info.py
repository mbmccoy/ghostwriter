#!/usr/bin/env python3
import argparse

import distutils.sysconfig as du_sysconfig
import itertools
import os
import platform
import sys
import sysconfig


def get_python_library(python_version):
    """Get path to the python library associated with the current python
    interpreter."""
    # From skbuild source code

    # determine direct path to libpython
    python_library = sysconfig.get_config_var('LIBRARY')

    # if static (or nonexistent), try to find a suitable dynamic libpython
    if (not python_library or
            os.path.splitext(python_library)[1][-2:] == '.a'):

        candidate_lib_prefixes = ['', 'lib']

        candidate_implementations = ['python']
        if hasattr(sys, "pypy_version_info"):
            candidate_implementations = ['pypy-c', 'pypy3-c']

        candidate_extensions = ['.lib', '.so', '.a']
        if sysconfig.get_config_var('WITH_DYLD'):
            candidate_extensions.insert(0, '.dylib')

        candidate_versions = [python_version]
        if python_version:
            candidate_versions.append('')
            candidate_versions.insert(
                0, "".join(python_version.split(".")[:2]))

        abiflags = getattr(sys, 'abiflags', '')
        candidate_abiflags = [abiflags]
        if abiflags:
            candidate_abiflags.append('')

        # Ensure the value injected by virtualenv is
        # returned on windows.
        # Because calling `sysconfig.get_config_var('multiarchsubdir')`
        # returns an empty string on Linux, `du_sysconfig` is only used to
        # get the value of `LIBDIR`.
        libdir = du_sysconfig.get_config_var('LIBDIR')
        if sysconfig.get_config_var('MULTIARCH'):
            masd = sysconfig.get_config_var('multiarchsubdir')
            if masd:
                if masd.startswith(os.sep):
                    masd = masd[len(os.sep):]
                libdir = os.path.join(libdir, masd)

        if libdir is None:
            libdir = os.path.abspath(os.path.join(
                sysconfig.get_config_var('LIBDEST'), "..", "libs"))

        candidates = (
            os.path.join(
                libdir,
                ''.join((pre, impl, ver, abi, ext))
            )
            for (pre, impl, ext, ver, abi) in itertools.product(
            candidate_lib_prefixes,
            candidate_implementations,
            candidate_extensions,
            candidate_versions,
            candidate_abiflags
        )
        )

        for candidate in candidates:
            if os.path.exists(candidate):
                # we found a (likely alternate) libpython
                python_library = candidate
                break

        return python_library


def is_raspberry_pi():
    """Is this a raspberry pi?"""
    return "raspberrypi" in platform.uname()


def is_m1_mac():
    """Is this an M1 mac?"""
    return "RELEASE_ARM64" in platform.version()


def get_platform():
    """Print the platform."""
    return platform.uname()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Get basic information about python.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--library",
        action="store_true",
        help="The library file (e.g., libpython3.6m.a)",
    )
    group.add_argument(
        "--version",
        action="store_true",
        help="The python version (e.g., 3.6)",
    )
    group.add_argument(
        "--raspberry-pi",
        action="store_true",
        help="Is this a raspberry pi?",
    )
    group.add_argument(
        "--m1-mac",
        action="store_true",
        help="Is this an M1 Macbook?",
    )
    group.add_argument(
        "--platform",
        action="store_true",
        help="Print platform information.",
    )
    args = parser.parse_args()

    version_str = "{}.{}".format(*sys.version_info[:2])
    if args.version:
        print(version_str)
    if args.library:
        print(get_python_library(python_version=version_str))
    if args.raspberry_pi:
        print(is_raspberry_pi())
    if args.m1_mac:
        print(is_m1_mac())
    if args.platform:
        print(get_platform())
