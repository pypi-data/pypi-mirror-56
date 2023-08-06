from setuptools import setup, find_packages

setup(
    name="ebayoauthclient",
    version="0.0.3",
    packages=find_packages(),
    license="LICENSE",
    description="Python OAuth SDK: Get OAuth tokens for eBay public APIs",
    author="Hossein Amin",
    author_email="hossein@aminbros.com",
    url="https://github.com/hosseinamin/ebay-oauth-python-client",
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
    ],
    install_requires=[
        'requests>=2.21.0,<3',
        'PyYAML>=5.1,<6',
    ],
    setup_requires=[
        'selenium>=3.141.0,<4',
    ]
)
