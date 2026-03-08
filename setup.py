from setuptools import setup, find_packages

setup(
    name="saois",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "rich>=13.0.0",
    ],
    entry_points={
        "console_scripts": [
            "saois=saois.cli:main",
        ],
    },
    author="Anne",
    description="An innovative 3D animated CLI for managing development projects",
    python_requires=">=3.7",
)
