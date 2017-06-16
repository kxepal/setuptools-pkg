setuptools_pkg
==============

Plugin for setuptools that provides `bdist_pkg` command for building FreeBSD
package artifact.

How to use?
-----------

Simply add ``setuptools-pkg`` to ``setup_requires`` in your `setup.py`:

.. code-block:: python

    setup(
        name="myproject",
        version="1.0.0",
        ...
        setup_requires=["setuptools-pkg"]
    )

Once it's done, the ``setup.py bdist_pkg`` command will be available to produce
``dist/myproject-1.0.0.tgz`` artifact.

If you don't want or just cannot have build-time dependencies, same effect can
be reached by installing `setuptools-pkg` as regular Python package.

If you need to build (actually, you want) ``txz`` packages and you're using
Python 2, you should specify ``lzma-2.7`` extra to have lzma support.
For Python 3 there is no need in this since it's available out-of-the box.

Advanced usage
--------------

Ok, that was too easy. In real world, things are not as easy as we would like
to have them.

Each project has dependencies, unless it's lucky one. For packages we would
like to preserve that information, but suddenly, packages in FreeBSD may be
named differently from PyPI or be of the different version because of included
patches. That's said, we need the mapping between them. Let's pick this project
as an example:

.. code-block:: python

    setup(
        ...,
        # Typically, our dependencies looks like this:
        install_requires=[
            'setuptools>=18.2',
        ],
        extras_require={
            'lzma-2.7': [
                'backports.lzma==0.0.6',
            ],
        },
        # The `command_options` is the way to specify parameters for setuptools
        # commands from the `setup()` call. Alternatively, you can do that in
        # `setup.cfg`.
        command_options={
            # bdist_pkg is the name of command setuptools_pkg provides
            'bdist_pkg': {
                # The requirements mapping itself. The __file__ instructs
                # setuptools from where these values came from. Required.
                # The rest is our mapping.
                'requirements_mapping': (__file__, {
                    # The key of this mapping is an exact value of a requires
                    # list.
                    'setuptools>=18.2': {
                        # The value is a FreeBSD pkg metadata: package name,
                        # origin and version.
                        'name': 'py27-setuptools',
                        'origin': 'devel/py-setuptools',
                        # In our example setuptools>=18.2 tells us to pick
                        # any version of setuptools greater than 18.2 and we
                        # explicitly picks package with strict version 20.0.
                        #
                        # Please note, that version field is required while
                        # it's not in MANIFEST file.
                        'version': '20.0'
                    },
                    # Mapping for extras is optional till the moment you
                    # want to make a package with these extras on.
                    'backports.lzma==0.0.6': {
                        'name': 'py27-backports_lzma',
                        'origin': 'devel/py-backports_lzma',
                        'version': '0.0.6'
                    }
                }),
                # bdist_pkg turns all the extras into options and through
                # selected options you can choose which ones will be enabled 
                # for a package. By default all the options are in "off" state.
                'selected_options': [
                    'lzma-2.7',
                ]
            }
        }
    )

Common pitfalls here:

1. Requirements mapping is not portable. In your pkg repository there could be
   different versions and different package namings.
2. Requirements mapping should be up to date.
3. There is no checks that mapping items are correct. You should pay attention
   to what you put there.
4. Having `requirements.txt` instead of using ``install_requires`` in
   `setup.py`  will make your life harder since, technically, your project
   has no dependencies and we cannot help you there to keep it consistent.
   You'll have to specify ``deps`` command property directly and `bdist_pkg`
   could not ensure that you have there all the packages that project actually
   uses.

That's could be found quite boring. However, if all your dependencies in pkg
repository are names same as on PyPI and has Python version prefix (like
``py35-setuptools``), than requirements mapping is optional. You can just make
package with:

.. code-block:: bash

    python setup.py bdist_pkg --use-pypi-deps

Expert usage
------------

In expert mode you may configure package generation in the way you like.
Here is the complete list of options you may specify for `bdist_pkg`:

- ``abi`` and ``arch``: FreeBSD arch and ABI for which package is made. You must
  specify them manually if you build package on non-FreeBSD system or if you
  distribution is not pure.

- ``categories``: A list (literally) of package categories.
  By default uses ``description`` field of project metadata.

- ``comment``: Comment is a one-line description of this package.
  By default uses ``description`` field of project metadata.

- ``deps``: Package dependencies. Sometimes package may depend on non Python
  projects, like those who provides services or libraries against which
  your projects dynamically links. The format of deps specification is
  the same as in `+MANIFEST` file, except it's Python dict, not JSON or UCL.
  For Python dependencies check the ``requirements_mapping`` below.

- ``desc``: A longer description of the package.
  By default uses ``long_description`` field of project metadata.

- ``groups``: A list of groups to provide.

- ``license``: Project license.
  By default uses ``license`` field of project metadata.

- ``maintainer``: The maintainer's mail address. Python distributions defines
  both maintainer and author entities who rules the package. By default,
  the maintainer one is picked if available with fallback to author in case
  when it's not.

- ``name``: Package name. Since FreeBSD packages often uses own naming policy,
  the custom name can be used instead of real project one.

- ``options``: Package options. By default, this list is filled from the extras.

- ``selected_options``: List of options which are used for this package build.

- ``origin``: By default the generic origin ``devel/py-{project_name}`` is set.

- ``prefix``:  The path where the files contained in this package are installed
  (usually ``/usr/local``).

- ``provides``: A list of features/services packages provides.

- ``requires``: A list of features/services packages paquires.

- ``requirements_mapping``: Mapping between PyPI requirements and FreeBSD
  packages. This mapping helps to ensure that all the dependencies specified
  in ``install_requires`` and ``extras_require`` will be satisfied through
  system packages. The result fills the ``deps`` option.

- ``scripts``: `Package scripts <https://wiki.freebsd.org/pkgng#Scripts>`_.

- ``users``: A list of users to provide.

- ``version``: Package version. As like package name, can be different from
  real project version, depending on local modifications, patches, epoch etc.

- ``www``: Project URL.


FAQ
---

- **How it's different from pytoport?**

  The `pytoport`_ project generates *ports* from modules on *PyPI*.
  It does great job on this, but ``bdist_pkg`` solves a different problem,
  especially, when your project cannot be published on PyPI.

- **How can I make a package for some arbitrary Python project?**

  You have to patch it first to let him produce proper package with the deps,
  metadata and else bits. But seriously, you better use ports all the time.

- **If I should use ports to make packages, why this project exists?**

  In my case we have a couple of in-house projects which we package directly
  without using any ports or cooking Makefiles.

.. _pytoport: https://github.com/freebsd/pytoport/
