from setuptools import setup, find_packages
from os.path import join, dirname


setup(
    name="aiocian",
    version="0.0.2",
    
    author="Oleg Yurchik",
    author_email="oleg.yurchik@protonmail.com",
    url="https://github.com/OlegYurchik/aiocian",
    
    description="",
    long_description=open(join(dirname(__file__), "README.md")).read(),
    long_description_content_type="text/markdown",
    
    packages=find_packages(exclude=["tests"]),

    python_requires=">=3.6",
    install_requires=["aiohttp", "requests"],
    tests_require=["pytest"],
    test_suite="tests",
)
