#!/usr/bin/env python3
'''
Created on 1 Dec 2017

@author: julianporter
'''
from setuptools import setup, Extension
from setuptools.config import read_configuration
import os
from collections import namedtuple
import numpy
import subprocess

def getPaths(libs):
    libDir=set()
    incDir=set()
    
    for lib in libs:
        out=subprocess.check_output(['pkg-config','--libs','--cflags',lib]).decode('utf8').split()
        for term in out:
            if term.startswith('-I'): incDir.add(term[2:])
            elif term.startswith('-L'): libDir.add(term[2:])
    return libDir, incDir
    


configuration=read_configuration('setup.cfg')
metadata=configuration['metadata']

def sourceFilesIn(folder,exclude=[]):
    try:
        items=os.listdir(folder)
        return [os.path.join(folder,item) for item in items if item.endswith('.cpp') and item not in exclude]
    except:
        return []

Version = namedtuple('Version',['major','minor','maintenance'])
def processVersion():
    version=metadata['version']
    parts=version.split('.')
    if len(parts)<3: parts.extend([0,0,0])
    return Version(*(parts[:3]))

includes=['/usr/local/include']
includes.append(f'{numpy.get_include()}/numpy')

def makeExtension(module,src):
    #print("Making {} with {}".format(module,src))
    
    v=processVersion()
    mv=f'"{v.major}.{v.minor}.{v.maintenance}"'
    return Extension(module,
                    define_macros = [('MAJOR_VERSION', v.major),
                                     ('MINOR_VERSION', v.minor),
                                     ('MAINTENANCE_VERSION', v.maintenance),
                                     ('MODULE_VERSION', mv)],
                    sources = src,
                    language = 'c++',
                    include_dirs=includes,
                    libraries = ['sndfile','rubberband'],
                    library_dirs = ['/usr/local/lib'],
                    extra_compile_args=['-std=c++17'])

src=[]
src.extend(sourceFilesIn('src'))
# src.extend(sourceFilesIn('pcm2mp3-cpp/src/id3',['main.cpp']))

coder = makeExtension('rubberband',src)

with open('README.rst') as readme:
    longDescription = readme.read()

setup (
    ext_modules = [coder],
    long_description = longDescription, 
)

