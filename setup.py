from setuptools import setup, find_packages

setup(
    name="saois",
    version="2.0.0",
    packages=find_packages(),
    install_requires=[
        "rich>=13.0.0",
    ],
    entry_points={
        "console_scripts": [
            "saois=saois.simple_cli:main",
        ],
    },
    author="Anne",
    description="AI Development Assistant - Work on any project with the right AI tool",
    python_requires=">=3.9",
)
