import setuptools

pkg_name = "testhello321"

setuptools.setup(
    name=pkg_name,
    version="0.1.0",
    author="Elias",
    description="hello",
    packages=setuptools.find_packages(),
    scripts=['bin/testhello321'],
    include_package_data=True,
    install_requires=[
        'simplejson',
        ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ]
)