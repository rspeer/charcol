from setuptools import setup

setup(
    name="charcol",
    version='0.1',
    maintainer='Rob Speer',
    maintainer_email='rob@luminoso.com',
    license="MIT",
    url='http://github.com/rspeer/charcol',
    platforms=["any"],
    description="Collects Unicode characters found in the wild",
    packages=['charcol'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    #entry_points={
    #    'console_scripts': [
    #    ]
    #}
)
