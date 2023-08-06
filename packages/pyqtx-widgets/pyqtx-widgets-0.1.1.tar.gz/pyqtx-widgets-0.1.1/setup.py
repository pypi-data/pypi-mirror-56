import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

with open("version.txt", "r") as fh:
    version = fh.read()

setuptools.setup(
    name="pyqtx-widgets", # Replace with your own username
    version=version,
    author="Pedro Morgan",
    author_email="pete@daffodil.uk.com",
    description="pyqtx Widgets",
    long_description=long_description,
    #long_description_content_type="text/markdown",
    url="https://pyqtx.gitlab.io/pyqtx_widgets/",
    project_urls={
        "Bug Tracker": "https://gitlab.com/pyqtx/pyqtx_widgets/issues",
        "Documentation": "https://pyqtx.gitlab.io/pyqtx_widgets/",
        "Source Code": "https://gitlab.com/pyqtx/pyqtx_widgets",
    },
    packages=setuptools.find_packages(exclude="docs"),
    # package_data={
    #     '': ['*.png', '*.md', "*.html", "*.ini"],
    # },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.4',
    scripts=['pyqtx-demo.py'],
    include_package_data=True,
    install_requires=[
       'mistune',
       'qtawesome',
    ],

)
