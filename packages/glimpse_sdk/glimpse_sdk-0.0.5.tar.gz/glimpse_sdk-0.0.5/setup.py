import distutils.core

try:
    import setuptools
except ImportError:
    pass

packages = ['pycryptodome']

distutils.core.setup(
    name='glimpse_sdk',
    version='0.0.5',
    packages=['glimpse_sdk', 'glimpse_sdk/mycrypto'],
    author='murphy',
    author_email='murphy@nilinside.com',
    install_requires=packages
)
