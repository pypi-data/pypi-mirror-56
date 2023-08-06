from distutils.core import setup

setup(
    name="jsoncompare3",
    version='0.1.0',
    author='Lanser.Z',
    author_email='lanser.z@gmail.com',
    url='https://github.com/lanser-z/jsoncompare.git',
    license='LICENSE.txt',
    description='jsoncompare3 is a simple Python3 utility for comparing two JSON objects',
    long_description=open('README.txt').read(),
    install_requires=[
        "requests >= 2.0.0",
    ],

)
