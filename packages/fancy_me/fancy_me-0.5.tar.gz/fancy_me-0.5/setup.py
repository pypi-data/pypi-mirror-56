from setuptools import setup, find_packages

pkgs = ['fancy_me', "fancy_me.ws", "fancy_me.udp"]

print(pkgs)
setup(
    author="somewheve",
    version=0.5,
    name="fancy_me",
    packages=pkgs,
    install_requires=["websockets"],
    author_email='somewheve@gmail.com',
    license="MIT"
)
