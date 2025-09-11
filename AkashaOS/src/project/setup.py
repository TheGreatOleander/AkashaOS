
from setuptools import setup, find_packages

setup(
    name="akashaos",
    version="0.1.0",
    description="AkashaOS: A symbiotic ecosystem playground for AI and human creativity",
    author="AkashaOS Community",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click",
    ],
    entry_points={
        "console_scripts": [
            "akasha=akasha.cli:main",
        ],
    },
    python_requires=">=3.7",
)
