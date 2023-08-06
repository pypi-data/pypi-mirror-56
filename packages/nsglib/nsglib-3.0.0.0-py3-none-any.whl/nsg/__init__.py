"""
Declares nsg as a namespace package

https://stackoverflow.com/questions/1675734/how-do-i-create-a-namespace-package-in-python
"""
from pkgutil import extend_path
__import__('pkg_resources').declare_namespace(__name__)

__path__ = extend_path(__path__, __name__)
