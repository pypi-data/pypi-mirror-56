from setuptools import setup

setup(name='searchanonamuse',
      version='0.01',
      description='Receives the login and password and can be used to search a keyword in myAnonaMuse and return the html',
      url='https://github.com/samuelsonsev/searchanonamuse',
      author='Sam',
      author_email='none@example.com',
      license='MIT',
      packages=['searchanonamuse'],
      zip_safe=False,
      install_requires = ['selenium'])