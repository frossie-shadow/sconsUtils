#
# A simple python interface to git, using os.popen
# Based on the svn interface.
#
# If ever we want to do anything clever, we should use one of
# the supported python packages
#
from __future__ import absolute_import, division, print_function
import os
from .. import state
from .. import utils


def guessVersionName():
    """Guess a version name"""

    if not os.path.exists(".git"):
        state.log.warn("Cannot guess version without .git directory; version will be set to 'unknown'.")
        return "unknown"
    status = utils.runExternal("git status --porcelain --untracked-files=no", fatal=True)
    if status.strip():
        raise RuntimeError("Error with git version: uncommitted changes")
    desc = utils.runExternal("git describe --tags --always", fatal=True)
    return desc.strip()


def guessFingerprint():
    """Return (fingerprint, modified) where fingerprint is the repository's SHA1"""
    fingerprint, modified = "0x0", False

    if not os.path.exists(".git"):
        state.log.warn("Cannot guess fingerprint without .git directory; will be set to '%s'."
                       % fingerprint)
    else:
        status = utils.runExternal("git status --porcelain --untracked-files=no", fatal=True)
        if status.strip():
            modified = True
        output = utils.runExternal("git rev-parse HEAD", fatal=False)

        fingerprint = output.strip()

    return fingerprint, modified
