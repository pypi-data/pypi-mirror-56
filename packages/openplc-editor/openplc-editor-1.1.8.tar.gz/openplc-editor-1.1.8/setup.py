import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="openplc-editor", # Replace with your own username
    version="v1.1.8",
    author="OpenPLC Team",
    author_email="openplc@daffodil.uk.com",
    description="OpenPLC Editor",
    long_description=long_description,
    #long_description_content_type="text/markdown",
    url="https://openplcproject.com",
    project_urls={
        "Bug Tracker": "https://gitlab.com/openplcproject/openplc_editor/issues",
        "Documentation": "https://openplcproject.gitlab.io/openplc_editor/",
        "Source Code": "https://gitlab.com/openplcproject/openplc_editor",
    },
    packages=setuptools.find_packages(exclude="docs"),
    package_data={
        '': ['*.png', '*.md', "*.html", "*.ini",
             "*.c", "*.h", "*.cpp",
             "*.txt", "*.yaml", "*.yml", "*.xml"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.6',
    scripts=['openplc-editor.py'],
    include_package_data=True,
    install_requires=[
        'zeroconf==0.19.1',
        'numpy==1.16.5',
        "matplotlib==2.0.2",
        "lxml",
        "sslpsk",
        "wxPython"

    ],
    data_files = [
        ('share/applications', ['openplc-editor.desktop']),
    ],
)
