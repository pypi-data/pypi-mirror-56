import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="metro2",
    version="2.0.1",
    author="Ranu Lathi",
    author_email="ranu@peachstreet.com",
    description="Generate metro 2 format for credit reporting to credit bureaus",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/ranupeachstreet/metro2",
    packages=setuptools.find_packages(),
    include_package_data=True,
    py_modules = ['metro2'],
    zip_safe=False,
    license='MIT',
)