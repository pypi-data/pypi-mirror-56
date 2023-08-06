from setuptools import setup

def readme():
    with open('Readme.md') as f:
        Readme = f.read()
    return Readme

setup(
    name="br_helper",
    version="0.1.1",
    description="Automate browser the easy way",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/Tornike-Skhulukhia/browser_automation_helper",
    author="Tornike Skhulukhia",
    author_email="Tornike.Skhulukhia.1@iliauni.edu.ge",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    packages=["br_helper"],
    include_package_data=True,
    install_requires=["selenium>=3.141.0", "beautifulsoup4>=4.6.0"],
)
