import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
  name = 'prepro',         
  packages = ['prepro'],   
  version = '0.4',     
  license='MIT',
  description = 'Useful for Auto Pre-processing',
  long_description=""" Preprocessing Module prepro.missing(data="",min_ratio=0.0,values="",method="mean",drop_max="no) 
  https://github.com/stsfaroz/prepro """,   
  author = 'SALMAN_FAROZ',                   
  author_email = 'farozsts@gmail.com',      
  url = 'https://github.com/stsfaroz/prepro',  
  download_url = 'https://github.com/stsfaroz/prepro/archive/0.1.tar.gz',    
  keywords = ['missing values', 'preprocessig'],   
  install_requires=[            
          'numpy',
          'pandas',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',      
    'Intended Audience :: Developers',     
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3.6',
  ],
)
