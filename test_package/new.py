import path
import sys
import os
directory = path.Path(__file__).abspath()
sys.path.append(directory.parent.parent)
print(directory.parent.parent)

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)+'\model'
sys.path.append(parent+'/model')
import config
print(parent)