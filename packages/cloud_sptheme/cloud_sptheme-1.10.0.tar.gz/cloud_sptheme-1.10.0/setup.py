"""
cloud_sptheme setup script
"""
#=============================================================================
# init script env -- ensure cwd = root of source dir
#=============================================================================
import os
root_dir = os.path.abspath(os.path.join(__file__, ".."))
os.chdir(root_dir)

#=============================================================================
# imports
#=============================================================================
# core
import setuptools
import sys
# pkg
from cloud_sptheme import _iter_theme_sources
from cloud_sptheme import __version__ as version

#=============================================================================
# init setup options
#=============================================================================
opts = dict(
    #==================================================================
    # sources
    #==================================================================
    packages=setuptools.find_packages(root_dir),
    package_data={
        "cloud_sptheme": ["themes/*/*.*", "themes/*/static/*.*", "ext/static/*.*"]
    },
    zip_safe=False,

    #==================================================================
    # metadata
    #==================================================================
    name="cloud_sptheme",
    # NOTE: 'version' set below
    author="Eli Collins",
    author_email="elic@assurancetechnologies.com",
    license = "BSD",

    url = "https://bitbucket.org/ecollins/cloud_sptheme",
    download_url = "https://pypi.python.org/pypi/cloud_sptheme",

    install_requires=[
        "sphinx>=1.6"
    ],

    entry_points={
        # signal to sphinx it should call "cloud_sptheme:setup(app)" to setup these html themes
        "sphinx.html_themes": ['%s = cloud_sptheme' % name for name, path in _iter_theme_sources()]
    },

    #==================================================================
    # details
    #==================================================================
    description= 
    "a nice sphinx theme named 'Cloud', and some related extensions",

    long_description="""\
This is a small package containing a Sphinx theme named "Cloud",
along with some related Sphinx extensions. To see an example
of the theme in action, check out it's documentation
at `<https://cloud-sptheme.readthedocs.io>`_.
    """,

    keywords="sphinx extension theme",

    classifiers="""
Development Status :: 5 - Production/Stable
Framework :: Sphinx :: Extension
Framework :: Sphinx :: Theme
Intended Audience :: Developers
License :: OSI Approved :: BSD License
Operating System :: OS Independent
Programming Language :: Python :: 2.6
Programming Language :: Python :: 2.7
Programming Language :: Python :: 3
Programming Language :: Python :: 3.3
Programming Language :: Python :: 3.4
Programming Language :: Python :: 3.5
Programming Language :: Python :: 3.6
Programming Language :: Python :: 3.7
Programming Language :: Python :: 3.8
Topic :: Documentation
Topic :: Software Development :: Documentation
""".strip().splitlines(),

    #==================================================================
    # custom setup
    #==================================================================
    script_args=sys.argv[1:],
    cmdclass={},
)

#=============================================================================
# set version string
#=============================================================================

# append hg revision to builds
stamp_build = False
if stamp_build:
    from cloud_sptheme._setup.stamp import (
        as_bool, append_hg_revision, stamp_distutils_output,
        install_build_py_exclude, set_command_options
    )

    # add HG revision to end of version
    if as_bool(os.environ.get("SETUP_TAG_RELEASE", "yes")):
        version = append_hg_revision(version)

    # subclass build_py & sdist to rewrite source version string,
    # and clears stamp_build flag (above) so this doesn't run again.
    stamp_distutils_output(opts, version)

    # exclude '._setup' package from builds, only needed for sdist
    install_build_py_exclude(opts)
    set_command_options(opts, "build_py",
        exclude_packages=["cloud_sptheme._setup"],
    )

opts['version'] = version

#=============================================================================
# run setup
#=============================================================================
setuptools.setup(**opts)

#=============================================================================
# eof
#=============================================================================
