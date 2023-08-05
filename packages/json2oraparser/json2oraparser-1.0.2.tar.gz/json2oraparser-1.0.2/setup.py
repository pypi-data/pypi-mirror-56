import setuptools

with open("README.md", "r") as f:
    long_desc = f.read()

setuptools.setup(
    name="json2oraparser",
    version="1.0.2",
    author="Abhishek Sinha, Samrat Ghosh, Siddhartha Bhattacharya, Shouvik Das, Sudipta Dey, Subhajit Bhar",
    author_email="ntpythondev@gmail.com",
    description="The 'json2oraparser' library parses a JSON file (nested upto n-th level) according to user given metadata and stores Json data into Oracle database",
    long_description=long_desc,
    long_description_content_type="text/markdown",
	license = "MIT",
    platforms='any',
    url="https://github.com/ntpythondev/json2oraparser.git",
    packages=setuptools.find_packages(),
	package_data={'json2oraparser': ['Config/Config.yml', 'Resources/SQL/*.sql', 'METADATA/*.csv', 'METADATA/*.json', 'METADATA/*.txt']},
	install_requires=['cx_Oracle', 'pandas', 'PyYAML'],
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
		"Development Status :: 4 - Beta"     # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
		#"Intended Audience :: Developers"    # Define that your audience are developers
		#"Topic :: Software Development :: Build Json to Oracle Parser",
    ]   
)