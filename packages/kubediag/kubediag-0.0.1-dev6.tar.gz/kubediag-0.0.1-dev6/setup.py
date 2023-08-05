from distutils.core import setup

setup(
  name = 'kubediag',
  packages = ['kubediag'],
  version = '0.0.1-dev6',
  license = 'Apache-2.0',
  description = 'Kubernetes Diagnostic Tool built by AWS Premium Support',
  author = 'Jason Forte',
  author_email = 'fortejas@amazon.com',
  url = 'https://github.com/fortejas/kubediag',
  long_description = open('README.md').read(),
  long_description_content_type = 'text/markdown',
  description_content_type = 'text/markdown',
  download_url = 'https://github.com/fortejas/kubediag/archive/0.0.1-dev6.tar.gz',
  keywords = ['k8s', 'kubernetes', 'cli', 'troubleshooting'],
  scripts=['bin/kubediag'],
  install_requires=[
          'colorama',
          'kubernetes',
          'requests'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: Apache Software License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)