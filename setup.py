from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="envman",
    version="1.0.0",
    author="Ahmad Bilal",
    author_email="realahmad001@gmail.com",
    description="Secure environment variable manager with encryption and team sharing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ahmad0303/envman",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[
        "click>=8.0.0",
        "cryptography>=41.0.0",
        "tabulate>=0.9.0",
    ],
    entry_points={
        "console_scripts": [
            "envman=envman.cli:main",
        ],
    },
)
