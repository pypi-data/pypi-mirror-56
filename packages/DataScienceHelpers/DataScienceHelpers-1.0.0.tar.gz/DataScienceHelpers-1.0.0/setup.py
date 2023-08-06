import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="DataScienceHelpers",
    version="1.0.0",
    author="Max Taggart",
    author_email="max.taggart@healthcatalyst.com",
    description="Helper modules for doing data cleaning, training, exploration, etc.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=[
        "scikit-learn",
        "pandas",
        "numpy",
	"ipython",
        "bcolz",
        "graphviz",
        "sklearn_pandas",
        "isoweek",
        "pandas_summary",
    ],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
