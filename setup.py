import os
import re
from setuptools import setup, find_packages

def get_version():
    init_py = os.path.join(os.path.dirname(__file__), 'src', 'seekwellpandas', '__init__.py')
    with open(init_py, 'r') as f:
        content = f.read()
    match = re.search(r"^__version__\s*=\s*['\"]([^'\"]*)['\"]", content, re.M)
    if match:
        return match.group(1)
    raise RuntimeError("Unable to find version string in %s." % init_py)

setup(
    name="seekwellpandas",
    version=get_version(),
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    python_requires=">=3.7",
    install_requires=[
        "pandas>=1.0.0",
        "pandas-flavor>=0.3.0",
    ],
    # Autres paramètres de configuration...
)