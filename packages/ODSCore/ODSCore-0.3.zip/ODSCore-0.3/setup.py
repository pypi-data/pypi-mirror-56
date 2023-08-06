from distutils.core import setup
setup(
  name = 'ODSCore',
  packages = ['ODSCore'],   
  version = '0.3',      
  license='MIT',       
  description = 'Core Components for ODS Database',   
  author = 'Monty Dimkpa',                   
  author_email = 'cmdimkpa@gmail.com',      
  url = 'https://github.com/cmdimkpa/ODSCore',   
  download_url = 'https://github.com/cmdimkpa/ODSCore/archive/v_03.tar.gz',    
  keywords = ['ODS', 'S3AppDatabase', 'Database'],   
  install_requires=[            
          'requests',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',    
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 2.7',      
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
