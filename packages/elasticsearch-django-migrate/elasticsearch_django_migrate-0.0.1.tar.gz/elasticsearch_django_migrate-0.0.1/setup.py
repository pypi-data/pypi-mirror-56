import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="elasticsearch_django_migrate", # Replace with your own username
    version="0.0.1",
    author="Li Zhiyuan",
    author_email="forlearn_lzy@163.com",
    description="Migrate elasticsearch Document represented by python into Elasticsearch index",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/amazinglzy/elasticsearch_migrate",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
