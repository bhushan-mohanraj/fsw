import setuptools

setuptools.setup(
    name="fsw",
    version="0.1.1",
    description="Tools and guides for building apps with Flask, SQLAlchemy, and WTForms.",
    url="https://github.com/bhushanmohanraj/fsw",
    author="Bhushan Mohanraj",
    packages=setuptools.find_packages(),
    install_requires=[
        "Flask>=2.0",
        "SQLAlchemy>=1.4,<2",
        "WTForms>=2.3,<3",
    ],
    python_requires='>=3.6',
)
