setuptools_pkg
==============

Plugin for setuptools that provides `bdist_pkg` command for building FreeBSD
package artifact.

How to use?
-----------

Simply add `setuptools-pkg` to `setup_requires` in your setup.py:

.. code:: python

    setup(
        name="myproject",
        version="1.0.0",
        ...
        setup_requires=["setuptools-pkg"]
    )

Once it's done, the `setup.py bdist_pkg` command will be available to produce
`dist/myproject-1.0.0.txz` artifact.

If you don't want or just cannot have build-time dependencies, same effect can
be reached by installing `setuptools-pkg` as regular Python package.
