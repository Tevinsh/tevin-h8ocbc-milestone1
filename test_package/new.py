
import path
import sys
import os
directory = path.Path(__file__).abspath()
sys.path.append(directory.parent.parent)
print(directory.parent.parent)

current = os.getcwd()
parent = os.path.dirname(current)
sys.path.append(parent+'/model')
import config
print('current',current)

basedir = os.path.abspath(os.path.dirname(__file__))
print(basedir)