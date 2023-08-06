import pkg_resources
from pkg_resources import parse_version, get_distribution
import re

def getQuarchPyVersion ():
    return pkg_resources.get_distribution("quarchpy").version

def requiredQuarchpyVersion (requiredVersion):
    currentVersion =getQuarchPyVersion ()
    requiredVersion=requiredVersion.split(".")
    currentVersion =currentVersion.split(".")

    i = 0
    for x in requiredVersion:
        requiredVersion[i] = int(x)
        i+=1
    i= 0
    for x in currentVersion:
        currentVersion[i] = int(x)
        i+=1

    if currentVersion[0] < requiredVersion[0]:
        raise ValueError("Current quarchpy version " + str(currentVersion) + " is not high enough, upgrade to " + str(
            requiredVersion) + " or above.")
        return False
    elif currentVersion[0] > requiredVersion[0]:
        return True
    else:
        if currentVersion[1] < requiredVersion[1]:
            raise ValueError(
                "Current quarchpy version " + str(currentVersion) + " is not high enough, upgrade to " + str(
                    requiredVersion) + " or above.")
            return False
        elif currentVersion[1] > requiredVersion[1]:
            return True
        else:
            if currentVersion[2] < requiredVersion[2]:
                raise ValueError(
                    "Current quarchpy version " + str(currentVersion) + " is not high enough, upgrade to " + str(
                        requiredVersion) + " or above.")
                return False
            elif currentVersion[2] > requiredVersion[2]:
                return True
            else: return True