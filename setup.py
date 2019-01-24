from setuptools import setup, find_packages

setup(
    name='amznscrp',
    url='https://github.com/jenslaufer/amznscrp.git',
    author='Jens Laufer',
    author_email='jenslaufer@gmail.com',
    packages=['amznscrp'],
    install_requires=['requests', 'argparse', 'bottlenose',
                      'bs4', 'lxml', 'getsmarties', 'scikit-learn', 'pickle', 'pandas', 'numpy'],
    version='0.0.1',
    license='MIT',
    description='Tools to scrp Amz',
)
