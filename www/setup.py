from setuptools import setup, find_packages


setup(
    name="softorks-and-softarna",
    use_scm_version={
        "write_to": "www/__init__.py",
        "write_to_template": '__version__ = "{version}"',
    },
    packages=find_packages(),
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
