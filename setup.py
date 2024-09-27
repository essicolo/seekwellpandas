import os
import re
from setuptools import setup, find_packages

def get_version():
    init_py = os.path.join(os.path.dirname(__file__), 'src', 'seekwellpandas', '__init__.py')
    with open(init_py, 'r', encoding='utf-8') as f:
        content = f.read()
    match = re.search(r"^__version__\s*=\s*['\"]([^'\"]*)['\"]", content, re.M)
    if match:
        return match.group(1)
    raise RuntimeError("Unable to find version string in %s." % init_py)

# Lire le contenu du README
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="seekwellpandas",
    version=get_version(),
    author="Your Name",
    author_email="your.email@example.com",
    description="A pandas extension providing SQL-like methods for data manipulation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/seekwellpandas",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    python_requires=">=3.7",
    install_requires=[
        "pandas>=2.0.0",
        "pandas-flavor>=0.3.0",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="pandas sql data-manipulation",
)