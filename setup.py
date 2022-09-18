import pathlib

from setuptools import find_packages, setup

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")


setup(
    name="national-movie-database",
    version="0.0.1",
    description="National movies info & news sample web app - SDA Tirana, Albania",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gledi/national-movie-database",
    author="Gledi Caushaj",
    author_email="gledi.alb@gmail.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Topic :: Education",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "License :: Free For Educational Use",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3 :: Only",
        "Framework :: Django :: 4",
        "Operating System :: OS Independent",
    ],
    keywords="movies, final, project, SDA",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.9, <4",
    install_requires=[
        "django",
        "environs",
        "dj-database-url",
        "djangorestframework",
        "django-registration-redux",
        "django-hashids",
        "django-crispy-forms",
        "crispy-bootstrap5",
        "pillow",
        "django-imagekit",
        "django-mptt",
        "django-taggit",
        "django-filter",
        "whitenoise[brotli]",
        "stripe",
        "psycopg2",
        "mistune",
        "pygments",
    ],
    extras_require={
        "dev": [
            "django-debug-toolbar",
            "django-extensions",
            "ipython",
            "ruff",
            "black",
            "isort",
            "graphviz",
            "mypy",
        ],
        "test": [
            "pytest",
            "pytest-django",
            "coverage",
            "pytest-cov",
            "model-bakery",
            "faker",
        ],
        "prod": [
            "gunicorn",
        ],
    },
    entry_points={
        "console_scripts": [
            "manage=nmdb.manage:main",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/gledi/national-movie-database/issues",
        "Source": "https://github.com/gledi/national-movie-database",
    },
)
