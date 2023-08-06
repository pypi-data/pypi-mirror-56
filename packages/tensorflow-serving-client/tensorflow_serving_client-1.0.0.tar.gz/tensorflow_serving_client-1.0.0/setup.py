import setuptools


class BuildPackageProtos(setuptools.Command):
  description = 'build grpc protobuf modules'
  user_options = []

  def initialize_options(self):
    pass
  def finalize_options(self):
    pass

  def run(self):
    from grpc_tools.command import build_package_protos
    build_package_protos('.')


setuptools.setup(
    name='tensorflow_serving_client',
    version='1.0.0',
    description='Python client for tensorflow serving',
    author='Triage Technologies Inc.',
    author_email='ai@triage.com',
    url='https://triage.com',
    license='MIT',
    packages=[
        'tensorflow_serving_client',
        'tensorflow_serving_client.protos',
    ],
    scripts=[
        'bin/tensorflow_serving_client',
    ],
    setup_requires=[
        'cython',
        'grpcio-tools'
    ],
    install_requires=[
        'grpcio',
        'keras-model-specs == 1.*'
    ],
    cmdclass={
        'build_protos': BuildPackageProtos
    },
)
