import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="imdb-search",
    version="0.0.1",
    entry_points={
        'console_scripts': ['imdb-search=imdb_search.main:main'],
    },
    author="Richard Fontein",
    author_email="richard@fontein.co",
    license='MIT',
    description="CLI to search for movies than an actor/actress has starred in.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/richardfontein/imdb-search",
    packages=setuptools.find_packages(),
    install_requires=[
        'pick',
        'requests'
    ],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.6',
)
