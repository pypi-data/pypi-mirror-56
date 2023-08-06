import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pgcrud", # Replace with your own username
    version="0.1.0",
    author="Will Watkinson",
    author_email="wjwats4295@gmail.com",
    description="A package to perform Postgres CRUD operations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/wjwatkinson/pgcrud",
    packages=["pgcrud"],
    install_requires=['psycopg2'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
