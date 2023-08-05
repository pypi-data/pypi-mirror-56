from setuptools import setup, find_packages

install_requires = [
    'click',
    'psutil',
    'numpy',
]

setup(
    name='pyspyke',
    version='0.0.1',
    author='Joshua Groeschl',
    author_email='joshua.groeschl@tutanota.com',
    description='Application for consuming memory of linux systems.',
    license='MIT',
    py_modules=['pyspyke'],
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'pyspyke = pyspyke.pyspyke:main',
        ]
    },
    package_dir={'': 'src'},
    packages=find_packages('src')
)