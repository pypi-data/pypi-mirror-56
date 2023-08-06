from setuptools import setup, find_packages

setup(name="basestego",
      version="1.1a",
      description="Steganography with base64",
      author="Sergey Belousov",
      author_email="bijereg@gmail.com",
      packages=find_packages(),
      python_requires=">=3.6",
      test_suite="tests")
