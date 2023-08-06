import setuptools

print(setuptools.find_packages())

setuptools.setup(
    name="cloudwright_atlassian_jira",
    version="0.0.0",
    author="cloudwright",
    url="https://cloudwright.io",
    author_email="founders@cloudwright.io",
    description="cloudwright_atlassian_jira",
    packages=setuptools.find_packages(),
    install_requires=[ ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
)
