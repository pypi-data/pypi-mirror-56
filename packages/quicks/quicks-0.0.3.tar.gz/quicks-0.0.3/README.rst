
Quicks
======

Project generator

.. code-block::

   pip install quicks

   quicks PROJECT_NAME example.yml

example.yml Jinja2 style

.. code-block:: yaml

   files:
     - '{{project}}/__init__.py'
     - '{{project}}/__main__.py'
     - '{{project}}/requirements.txt'
     - '.gitignore'
     - 'LICENSE'
     - 'Dockerfile'
     - 'README.md'

   templates:
     'README.md': |
       # {{project}}
