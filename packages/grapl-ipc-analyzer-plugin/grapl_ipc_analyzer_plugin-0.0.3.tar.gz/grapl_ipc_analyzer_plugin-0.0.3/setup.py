from setuptools import setup, find_packages

setup(
    name="grapl_ipc_analyzer_plugin",
    version="0.0.3",
    description="Library for Grapl Analyzers",
    url="https://github.com/insanitybit/grapl-ipc-plugin/",
    author="insanitybit",
    author_email="insanitybit@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    zip_safe=False,
    package_data = {
        "grapl_ipc_analyzer_plugin": ["py.typed"]
    },
    packages=find_packages(),
    include_package_data=True,
    install_requires=["pydgraph"],
)
