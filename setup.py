from setuptools import setup

setup(
    name='markmove',
    version='0.0.9',
    description='a pip package which is used to move markdown files',
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author='sword4869',
    url='https://github.com/sword4869/markmove',
    install_requires=[
        'configargparse',
        'opencv-contrib-python',
        'numpy',
        'pillow',
        'PySimpleGUI'
    ],
    entry_points={
        'console_scripts': [
            'markmove = markmove.move:main',
            'markmove_gui = markmove.gui:main',
        ]
    },
)