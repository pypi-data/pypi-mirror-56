import setuptools

'''
IMPORTANT!
Use python 2 to run setuptools. Otherwise this will end up as an package
at PyPi and we want it to be a module.

Commands to publish
python setup.py sdist bdist_wheel
twine upload dist/*

'''

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="super_simple_test_sequencer",
    version="0.0.1",
    license='MIT License',
    author="JOT Automation Ltd.",
    author_email="rami.rahikkala@jotautomation.com",
    description="Super simple test sequencer for production testing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jotautomation/gaiapythonclient",
    py_modules=['gaiaclient'],
    install_requires=['json2html'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
