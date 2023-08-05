from setuptools import setup

setup(
    name='DataScienceTools',
    version='0.1dev',
    packages=['dstools','dstools.preprocessing', 'dstools.classifier'],
    license='MIT License',
    long_description=open('README.md').read(),
    python_requires='>3.6',
    install_requires=[
                    'numpy>=1.16.2',
                    'pandas>=0.24.2',
                    'scikit-learn>=0.20.3',
                    ]
)