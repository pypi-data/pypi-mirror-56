import setuptools

setuptools.setup(
    name="tod0",
    version="0.2.0",
    author="kiblee",
    author_email="kiblee@pm.me",
    packages=["todocli", "todocli.test"],
    url="https://github.com/kiblee/tod0",
    license="LICENSE",
    description="A CLI for Microsoft To-Do.",
    install_requires=["Click", "pyyaml", "requests", "requests_oauthlib",],
    include_package_data=True,
    entry_points="""
        [console_scripts]
        tod=todocli.cli:main
    """,
    python_requires=">=3.6",
)
