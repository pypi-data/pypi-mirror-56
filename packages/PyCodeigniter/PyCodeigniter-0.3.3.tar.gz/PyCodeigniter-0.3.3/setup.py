#from distutils.core import setup
from setuptools import setup, find_packages

setup(
    name='PyCodeigniter',
    version='0.3.3',
     packages=['codeigniter', 'codeigniter.system',
              'codeigniter.system.core',  'codeigniter.application',
              'codeigniter.application.config', 'codeigniter.application.models', 'codeigniter.application.helpers',
              'codeigniter.application.library', 'codeigniter.application.controllers','codeigniter.application.views'],
    url='https://github.com/sjqzhang/PyCodeigniter',
    license='GPL',
    # install_requires = ['setuptools','pymysql','DBUtils'],
    install_requires=['pymysql==0.7.6','DBUtils==1.2','gevent==1.2.0'],
    author='s_jqzhang',
    author_email='s_jqzhang@163.com',






    description="Codeigniter(PHP) implement by python\n If you want to build high performance service you'd better use gevent. "

)

