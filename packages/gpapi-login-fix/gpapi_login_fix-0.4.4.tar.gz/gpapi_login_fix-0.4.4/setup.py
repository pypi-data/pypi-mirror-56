from setuptools import setup
from setuptools.command.build_py import build_py as _build


import os.path
import subprocess

PROTOC_BIN = "/usr/local/bin/protoc"

CURRENT_DIR = os.path.abspath( os.path.dirname( __file__ ) )

class ProtobufBuilder(_build):

    def run(self):
        # check if protobuf is installed
        if not os.path.isfile(PROTOC_BIN):
            raise Exception("You should install protobuf compiler")

        print("Building protobuf file")
        subprocess.run([PROTOC_BIN,
            "--proto_path=" + CURRENT_DIR,
            "--python_out=" + CURRENT_DIR + "/gpapi/",
            CURRENT_DIR + "/googleplay.proto"])
        super().run()

setup(name='gpapi_login_fix',
      version='0.4.4',
      description='Unofficial python api for google play',
      url='https://github.com/worldofprasanna/googleplay-api',
      download_url = 'https://github.com/worldofprasanna/googleplay-api/archive/0.4.4.tar.gz',
      author='NoMore201',
      author_email='domenico.iezzi.201@gmail.com',
      license='GPL3',
      packages=['gpapi_login_fix'],
      package_data={
          'gpapi_login_fix': [
              'config.py'
              'device.properties',
              'googleplay_pb2.py',
              'googleplay.py',
              'utils.py'
          ]},
      include_package_data=True,
      cmdclass={'build_py': ProtobufBuilder},
      install_requires=['cryptography>=2.2',
                        'protobuf>=3.5.2',
                        'requests'])
