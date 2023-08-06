from distutils.core import setup


setup(
  name='glue2protojson',
  packages=['glue2protojson'],
  version='0.1.0',
  license='MIT',
  description='Get a AWS Glue table schema and convert it to JSON of meta types and proto messages definition',
  author='Ricardo Edo Nevado',
  author_email='ricardo.edo@gmail.com',
  url='https://github.com/ricardoedo',
  download_url='https://github.com/ricardoedo/glue2protojson/archive/v0.1.0-beta.tar.gz',
  keywords=['AWS', 'GLUE', 'GRPC', 'PROTO', 'PROTOBUF'],
  install_requires=[
          'boto3>=1.10.25',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',  # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
  ],
)
