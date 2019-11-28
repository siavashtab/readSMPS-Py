from setuptools import setup, find_packages

setup(name='ReadSMPS',
      version='0.0.1',
      description='reading SMPs format files',
      long_description='Using this package the read the SMPS files using GUROBI and python',
      keywords='readSMPS',
      url='https://github.com/siavashtab/readSMPS-Py',
      author='Siavash Tabrizian',
      author_email='stabrizian@smu.edu',
      license='Siavash Tabrizian',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False)
