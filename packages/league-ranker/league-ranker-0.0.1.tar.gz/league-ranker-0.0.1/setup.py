from setuptools import find_packages, setup


with open('README.rst') as f:
    long_description = f.read()


setup(
    name='league-ranker',
    version='0.0.1',
    packages=find_packages(exclude=('tests',)),
    package_data={'league_ranker': ['py.typed']},
    url='https://ranker.readthedocs.io/en/latest/',
    project_urls={
        'Documentation': 'https://ranker.readthedocs.io/en/latest/',
        'Code': 'https://github.com/PeterJCLaw/ranker',
        'Issue tracker': 'https://github.com/PeterJCLaw/ranker/issues',
    },
    description="League ranking for arbitrary numbers of competitors.",
    long_description=long_description,
    author='Student Robotics Competition Software SIG',
    author_email='srobo-devel@googlegroups.com',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Typing :: Typed',
    ],
    setup_requires=[
        'Sphinx >=1.8.5, <2',
    ],
    test_suite='tests',
    zip_safe=True,
)
