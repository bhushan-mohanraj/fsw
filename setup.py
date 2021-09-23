import setuptools

setuptools.setup(
    name="fsw",
    version="0.0.0",
    author="Bhushan Mohanraj",
    description="Tools and guides for building apps with Flask, SQLAlchemy, and WTForms.",
    install_requires=[
        "Flask>=2",
        "SQLAlchemy>=1.4,<2",
        "WTForms>=2.3,<3",
    ],
)
