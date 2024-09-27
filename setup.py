from setuptools import setup, find_packages

setup(
    name="seekwellpandas",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pandas>=2.2.3",
        "pandas_flavor>=0.6.0",
    ],
    python_requires=">=3.10",
)