from setuptools import setup, find_packages

VERSION = '0.0.4'

setup(name='pyopendsix',
      version=VERSION,
      description='Restful Python API based on OpenD6',
      url='https://gitlab.com/HexGearInc/pyopendsix',
      license='MIT',
      author='Lucas Ramage',
      author_email='ramage.lucas@protonmail.com',
      packages=find_packages(),
      install_requires=['flask'],
      include_package_data=True,
      entry_points={
          'console_scripts': [
              'pyopendsix = pyopendsix.__main__:create_api'
          ]
      },
      zip_safe=False
)
