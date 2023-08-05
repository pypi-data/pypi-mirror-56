import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ems-generator-pkg-MarkoDS",
    version="0.0.6",
    author="Marko Kauzlarić",
    author_email="marko@discoveryspecialists.com",
    description="Library to generate .ad1, .ad2, .veh, .env by CIECA \
        estimate management standard",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/acdcorp/autolink_ems_generator",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'dbf',
    ],
    python_requires='>=3.7',
)
