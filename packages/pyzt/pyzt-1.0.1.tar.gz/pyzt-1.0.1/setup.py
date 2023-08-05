from setuptools import setup

setup(
    author="pyzt",
    author_email="info@azat.ai",
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    description="pyzt python librariy wrapper for azt lang.",
    install_requires=["azt","cython","termcolor"],
    keywords="pyzt",
    name="pyzt",
    package_dir={"": "src"},
    packages=["pyzt"],
    url="https://azat.ai",
    version="1.0.1"
)