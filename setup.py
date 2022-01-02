from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='requests-forecast',
    license='BSD',
    version='0.6.2',
    description='A minimalist Forecast.io API client.',
    long_description=readme,
    author='Jeff Triplett',
    author_email='jeff.triplett@gmail.com',
    url='https://gitlab.com/jeff.triplett/requests-forecast',
    py_modules=['requests_forecast'],
    install_requires=[
        'cached-property',
        'requests>=1.2',
        'pytz',
    ],
    packages=find_packages(),
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
