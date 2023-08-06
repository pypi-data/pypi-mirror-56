from distutils.core import setup
setup(
  name = 'unifiled',
  packages = ['unifiled'],
  version = '1.1',
  license='MIT',
  description = 'Easily connect to Ubiquiti Unifi led devices',
  author = 'Floris Van der krieken',
  author_email = 'git@florisvdk.net',
  url = 'https://github.com/florisvdk/unifiled',
  download_url = 'https://github.com/florisvdk/unifiled/archive/v1.1.zip',
  keywords = ['UNIFI', 'LED', 'CONTROLLER', 'UBIQUITI'],
  install_requires=[
          'requests',
          'urllib3',
      ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',      # "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)
