from setuptools import find_packages, setup

setup(
    name='markmove',
    version='0.0.3',
    description='a pip package which is used to move markdown files',
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author='sword4869',
    url='https://github.com/sword4869/markmove',
    install_requires=[
        'configargparse',
        'opencv-contrib-python',
        'numpy'
    ],
    entry_points={
        'console_scripts': [
            'markmove = markmove.main:main',
        ]
    },
)