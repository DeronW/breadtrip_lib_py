from setuptools import setup, find_packages
setup(
    name = 'breadtrip',
    version = '0.1',
    packages = find_packages(),
    #scripts = ['say_hello.py'],
    install_requires = ['psycopg2', 'python-dateutil==1.5', 'requests'],

    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst'],
    },

    # metadata for upload to PyPI
    author = 'breadtrip',
    author_email = 'pythoner@breadtrip.com',
    description = 'private library that breadtrip use',
    license = 'BSD',
    keywords = 'breadtrip',
    url = "http://lib.breadtrip.com/python",
)
