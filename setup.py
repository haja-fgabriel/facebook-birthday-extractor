from setuptools import setup, find_packages

setup(
    name="facebook-scraper",
    author="Haja Florin-Gabriel",
    description="Scraper for Facebook friends' birthdays",
    author_email="haja.fgabriel@gmail.com",
    package_dir={"": "src/"},
    packages=find_packages("src/")
)