from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(name="pysubmit",
      version="1.0.1",
      description="Versatile computation submission tool",
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://bitbucket.org/Mc_M/pysubmit",
      author="Martin Lellep",
      author_email="martin.lellep@gmail.com",
      license="MIT",
      packages=["pysubmit"],
      install_requires=[
          "jinja2",
      ],
      entry_points = {
        "console_scripts": ['pysubmit=pysubmit.command_line:main'],
      },
      zip_safe=False,
      python_required='>=3.6')
