from setuptools import setup, find_packages

setup(
    name="shadedb-api",
    version="0.1.8",
    description="The official, high-performance Python client for ShadeDB cloud instances. ShadeDB provides a streamlined, developer-first approach to cloud data management. This library is designed to be the permanent interface for ShadeDB, ensuring a seamless transition from development to full-scale production. Currently in mvp stage",
    author="Shade",
    author_email="adesolasherifdeen3@gmail.com",
    packages=find_packages(),
    install_requires=[
        'requests',
        'shadeDB'
    ],
    entry_points={
        "console_scripts": [
            "shadedb-api-init=shadedb_api.console.__init__:__saver__",
            "shadedb-api=shadedb_api.console.cli:__main__",
        ]
    },
    include_package_data=True,
    python_requires='>=3.11',
    license="GPL-3.0",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    project_urls={
        "GitHub": "https://github.com/harkerbyte",
        "Facebook": "https://facebook.com/harkerbyte",
        "Whatsapp" : "https://whatsapp.com/channel/0029Vb5f98Z90x2p6S1rhT0S",
        "Youtube" : "https://youtube.com/@harkerbyte",
        "Instagram": "https://instagram.com/harkerbyte"
    },
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
)