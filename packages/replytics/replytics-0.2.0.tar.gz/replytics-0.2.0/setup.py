import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="replytics",
	version="0.2.0",
	author="mat",
	author_email="pypi@matdoes.dev",
	description="Easily track your statistics for Repl.it projects!",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://replytics.matdoes.dev",
	packages=setuptools.find_packages(),
	install_requires='websocket-client',
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
)