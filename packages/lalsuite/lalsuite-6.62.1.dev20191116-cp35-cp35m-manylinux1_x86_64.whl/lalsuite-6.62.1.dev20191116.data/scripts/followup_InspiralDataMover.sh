#!python
import os, pkg_resources, sys
os.execv(pkg_resources.resource_filename('lalapps', 'bin/followup_InspiralDataMover.sh'), sys.argv)
