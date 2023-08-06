from setuptools import setup, find_packages            #这个包没有的可以pip一下

setup(
    name = "ustciscr",      #这里是pip项目发布的名称
    version = "2.2.5",  #版本号，数值大的会优先被pip
    keywords = ("pip", "ustciscr","featureextraction"),
    description = "This is ustc-iscr score package",
    long_description = "This is ustc-iscr score package",
    license = "MIT Licence",

    url = "https://github.com/WolverineQin/ustciscr",     #项目相关文件地址，一般是github
    author = "qjqqjq",
    author_email = "1102692995@qq.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ["numpy","pandas","requests","pyDes"]          #这个项目需要的第三方库
)
