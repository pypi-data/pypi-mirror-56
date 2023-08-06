import setuptools

setuptools.setup(
    name="rottencode",
    version="0.3.0",
    author="Oliver Berger",
    author_email="diefans@gmail.com",
    description="exhibit rotten code",
    long_description="exhibit rotten code",
    # long_description_content_type="text/markdown",
    zip_safe=False,
    include_package_data=True,
    package_dir={"": "src"},
    # https://setuptools.readthedocs.io/en/latest/setuptools.html#find-namespace-packages
    packages=setuptools.find_namespace_packages(where="src"),
    entry_points={
        # register our microservice plugins
        "console_scripts": ["rottencode = rottencode.cli:main"]
    },
    install_requires=["click", "structlog", "colorama", "typed_astunparse"],
    extras_require={
        "tests": [
            "pytest>=4.6,<5.0",
            "pytest-cov>=^2.7,<3.0",
            "mock>=3.0<4.0",
            "pytest-mock>=1.10<2.0",
            "pytest-watch>=4.2<5.0",
            "pytest-randomly>=3.1<4.0",
            "pdbpp",
        ]
    },
)