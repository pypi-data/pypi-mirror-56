#!-*-coding:utf-8-*-
import os
import sys

sys.path.append("../")
from  ..lib import file as fl
from  ..lib import message as ms

def mkdir( path ):
    if not os.path.exists( path ):
        ms.message( str( path ) + "Created" )
        os.makedirs( path )
