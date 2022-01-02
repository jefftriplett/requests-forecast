from pathlib import Path
from setuptools import setup, find_packages


readme = Path("README.md").read_text()
license = Path("LICENSE").read_text()

setup(
    name="requests-forecast",
    license="BSD",
    version="0.6.2",
    description="A minimalist Forecast.io API client.",
    long_description=readme,
    author="Jeff Triplett",
    author_email="jeff.triplett@gmail.com",
    url="https://github.com/jefftriplett/requests-forecast",
    py_modules=["requests_forecast"],
    install_requires=[
        "requests>=1.2",
        "pytz",
    ],
    packages=find_packages(),
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
