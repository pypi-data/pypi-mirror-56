from setuptools import setup, find_packages

setup(
  name = 'AiohttpStarter',
  packages=find_packages(),
  version = '0.2.0',
  license='MIT',
  description = 'Aiohttp server starter',
  author = 'Maksim Vorontsov',
  author_email = 'social.maksim.vrs@gmail.com',
  url = 'https://gitlab.com/maksimvrs/aiohttp-starter',
  download_url = 'https://gitlab.com/maksimvrs/aiohttp-starter/-/archive/master/aiohttp-starter-master.tar.gz',
  keywords = ['aiohttp', 'starter', 'django'],
  install_requires=[
        'python-settings',
        'aiohttp',
        'click',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)