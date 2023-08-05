# --  preambule ------------------------------------------------------------
import os
from distutils.core import setup
from setuptools import find_packages	
	
# -- settings & data -------------------------------------------------------

project_var_name = "tnmk_ensae"
readme = 'README.md'	

KEYWORDS = project_var_name + ', TABSOBA_NGARBAYE_MBIA_KONDO'
DESCRIPTION = """Un module graphique pour la visualisation"""
CLASSIFIERS = ['Programming Language :: Python :: 3',
	       'Topic :: Scientific/Engineering :: Visualization',
	       'Topic :: Software Development :: Libraries :: Python Modules',
	       'Topic :: Education',
	       'License :: OSI Approved :: MIT License'
			   ]

here = os.path.dirname(__file__)
packages = find_packages()	
package_dir = {k: os.path.join(here, k.replace(".", "/")) for k in packages}	   


# -- common part ------------------------------------------------------------

with open(readme, "r") as fh:
    descriptif_long = fh.read()

setup(
    name=project_var_name,
    version="1.0",
    author="TABSOBA_NGARBAYE_MBIA_KONDO",
    author_email='ngarbaye.54@gmail.com',
    license="MIT",
    description=DESCRIPTION,
    long_description=descriptif_long,
    long_description_content_type="text/markdown",
    packages=packages,
    package_dir=package_dir,
    classifiers=CLASSIFIERS,
    python_requires='>=3.7')

# -- end file ---------------------------------------------------------------