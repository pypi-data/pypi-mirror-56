from setuptools import setup , find_packages

long_description = 'Name: IOTBit Library for IoTBit V1.7 i.e industrial variant \n Purpose: Library to interface with the IOTBit HAT on the Raspberry Pi, \n tested on the latest version of Raspbian using a Raspberry Pi 3b.\n classes: IotModem \n requirements: pyserial module, RPI.GPIO'
#TODO: add smbus to requirements for battery support.
setup(name='iotbit_library',
      version='1.0.6',
      description='Library to work with the IoTBit Industrial version on the Raspberry Pi',
      long_description=long_description,
      # url='https://github.com/robintibor/python-mindwave-mobile',
      author='Sam',
      author_email='sam@altitude.pw',
      packages=find_packages(),
      install_requires=[
          'pyserial',
          'RPI.GPIO'
      ],
      classifiers=[
          "Programming Language :: Python :: 3",
          "Operating System :: POSIX :: Linux",
          "Development Status :: 5 - Production/Stable "
      ]
      )
