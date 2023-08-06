import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

with open("ogtstatic/version.txt", "r") as fh:
    version = fh.read()

setuptools.setup(
    name="open-geotechnical", # Replace with your own username
    version=version,

    author="Pedro Morgan",
    author_email="ogt@daffodil.uk.com",

    description="Open Geotechnical",
    long_description=long_description,

    url="https://open-geotechnical.gitlab.io/ogt_py/",
    project_urls={
        "Bug Tracker": "https://gitlab.com/open-geotechnical/ogt_py/issues",
        "Documentation": "https://open-geotechnical.gitlab.io/ogt_py/",
        "Source Code": "https://gitlab.com/open-geotechnical/ogt_py",
    },

    packages=setuptools.find_packages(exclude="docs"),
    include_package_data=True,
    package_data={
        'ogtstatic': ['*'],
    },

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
    ],

    python_requires='>=3.4',
    install_requires=[
       'mistune',
       'openpyxl',
        "pyyaml",
        "geojson",
        "flask"
    ],

    scripts=[
        'ogt-cli.py',
        'ogt-desktop.py',
        'ogt-server.sh'
    ],
    data_files=[
        ('share/icons/32x32/apps', ['etc/open-geotechnical.png']),
        ('share/applications', ['etc/open-geotechnical.desktop']),
    ],
)
