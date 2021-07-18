#!/usr/bin/env python3

####################################\
#       Omega LaunchServices        #
#   From the Omega Platform, v0.1   #
####################################/

from subprocess import Popen
from os import path

import time
import yaml
import sys
import os
import re


HOME = os.getenv("HOME")
_lang = os.getenv("LANG")

if not _lang:
    _lang = "en"
LANG = _lang.split("_")[0].lower()
COUNTRY = _lang.split("_")[1].split(".")[0].upper()
subprocesses = []

class AppBundle():
    def __init__(self, location, record=True):
        self.location = location
        self.loadApp(record)
    
    def loadApp(self, record=True):
        d = self.location
        if not path.exists(d): # if it doesn't exists then try adding .app
            d += ".app"
            if not path.exists(d): # if it still doesn't exist then something bad has happened
                self.app = {}
                self.entries = []
                return
        y = d+"/manifest.yml" # Try the two YAML extensions, then JSON
        if not path.exists(y):
            y = d+"/manifest.yaml"
            if not path.exists(y):
                y = d + "/manifest.json"
                if not path.exists(y):
                    y = d+"/Contents/manifest.yml" # Try in /Contents too, the OS X place
                    if not path.exists(y):
                        y = d+"/Contents/manifest.yaml"
                        if not path.exists(y):
                            y = d + "/Contents/manifest.json"
                            if not path.exists(y):
                                return
        with open(y) as mF:
            mC = mF.read()
        entries = yaml.load_all(mC)
        self.entries = entries
        self.app = entries[0]
        lc = LocationCache()
        if record:
            for e in entries:
                e['location'] = self.location
                lc.addApp(e)
        lc.saveCache()
        return [entries,record]
    
    def infoDump(self):
        print(yaml.dump(self.entries))
    
    def execApp(self, args=[]):
        if not 'exec' in self.app.keys():
            print("Warning: '" + self.location + "' is not an executable app bundle.")
            return
        e = self.app['exec']
        places = ([self.location + "/" + e, self.location + "/Resources/" + e,
                  self.location + "/MacOS/" + e, self.location + "/Contents/" + e,
                  self.location + "/Contents/MacOS/" + e,
                  self.location + "/Contents/Resources/" + e] +
                  [i + "/" + e for i in os.getenv("PATH").split(":")] + [e]) # plain e is supported for compatibility
        for place in places:
            if os.path.exists(place):
                e = place
                break
        else:
            print("Error: '"+e+"' not found in app bundle or $PATH.")
            return
        argv = [e] + args
        subprocesses.append(Popen(argv))

class LocationCache():
    def __init__(self):
        if path.exists(HOME + "/.cache/omega/appcache"):
            with open(HOME + "/.cache/omega/appcache") as apF:
                ap = apF.read()
            try:
                appcache = yaml.load(ap)
            except Exception as e:
                print(e)
                appcache = {"apps": []}
        else:
            appcache = {"apps": []}
        try:
            apps = list(appcache['apps'])
        except Exception as e:
            print(e)
            apps = []
        foundapps = []
        for app in apps:
            location = app["location"] # the last known location
            if path.exists(location):
                foundapps.append(app) # if the app doesn't exist anymore then screw it
            else:
                continue
        self.apps = foundapps
    
    def retrieveFromName(self, name):
        foundapps = []
        for app in self.apps:
            if app["name"] == name:
                foundapps.append(app)
        latestapp = {}
        revision = -1
        # When retrieving an app by its name, pick the latest one.
        for app in foundapps:
            if int(app["revision"]) > revision:
                latestapp = app
                revision = int(app['revision'])
        return latestapp
    
    def searchApps(self, pattern="*"):
        foundapps = []
        pat = re.compile(pattern)
        for app in self.apps:
            if "name_"+LANG in app:
                name = app["name_"+LANG]
            elif "name" in app:
                name = app["name"]
            else:
                continue
            if pat.match(name):
                foundapps.append(app)
        return foundapps
    
    def addApp(self, app):
        if app not in self.apps: # ignore if it's already there
            self.apps.append(app)
    
    def saveCache(self):
        appcache = {"apps": self.apps, "formatRevision":0}
        with open(HOME + "/.cache/omega/appcache", 'w') as pF:
            pF.write(yaml.dump(appcache))

__all__ = ['tidyUp', 'LocationCache', 'AppBundle']

def tidyUp():
    while len(subprocesses):
        for p in subprocesses:
            if p.poll() is not None:
                del p
        time.sleep(1)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("""
launch: launch an OsloOS app bundle

Synopsis:

    launch APP ARGUMENT…
        Launch an app bundle with arguments forwarded to the process
    
    launch --search PATTERN
        Search for a regular expression pattern in the applications database.
        This uses the extended regular expression format, so if you want to
        search for a particular term or set of terms, such as 'text editor' and
        have apps with either text or editor come up, you need to use
        '(.*|)(text|editor)(.*|)'.

    launch --help
        Print this help text

    launch --info APP
        Print information about an app bundle
""")
        sys.exit(1)
    a = sys.argv[1:]
    if a[0] == "--search":
        if len(a) == 1:
            print("Missing argument for --launch. Try running with --help.")
            sys.exit(1)
        lc = LocationCache()
        p = ""
        for arg in a[1:]:
            if p == "":
                p = arg
            else:
                p += " " + arg
        results = lc.searchApps(p)
        for app in results:
            print()
            print("=" * 80)
            if "location" in app:
                print("App bundle at "+app['location']+":")
            else:
                print("App bundle (location unknown):")
            print()
            print(yaml.dump(app, default_flow_style=False))
        if len(results) == 0:
            print("No results found :~(")
        sys.exit(0)
    elif a[0] == "--help":
        print("""
launch: launch an OsloOS app bundle

Synopsis:

    launch APP ARGUMENT…
        Launch an app bundle with arguments forwarded to the process

    launch --search PATTERN
        Search for a regular expression pattern in the applications database.
        This uses the extended regular expression format, so if you want to
        search for a particular term or set of terms, such as 'text editor' and
        have apps with either text or editor come up, you need to use
        '(.*|)(text|editor)(.*|)'.

    launch --help
        Print this help text

    launch --info APP
        Print information about an app bundle
""")
        sys.exit(0)
    elif a[0] == "--info":
        if len(a) == 1:
            print("Missing argument for --info. Try running with --help.")
            sys.exit(1)
        for app in a[1:]:
            AppBundle(app).infoDump()
        sys.exit(0)
        
    AppBundle(a[0]).execApp(a[1:] if len(a) > 1 else [])
