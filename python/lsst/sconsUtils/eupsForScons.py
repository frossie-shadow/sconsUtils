from __future__ import absolute_import, division, print_function
import os

try:
    from eups import *
    eupsLoaded = True
except ImportError:
    eupsLoaded = False


def haveEups():
    return eupsLoaded


if not haveEups():
    #
    # Fake what we can so sconsUtils can limp along without eups
    #
    def flavor():
        from .state import env, log

        log.warn("Unable to import eups; guessing flavor")

        if env['PLATFORM'] == "posix":
            return os.uname()[0].title()
        else:
            return env['PLATFORM'].title()

    def productDir(name):
        return os.environ.get("%s_DIR" % name.upper())

    def findSetupVersion(eupsProduct):
        return None, None, None, None, flavor()

    class _Eups(object):
        def __call__(self):
            return self
    Eups = _Eups()

    Eups.findSetupVersion = findSetupVersion

    class _Utils(object):
        pass
    utils = _Utils()

    def setupEnvNameFor(productName):
        return "SETUP_%s" % productName

    utils.setupEnvNameFor = setupEnvNameFor


def getEups():
    """ Return a cached Eups instance, auto-creating if necessary """
    try:
        return getEups._eups
    except AttributeError:
        getEups._eups = Eups()
        return getEups._eups
