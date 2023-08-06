# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['numpoly',
 'numpoly.array_function',
 'numpoly.construct',
 'numpoly.poly_function']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.16,<2.0']

setup_kwargs = {
    'name': 'numpoly',
    'version': '0.1.2',
    'description': 'Polynomials as a numpy datatype',
    'long_description': '.. image:: doc/.static/numpoly_logo.svg\n   :height: 300 px\n   :width: 300 px\n   :align: center\n\n|circleci| |codecov| |pypi| |readthedocs|\n\n.. |circleci| image:: https://circleci.com/gh/jonathf/numpoly/tree/master.svg?style=shield\n    :target: https://circleci.com/gh/jonathf/numpoly/tree/master\n.. |codecov| image:: https://codecov.io/gh/jonathf/numpoly/branch/master/graph/badge.svg\n    :target: https://codecov.io/gh/jonathf/numpoly\n.. |pypi| image:: https://badge.fury.io/py/numpoly.svg\n    :target: https://badge.fury.io/py/numpoly\n.. |readthedocs| image:: https://readthedocs.org/projects/numpoly/badge/?version=master\n    :target: http://numpoly.readthedocs.io/en/master/?badge=master\n\nNumpoly is a generic library for creating, manipulating polynomial arrays.\n\nMany numerical analysis, prominent in for example uncertainty quantification,\nuses polynomial approximations as proxy for real models to do analysis on.\nThese models are often solutions to non-linear problems discretized with high\nmesh. As such, the corresponding polynomial approximation consist of high\nnumber of dimensions and large multi-dimensional polynomial coefficients.\n\n``numpoly`` is a subclass of ``numpy.ndarray`` implemented to represent\npolynomials as array element. As such is fast and scales very well with the\nsize of the coefficients. It is also compatible with most ``numpy`` functions,\nwhere that makes sense, making the interface fairly intuitive. Some of the\ninterface is also inspired by the ``sympy`` interface.\n\n.. contents:: Table of Contents:\n\nInstallation\n------------\n\nInstallation should be straight forward:\n\n.. code-block:: bash\n\n    pip install numpoly\n\nAnd you should be ready to go.\n\nExample usage\n-------------\n\nConstructing polynomial is typically done using one of the available\nconstructors:\n\n.. code-block:: python\n\n   >>> numpoly.monomial(start=0, stop=3, indeterminants=("x", "y"))\n   polynomial([1, y, x, y**2, x*y, x**2, y**3, x*y**2, x**2*y, x**3])\n\nIt is also possible to construct your own from symbols:\n\n.. code-block:: python\n\n   >>> x, y = numpoly.symbols("x y")\n   >>> numpoly.polynomial([1, x**2-1, x*y, y**2-1])\n   polynomial([1, -1+x**2, x*y, -1+y**2])\n\nOr in combination with other numpy objects:\n\n.. code-block:: python\n\n   >>> x**numpy.arange(4)-y**numpy.arange(3, -1, -1)\n   polynomial([1-y**3, x-y**2, x**2-y, -1+x**3])\n\nThe polynomials can be evaluated as needed:\n\n.. code-block:: python\n\n   >>> poly = 3*x+2*y+1\n   >>> poly(x=y, y=[1, 2, 3])\n   polynomial([3+3*y, 5+3*y, 7+3*y])\n\nThe polynomials also support many numpy operations:\n\n.. code-block:: python\n\n   >>> numpy.reshape(x**numpy.arange(4), (2, 2))\n   polynomial([[1, x],\n               [x**2, x**3]])\n   >>> numpy.sum(numpoly.monomial(12)[::3])\n   polynomial(1+q**3+q**6+q**9+q**12)\n\nThere are also several polynomial specific operators:\n\n.. code-block:: python\n\n   >>> numpoly.diff([1, x, x**2], x)\n   polynomial([0, 1, 2*x])\n   >>> numpoly.gradient([x*y, x+y])\n   polynomial([[y, 1],\n               [x, 1]])\n\n\nDevelopment\n-----------\n\nDevelopment is done using `Poetry <https://poetry.eustace.io/>`_ manager.\nInside the repository directory, install and create a virtual enviroment with:\n\n.. code-block:: bash\n\n   poetry install\n\nTo run tests, run:\n\n.. code-block:: bash\n\n   poentry run pytest numpoly test --doctest-modules\n\nQuestions & Troubleshooting\n---------------------------\n\nFor any problems and questions you might have related to ``numpoly``, please\nfeel free to file an `issue <https://github.com/jonathf/numpoly/issues>`_.\n',
    'author': 'Jonathan Feinberg',
    'author_email': 'jonathf@gmail.com',
    'url': 'https://github.com/jonathf/numpoly',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
}


setup(**setup_kwargs)
