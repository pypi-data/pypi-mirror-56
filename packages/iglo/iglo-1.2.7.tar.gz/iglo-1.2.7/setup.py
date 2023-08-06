from setuptools import setup, find_packages

setup(name='iglo',
      version='1.2.7',
      description='Control iGlo based RGB lights',
      url='http://github.com/jesserockz/python-iglo',
      author='Jesse Hills',
      license='MIT',
      install_requires=[],
      packages=find_packages(exclude=["dist"]),
      zip_safe=True)
