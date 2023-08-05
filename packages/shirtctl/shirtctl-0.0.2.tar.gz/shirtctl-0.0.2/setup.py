from setuptools import setup
from os import path

with open(path.join(path.abspath(path.dirname(__file__)), 'README.md'), encoding='utf-8') as f:
  long_description = f.read()

setup(
  name = 'shirtctl',         
  packages = ['shirtctl'],   
  version = '0.0.2',      
  license='MIT',        
  description = 'The shirtctl Python SDK',
  long_description=long_description,
  long_description_content_type='text/markdown',
  author = 'Blair Hudson',                
  author_email = 'blair@shirtctl.com',     
  url = 'https://github.com/shirtctl/shirtctl-sdk-python',
  # download_url = '',    
  keywords = ['shirtctl', 'Python', 'SDK'],   
  install_requires=[],
  classifiers=[],
)