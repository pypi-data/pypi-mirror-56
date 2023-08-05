# OXO

A naughts & crosses game.

# Install

Currently this is installable as a python package to be ran in the Python3 repl.

To install run command:

`python3 -m pip install --user --upgrade oxo_pkg` (not yet available, use TestPyPi)

if installing from [TestPyPi](https://test.pypi.org/project/oxo-pkg/) run:

`python3 -m pip install --user --index-url https://test.pypi.org/simple/ oxo_pkg`

# Run

Open the python3 repl:-

`python3`

import and run the package:-

\>`import oxo_pkg`

\>`oxo_pkg.run()`

# Build

`python3 -m pip install --user --upgrade setuptools wheel` (install / update wheel & setuptools)

`python3 setup.py sdist bdist_wheel`

Produces a .whl built distribution & a tar file of the source code in `dist/` directory.

# Release

Increment release number in `setup.py` file.

Build a new release with steps above.

`python3 -m pip install --user --upgrade twine` (install / update twine)

`python3 -m twine upload dist/*` 

To upload to [TestPyPi](https://test.pypi.org/project/oxo-pkg/) run:

`python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*` 