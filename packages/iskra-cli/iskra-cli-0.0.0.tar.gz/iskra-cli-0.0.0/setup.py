from os.path import dirname, abspath
from setuptools import setup, find_packages


HERE = abspath(dirname(__file__))
README = open('README.md', encoding='utf-8').read()

setup(
    name='iskra-cli',
    version='0.0.0',
    url='https://iskra.ml',
    author='Eddy Ernesto del Valle Pino',
    author_email='eddy@edelvalle.me',
    long_description=README,
    long_description_content_type='text/markdown',
    description="Let's you interact with Iskra from the terminal",
    license='Freeware',
    packages=find_packages(exclude=['tests']),
    python_requires='>=3.5',
    install_requires=[
        'websocket-client==0.56.0',
        'colorama>=0.4,<0.5',
    ],
    scripts=['scripts/iskra'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: Freeware',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
)
