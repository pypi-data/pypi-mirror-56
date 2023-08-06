import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="idact-gui",
    version="0.2.4",
    author="Joanna Chyży, Karolina Piekarz, Piotr Swędrak",
    author_email="piotrekswedrak@gmail.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/intdata-bsc/idact-gui",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'PyQt5<5.10',
    ],
    dependency_links=[
        'git+ssh://git@github.com/intdata-bsc/idact.git@0.9#egg=idact'
    ],
    entry_points={
        'console_scripts': [
            'idactgui=gui.main:main',
        ],
    }
)
