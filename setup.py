from setuptools import setup, find_packages

with open("README_CLIENT.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="filevault-client",
    version="1.0.0",
    author="FileVault Team",
    description="Professional CLI client for FileVault remote file management",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/filevault",
    py_modules=["filevault_client"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: System :: Filesystems",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.28.0",
    ],
    entry_points={
        "console_scripts": [
            "filevault=filevault_client:main",
        ],
    },
)
