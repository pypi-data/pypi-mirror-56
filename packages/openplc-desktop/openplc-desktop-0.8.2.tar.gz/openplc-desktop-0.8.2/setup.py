import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

with open("version.txt", "r") as fh:
    version = fh.read()

setuptools.setup(
    name="openplc-desktop", # Replace with your own username
    version=version,
    author="Pedro Morgan",
    author_email="openplc@daffodil.uk.com",
    description="OpenPLC Desktop",
    long_description=long_description,
    #long_description_content_type="text/markdown",
    url="https://openplcproject.gitlab.io/openplc_desktop/",
    project_urls={
        "Bug Tracker": "https://gitlab.com/openplcproject/openplc_desktop/issues",
        "Documentation": "https://openplcproject.gitlab.io/openplc_desktop/",
        "Source Code": "https://gitlab.com/openplcproject/openplc_desktop",
    },
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    scripts=['openplc-desktop.py'],
)