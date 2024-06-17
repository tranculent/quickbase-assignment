from setuptools import setup, find_packages

setup(
    name='github_to_freshdesk',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'github_to_freshdesk=src.main:main',
        ],
    },
)
