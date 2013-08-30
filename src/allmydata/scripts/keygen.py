from __future__ import print_function

import os, sys
from allmydata.scripts.common import BasedirOptions
from allmydata.util.assertutil import precondition
from allmydata.util.encodingutil import listdir_unicode, quote_output

class CreateKeyGeneratorOptions(BasedirOptions):
    default_nodedir = None

    def getSynopsis(self):
        return "Usage:  %s [global-opts] create-key-generator [options] NODEDIR" % (self.command_name,)


keygen_tac = """
# -*- python -*-

import pkg_resources
pkg_resources.require('allmydata-tahoe')

from allmydata import key_generator
from twisted.application import service

k = key_generator.KeyGeneratorService(default_key_size=2048)
#k.key_generator.verbose = False
#k.key_generator.pool_size = 16
#k.key_generator.pool_refresh_delay = 6

application = service.Application("allmydata_key_generator")
k.setServiceParent(application)
"""

def create_key_generator(config, out=sys.stdout, err=sys.stderr):
    basedir = config['basedir']
    # This should always be called with an absolute Unicode basedir.
    precondition(isinstance(basedir, unicode), basedir)

    if os.path.exists(basedir):
        if listdir_unicode(basedir):
            print("The base directory %s is not empty." % quote_output(basedir), file=err)
            print("To avoid clobbering anything, I am going to quit now.", file=err)
            print("Please use a different directory, or empty this one.", file=err)
            return -1
        # we're willing to use an empty directory
    else:
        os.mkdir(basedir)
    f = open(os.path.join(basedir, "tahoe-key-generator.tac"), "wb")
    f.write(keygen_tac)
    f.close()
    return 0

subCommands = [
    ["create-key-generator", None, CreateKeyGeneratorOptions, "Create a key generator service."],
]

dispatch = {
    "create-key-generator": create_key_generator,
    }

