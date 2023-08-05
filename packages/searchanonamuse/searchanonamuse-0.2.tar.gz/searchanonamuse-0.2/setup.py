from setuptools import setup

setup(name='searchanonamuse',
      version='0.02',
      description='Receives login, password and path to ChromeDriver.exe as parameters and has a method'
                  ' that do the search in MAM and returns the HTML resulting of the search',
      url='https://github.com/samuelsonsev/searchanonamuse',
      author='Sam',
      author_email='none@example.com',
      license='MIT',
      packages=['searchanonamuse'],
      zip_safe=False, install_requires = ['selenium'])
