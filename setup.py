import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aist",
    version="0.2.3",
    author="Feimax",
    author_email="me@feimax.com",
    description="AIST = AI Service Tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/feimax/aist",
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'requests',
        'tqdm',
        'qiniu'
    ]
)
