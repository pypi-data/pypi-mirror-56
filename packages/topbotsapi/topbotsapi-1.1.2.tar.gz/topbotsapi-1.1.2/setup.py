import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="topbotsapi",
    version="1.1.2",
    author="Mister Jevil",
    author_email="dogasezer2002@gmail.com",
    description="Top Discord Bots Resmi api",
    url="https://topdiscordbots.tk",
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
)