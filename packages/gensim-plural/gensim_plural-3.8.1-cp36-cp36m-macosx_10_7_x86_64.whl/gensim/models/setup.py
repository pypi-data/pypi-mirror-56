from Cython.Distutils import build_ext
from distutils.core import setup
from distutils.extension import Extension
import numpy

import os
os.environ['CC'] = 'g++'
os.environ['CXX'] = 'g++'

ext_modules = [
    Extension(
        name="doc2vec_corpusfile",
        sources=["doc2vec_corpusfile.pyx"],
        extra_compile_args=["-Wno-cpp", "-Wno-unused-function", "-O2", "-march=native", '-stdlib=libc++', '-std=c++11'],
        extra_link_args=["-O2", "-march=native", '-stdlib=libc++'],
        language="c++",
        include_dirs=[numpy.get_include()],
    ),
    Extension(
        name="doc2vec_inner",
        sources=["doc2vec_inner.pyx"],
        extra_compile_args=["-Wno-cpp", "-Wno-unused-function", "-O2", "-march=native", '-stdlib=libc++', '-std=c++11'],
        extra_link_args=["-O2", "-march=native", '-stdlib=libc++'],
        language="c++",
        include_dirs=[numpy.get_include()],
    )
]

setup(
    name="doc2vec_corpusfile", ext_modules=ext_modules, cmdclass={"build_ext": build_ext}
)
setup(
    name="doc2vec_inner", ext_modules=ext_modules, cmdclass={"build_ext": build_ext}
)