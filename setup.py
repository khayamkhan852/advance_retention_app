from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in advance_retention_app/__init__.py
from advance_retention_app import __version__ as version

setup(
	name="advance_retention_app",
	version=version,
	description="A custom Frappe Application that will introduce Advance Invoice payment and deduction in sales invoice",
	author="Khayam Khan",
	author_email="khayamkhan852@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)