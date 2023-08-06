import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="chrys",
    version="3.0.6",
    author="Hein Bekker",
    author_email="hein@netbek.co.za",
    description="A collection of color palettes for mapping and visualisation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='BSD-3-Clause',
    url="https://github.com/netbek/chrys",
    install_requires=[
        'matplotlib == 2.2.4',
        'nose == 1.3.7',
        'numpy == 1.7.1',
        'wcag-contrast-ratio == 0.9',
    ],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX :: Linux",
    ],
)
