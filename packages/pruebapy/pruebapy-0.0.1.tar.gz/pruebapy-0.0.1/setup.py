import setuptools


with open('README.md') as f:
    README = f.read()

setuptools.setup(
    author="Diego Alvarez",
    author_email="diesazul96@hotmail.com",
    name='pruebapy',
    license="MIT",
    description='Pruebapy has some useful functions like consuming a csv froma S3 bucket.',
    version='v0.0.1',
    long_description= README,
    url='https://github.com/diesazul96/pruebapy',
    packages=setuptools.find_packages(),
    python_requires=">=3.5",
    install_requires=['requests'],
    classifiers=[
        # Trove classifiers
        # (https://pypi.python.org/pypi?%3Aaction=list_classifiers)
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
    ],
)