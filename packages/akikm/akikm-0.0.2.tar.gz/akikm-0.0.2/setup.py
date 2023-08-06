import setuptools
from src.akikm import __version__

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="akikm",
    version=__version__,
    author="aki",
    author_email="heti@qq.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    description="akikm",
    url="https://github.com/aki/akikm",
    py_modules=['akikm'],
    package_dir={'': 'src'},
    license='BSD',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires = [
        'python-dateutil>=2.8.0',
        'pywin32>=227'
    ]
)
