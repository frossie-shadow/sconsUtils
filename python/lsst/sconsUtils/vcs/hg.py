#
# A simple python interface to hg (Mercurial), using os.popen
# Based on the svn interface.
#
# If ever we want to do anything clever, we should use one of
# the supported svn/python packages
#
import os, re


#
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
#
def guessVersionName():
    """Guess a version name"""
    idents = os.popen("hg id").readline()
    ident = re.split(r"\s+", idents)
    if re.search(r"\+", ident[0]):
        raise RuntimeError("Error with hg version: uncommitted changes")

    # Prefer tag name to branch name; branch names get printed in parens
    index = 1
    while ident[index].startswith('(') and ident[index].endswith(')') and len(ident) > index + 1:
        index += 1

    # Prefer hash to "tip"
    if ident[index] == "tip":
        return ident[0]

    return ident[index]
