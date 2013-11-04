from setuptools import setup, find_packages
setup(
    name = 'breadtrip',
    version = '0.9',
    packages = find_packages(),
    #scripts = ['say_hello.py'],

    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst'],
        # And include any *.msg files found in the 'hello' package, too:
        'hello': ['*.msg'],
    },

    # metadata for upload to PyPI
    author = 'breadtrip',
    author_email = 'pythoner@breadtrip.com',
    description = 'this is private package that we use',
    license = 'BSD',
    keywords = 'breadtrip',
    url = "http://lib.breadtrip.com/python",
)
