import setuptools
import pathlib


readme_path = pathlib.Path(__file__).parent.resolve() / "README.md"

setuptools.setup(
    name="fsw",
    version="0.2.2",
    description="Tools and guides for building apps with Flask, SQLAlchemy, and WTForms.",
    long_description=readme_path.read_text("utf-8"),
    long_description_content_type="text/markdown",
    url="https://github.com/bhushan-mohanraj/fsw",
    author="Bhushan Mohanraj",
    packages=setuptools.find_packages(),
    install_requires=[
        "Flask>=2.0,<3",
        "SQLAlchemy>=1.4,<2",
        "WTForms>=3.0,<4",
    ],
    python_requires=">=3.10",
)
