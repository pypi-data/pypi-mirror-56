from setuptools import setup, find_packages

setup(
  name = 'AioBrokerTools',
  packages=find_packages(),
  version = '0.1.1',
  license='MIT',
  description = 'Async rabbitmq microservices framework',
  author = 'Maksim Vorontsov',
  author_email = 'social.maksim.vrs@gmail.com',
  url = 'https://gitlab.com/maksimvrs/aiobroker',
  download_url = 'https://gitlab.com/maksimvrs/aiobroker/-/archive/master/aiobroker-master.tar.gz',
  keywords = ['async', 'broker', 'rabbitmq', 'framework', 'microservice'],
  install_requires=[
        'aio-pika',
        'aiojobs',
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