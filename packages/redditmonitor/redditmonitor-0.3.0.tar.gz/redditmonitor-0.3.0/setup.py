from setuptools import setup, find_packages
setup(
    name="redditmonitor",
    version="0.3.0",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'redditmonitor = redditmonitor.monitor:main',
        ]
    },
    install_requires=[
    	'praw>=6',
    ],
)