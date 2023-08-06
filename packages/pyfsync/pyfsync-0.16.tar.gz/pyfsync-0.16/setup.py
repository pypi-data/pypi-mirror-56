from distutils.core import setup

install_requires = open("requirements.txt").read().strip().split("\n")

setup(
  name = 'pyfsync',
  packages = ['pyfsync'],
  version = '0.16',
  license='MIT',        
  description = 'Synchronize directories between hosts. ',   
  author = 'Be Water',
  author_email = 'be@water.com',
  url = 'https://github.com/hanayashiki/fsync',   
  download_url = 'https://github.com/hanayashiki/fsync',    
  keywords = ['Websocket', 'File Management', 'Tool'],   
  install_requires=install_requires,
  include_package_data=True,
  classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)
