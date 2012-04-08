#from distutils.core import setup
from setuptools import setup, find_packages

# http://guide.python-distribute.org/quickstart.html
# python setup.py sdist
# python setup.py register
# python setup.py sdist upload
# pip install python-qssertions
# pip install python-qssertions --upgrade --no-deps
# Manual upload to PypI
# http://pypi.python.org/pypi/django-dynamic-fixture
# Go to 'edit' link
# Update version and save
# Go to 'files' link and upload the file


tests_require = [
    'nose==1.1.2',
]

install_requires = [
]

setup(name='python-qssertions',
      url='https://github.com/paulocheque/python-qssertions',
      author="paulocheque",
      author_email='paulocheque@gmail.com',
      keywords='python django testing fixture',
      description='Library with additional assertions to help creation of good automated tests, including some special assertion that create additional test cases automatically like assertValidation.',
      license='MIT',
      classifiers=[
          'Operating System :: OS Independent',
          'Topic :: Software Development'
      ],

      version='0.1.0',
      install_requires=install_requires,
      tests_require=tests_require,
      test_suite='nose.collector',
      extras_require={'test': tests_require},

      packages=find_packages(),
)

