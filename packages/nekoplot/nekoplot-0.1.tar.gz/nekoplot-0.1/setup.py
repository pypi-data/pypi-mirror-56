import setuptools
ver=0.01
rme="""
        Small, WIP plotting lib.
        Similar to Matplotlib, but slightly more options, but only a image. That's okay though aha
    """
setuptools.setup(
    name="nekoplot",
    version=ver,
    author="LazyNeko",
    author_email="lazynekoo@gmail.com",
    description="Small, WIP graphing package.",
    long_description=rme,
    url="http://neko-bot.net/nekoplot",
    packages=setuptools.find_packages(include=["pillow","nbapi"]),
    python_requires=">=3.6"
)