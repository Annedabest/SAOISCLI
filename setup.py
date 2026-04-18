from setuptools import setup, find_packages

setup(
    name="saois",
    version="2.0.0",
    # Do not ship tests/ as an installable package (find_packages would pick it up via tests/__init__.py).
    packages=find_packages(exclude=["tests", "tests.*"]),
    package_data={"saois": ["templates/*.md", "experts/*.md"]},
    include_package_data=True,
    install_requires=[
        "rich>=13.0.0",
    ],
    extras_require={
        "dev": ["pytest>=7.0"],
    },
    entry_points={
        "console_scripts": [
            "saois=saois.simple_cli:main",
        ],
    },
    author="Anne",
    description="AI Development Assistant - Work on any project with the right AI tool",
    python_requires=">=3.9",
)
