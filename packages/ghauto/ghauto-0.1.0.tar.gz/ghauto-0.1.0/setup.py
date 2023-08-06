import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ghauto",
    version="0.1.0",
    author="Slack Tester",
    author_email="mrslackit@gmail.com",
    description="Slack API wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    install_requires=[
        'requests>=2.9.11',
        'typing>=3.5.3.0',
        'responses>=0.9.0'
    ],
    setup_requires=['pytest-runner'],
    test_suite='tests',
    tests_require=[
        'pytest>=3.3.1',
        'pytest-cov>=2.5.1',
        'pytest-flake8>=0.9.1',
        'pytest-mock>=1.6.3',
    ],
    zip_safe=True,
)
