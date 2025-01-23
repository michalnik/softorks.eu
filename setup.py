from setuptools import setup, find_packages


setup(
    name="website-softorks",
    use_scm_version={
        "version_scheme": "post-release",
        "local_scheme": "no-local-version",
        "write_to": "www/www/__init__.py",
        "write_to_template": '__version__ = "{version}"',
    },
    packages=find_packages(),
    include_package_data=True,
    description="WWW website of mine - softorks.eu and softarna.cz",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    setup_requires=["setuptools_scm"],
    python_requires=">=3.10",
    install_requires=[
        "python-dotenv",
        "django"
    ],
    extras_require={
        "dev": [
            "django-extensions"
        ],
        "prod": [
            "gunicorn[gevent]"
        ],
    },
)
