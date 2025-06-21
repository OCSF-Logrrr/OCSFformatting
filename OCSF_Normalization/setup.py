# setup.py

from setuptools import setup, Extension
from Cython.Build import cythonize

extensions = [
    Extension("app.classifier", ["app/classifier.pyx"])
]

setup(
    name="classifier",
    ext_modules=cythonize(
        extensions,
        compiler_directives={"language_level": "3"},
    ),
    zip_safe=False,
)
