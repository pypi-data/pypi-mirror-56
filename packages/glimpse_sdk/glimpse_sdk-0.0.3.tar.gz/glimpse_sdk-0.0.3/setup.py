import distutils.core

try:
    import setuptools
except ImportError:
    pass

packages = ['Crypto']

distutils.core.setup(
    name='glimpse_sdk',
    version='0.0.3',
    packages=['glimpse_sdk'],
    author='murphy',
    author_email='murphy@nilinside.com',
    install_requires=packages
)
