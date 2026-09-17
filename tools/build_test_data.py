#! /usr/bin/env python
#
# Copyright 2024 University of Calgary
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
This script builds the test data that the test suite reads from disk, into
tests/test_data. It is what 'make get-test-data' runs.

The test suite reads its files out of tests/test_data/data/ucalgary/read, with one
sub-directory per reader. Every file in there is downloaded verbatim from the open
data platform:

  1) SWAN_HSR_FILES --> read_swan_hsr, the HDF5 files that read_swan_hsr() is pointed at.

  2) RIOMETER_K0_FILES --> read_norstar_riometer, the text files that
     read_norstar_riometer() is pointed at.

Usage:

  python3 tools/build_test_data.py [--clean]

Files that are already in place are left alone, so an interrupted build only fetches
what it missed. Pass --tarball to also package the tree up, for hosting it somewhere
or handing it to someone.
"""

import argparse
import os
import shutil
import subprocess  # nosec
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor

# globals
DATA_TREE = "https://data.phys.ucalgary.ca/sort_by_project"
TARBALL_FILENAME = "pyucrio_test_data.tar.gz"
DEFAULT_DATA_DIR = "%s/tests/test_data" % (os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

# the part of the tree that the test suite points its readers at, relative to the data dir
READ_DIR = "data/ucalgary/read"

# SWAN HSR data: <data tree>/<path>/<yyyy>/<mm>/<dd>/<filename>
SWAN_HSR_FILES_PATH = "SWAN/hsr/l0/multi_freq/h5"
SWAN_HSR_FILES = [
    "20240203_mean-hsr_k0_v01.h5",
]

# riometer data (k0): <data tree>/<path>/<yyyy>/<mm>/<dd>/<filename>
RIOMETER_K0_FILES_PATH = "GO-Canada/GO-Rio/txt"
RIOMETER_K0_FILES = [
    "norstar_k0_rio-fsim_20180503_v01.txt",
]


def build_archive_manifest():
    """
    Work out the URL of every file that gets downloaded from the open data platform,
    returned as a dictionary of destination path in the test data tree --> URL.
    """
    manifest = {}

    # SWAN HSR data
    #
    # NOTE: the date is the first underscore-delimited part of the filename
    for filename in SWAN_HSR_FILES:
        date_str = filename.split('_')[0]
        manifest["%s/read_swan_hsr/%s" % (READ_DIR, filename)] = "%s/%s/%s/%s/%s/%s" % (DATA_TREE, SWAN_HSR_FILES_PATH, date_str[0:4],
                                                                                        date_str[4:6], date_str[6:8], filename)

    # riometer data
    #
    # NOTE: the date is the second-last underscore-delimited part of the filename, for both
    # the current and the historical filenaming
    for filename in RIOMETER_K0_FILES:
        date_str = filename.split('_')[-2]
        manifest["%s/read_norstar_riometer/%s" % (READ_DIR, filename)] = "%s/%s/%s/%s/%s/%s" % (DATA_TREE, RIOMETER_K0_FILES_PATH, date_str[0:4],
                                                                                                date_str[4:6], date_str[6:8], filename)

    return manifest


def download_file(url, output_filename):
    if (os.path.exists(output_filename) and os.path.getsize(output_filename) > 0):
        return 0
    os.makedirs(os.path.dirname(output_filename), exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "pyucrio test data builder"})
    with urllib.request.urlopen(req, timeout=300) as r:  # nosec
        content_type = r.headers.get("Content-Type", "")
        data = r.read()

    # the data server redirects to the home page for files that don't exist, so a
    # page of HTML means we asked for something that isn't there
    if ("text/html" in content_type.lower()):
        raise IOError("Received a page of HTML instead of a file, the URL is likely no longer valid: %s" % (url))
    with open(output_filename, "wb") as fp:
        fp.write(data)
    return len(data)


def download_archive_files(data_dir, n_parallel):

    def do_download(item):
        dest, url = item
        try:
            return (dest, download_file(url, "%s/%s" % (data_dir, dest)), None)
        except Exception as e:
            return (dest, 0, str(e))

    archive_manifest = build_archive_manifest()
    print("[downloading] %d files from the open data platform" % (len(archive_manifest)))
    with ThreadPoolExecutor(max_workers=n_parallel) as executor:
        results = list(executor.map(do_download, sorted(archive_manifest.items())))
    failures = [r for r in results if r[2] is not None]
    for f in failures:
        print("  failed: %s (%s)" % (f[0], f[2]))
    if (len(failures) > 0):
        raise IOError("Failed to download %d file(s)" % (len(failures)))
    print("[downloading] retrieved %.1f MB" % (sum(r[1] for r in results) / 1e6))


def set_permissions(data_dir):
    for root, _, files in os.walk(data_dir):
        for f in files:
            os.chmod(os.path.join(root, f), 0o644)


def create_tarball(data_dir):
    output_dir = os.path.dirname(data_dir)
    tarball_filename = "%s/%s" % (output_dir, TARBALL_FILENAME)
    print("[packaging] creating %s" % (tarball_filename))
    if (os.path.exists(tarball_filename)):
        os.remove(tarball_filename)
    subprocess.run(  # nosec
        ["tar", "-C", output_dir, "-czf", tarball_filename,
         os.path.basename(data_dir)],
        check=True,
    )
    return tarball_filename


def clean_data_dir(data_dir):
    print("[cleaning] removing the existing test data")
    shutil.rmtree("%s/%s" % (data_dir, READ_DIR.split('/')[0]), ignore_errors=True)


def main():
    # args
    parser = argparse.ArgumentParser(description="Build the test data that the test suite reads")
    parser.add_argument("--data-dir", default=DEFAULT_DATA_DIR, help="Directory to build the test data tree in (default: %s)" % (DEFAULT_DATA_DIR))
    parser.add_argument("--n-parallel", type=int, default=5, help="Number of parallel downloads (default: 5)")
    parser.add_argument("--clean", action="store_true", help="Remove the existing test data before building")
    parser.add_argument("--tarball", action="store_true", help="Also package the tree up as %s, beside the data directory" % (TARBALL_FILENAME))
    args = parser.parse_args()

    # set up paths
    data_dir = os.path.abspath(os.path.expanduser(args.data_dir))
    os.makedirs(data_dir, exist_ok=True)

    # build it
    #
    # NOTE: files that are already there are left alone, so an interrupted build only has
    # to fetch what it didn't get to the first time
    if (args.clean is True):
        clean_data_dir(data_dir)
    download_archive_files(data_dir, args.n_parallel)
    set_permissions(data_dir)
    print("\nDone, the test data is in %s" % (data_dir))

    # package it up, if we were asked to
    if (args.tarball is True):
        tarball_filename = create_tarball(data_dir)
        print("Packaged %s (%.1f MB)" % (tarball_filename, os.path.getsize(tarball_filename) / 1e6))
    return 0


if (__name__ == "__main__"):
    sys.exit(main())
