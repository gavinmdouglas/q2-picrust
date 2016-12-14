from setuptools import setup, find_packages
import re
import ast

# version parsing from __init__ pulled from Flask's setup.py
# https://github.com/mitsuhiko/flask/blob/master/setup.py
_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('q2_picrust/__init__.py', 'rb') as f:
    hit = _version_re.search(f.read().decode('utf-8')).group(1)
    version = str(ast.literal_eval(hit))

setup(
    name="q2-picrust",
    version=version,
    packages=find_packages(),
    # pandas, q2templates and q2-dummy-types are only required for the dummy
    # methods and visualizers provided as examples. Remove these dependencies
    # when you're ready to develop your plugin, and add your own dependencies
    # (if there are any).
    install_requires=['qiime >= 2.0.6',  'q2-types >= 0.0.6',
                      'biom-format >= 2.1.5, < 2.2.0'],
    author="Gavin Douglas",
    author_email="gavin.douglas@dal.ca",
    description="Plugin to run PICRUSt in QIIME 2 environment",
    entry_points={
        "qiime.plugins":
        ["q2-picrust=q2_picrust.plugin_setup:plugin"]
    },
    # If you are creating a visualizer, all template assets must be included in
    # the package source, if you are not using q2templates this can be removed
    package_data={
        "q2_picrust": ["assets/index.html"]
    }
)
