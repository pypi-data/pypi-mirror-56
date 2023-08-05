from setuptools import setup
setup(
    name='gameoflifepython',
    version='1.0.3',
    description='Game of Life implemented with PyGame.',
    author='FKH',
    license='GPL-3.0',
    packages=['gameoflifepython'],
    scripts=[
        'bin/gameoflifepython',
        'bin/gameoflifepython.bat',
    ],
    zip_safe=False,
    install_requires=[
        'pygame'
    ]
)