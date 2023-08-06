import setuptools

pkg_name = "howdytest222"

setuptools.setup(
    name=pkg_name,
    version="0.1.0",
    author="Elias",
    description="test",
    packages=setuptools.find_packages(),
    scripts=['bin/howdytest222'],
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