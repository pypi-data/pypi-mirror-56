from setuptools import setup, find_packages  

setup(  
    name = 'c_progress_bar',  
    version = '0.0.3',
    # keywords = ('chinesename',),  
    description = 'show progress bar',  
    license = 'MIT License',  
    install_requires = [],  
    packages = ['c_progress_bar'],  # 要打包的项目文件夹
    include_package_data=True,   # 自动打包文件夹内所有数据
    author = 'evanyang',  
    author_email = 'lightyiyi@qq.com',
    url = 'https://www.cnblogs.com/Evan-fanfan/',
    # packages = find_packages(include=("*"),),  
)  
