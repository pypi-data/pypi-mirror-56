from setuptools import setup, find_packages

setup(
    name="eventmonitoring-client",
    version="1.8.1",
    packages=find_packages(),
    install_requires=["requests>=2.18.2", "zappa>=0.47.1"],
)
