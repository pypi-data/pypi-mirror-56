from setuptools import setup, find_packages

setup(
    name="dataflame",
    version="1.0.6-beta",
    description="DataFlame: Machine-Learning Oriented Dataframe Manipulation Interface for Pandas Dataframes",
    url="https://github.com/shayanfazeli/dataflame",
    author="Shayan Fazeli",
    author_email="shayan@cs.ucla.edu",
    license="Apache",
    classifiers=[
          'Intended Audience :: Science/Research',
          #'Development Status :: 1 - Beta',
          'License :: OSI Approved :: Apache Software License',
          'Programming Language :: Python :: 3.6',
          'Topic :: Scientific/Engineering :: Artificial Intelligence'
      ],
    keywords="dataflame machine learning dataframe label interpolation",
    packages=find_packages(),
    python_requires='>3.6.0',
    install_requires=[
        'numpy',
        'pandas',
        'sklearn'
    ],
    zip_safe=False
)