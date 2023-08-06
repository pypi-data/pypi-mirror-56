from pathlib import Path
from setuptools import setup

PWD = Path(__file__).parent
README = (PWD / "README.rst").read_text()

setup(
    name='coding-test-foo',
    packages=['bar'],
    description='coding test package. I am a description.',
    long_description=README,
    long_description_content_type='text/x-rst',
    version='2.0.2',
    license='MIT',
    url='https://coding.net',
    author='Eric Chan',
    author_email='chenxinyu@coding.net',
    maintainer="Hello Nico, Eric Chan",
    maintainer_email="chenxinzhou@coding.net, support@coding.net",
    project_urls={
        "Bug Tracker": "https://bugs.example.com/HelloWorld/",
        "Documentation": "https://docs.example.com/HelloWorld/",
        "Source Code": "https://code.example.com/HelloWorld/",
    },
    classifiers=[
        'License :: OSI Approved :: Python Software Foundation License'
    ],
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst'],
        # And include any *.msg files found in the 'hello' package, too:
        'hello': ['*.msg'],
    },
    install_requires=['pip>=19.1.0'],
    extras_require={
        ":python_version>'2.7'": ["docutils"],
        'reST': ["docutils>=0.3"],
        'PDF': ["ReportLab>=1.2", "RXP"],
    },
    provides=['foo', 'foo'],
    zip_safe=False
)
