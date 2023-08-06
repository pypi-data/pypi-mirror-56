import setuptools

try:  # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError:  # for pip <= 9.0.3
    from pip.req import parse_requirements

requirements = parse_requirements('requirements.txt', session=False)

setuptools.setup(
    name="artificial",
    version="0.0.2",
    author="Artificial team",
    author_email="info@artificial.com",
    description="Artificial tools",
    packages=setuptools.find_namespace_packages(include=['artificial.*']),
    install_requires=[str(x.req) for x in requirements],
    python_requires='~=3.6',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ]
)
