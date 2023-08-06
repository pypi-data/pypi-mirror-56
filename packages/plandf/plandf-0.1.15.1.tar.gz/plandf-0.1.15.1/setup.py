from setuptools import setup

setup(name='plandf',
    version='0.1.15.1',
    description='Pandas DataFrame for computing Value-Over-Time for lists of tuples (Step.investables, Step.deliverables) of a Plan.',
    url='https://github.com/mindey/plandf',
    author='Mindey I.',
    author_email='mindey@infty.xyz',
    license='MIT',
    packages=['plandf'],
    install_requires=[
        'stepio>=0.1',
        'fred==3.1',
        'requests>=2.9.1',
        'pandas>=0.17.1',
    ],
    zip_safe=False)
