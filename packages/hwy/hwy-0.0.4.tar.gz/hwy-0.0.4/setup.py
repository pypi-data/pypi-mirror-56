from setuptools import find_packages, setup

with open('README.md') as f:
    long_description = f.read()

setup(
    name='hwy',
    version="0.0.4",
    description='print hello wy',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='wy',
    url='',
    author_email='',
    license='MIT', 
    packages=find_packages(),
    scripts = ['hwy/hellowy.py'],
    entry_points={
        'console_scripts': 'hwy = hwy.hellowy:balaba'
    },
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License"
    ]
)
