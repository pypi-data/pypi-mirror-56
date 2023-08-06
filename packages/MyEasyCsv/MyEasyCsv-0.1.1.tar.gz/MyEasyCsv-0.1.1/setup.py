from setuptools import setup, find_packages

setup(
    name="MyEasyCsv",
    version="0.1.1",
    description="easy csv",
    long_description="easy csv",
    license="MIT Licence",
    url="https://github.com/1085561450/hello-world",
    author="WJA",
    author_email="1085561450@qq.com",
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=['csv']
)
