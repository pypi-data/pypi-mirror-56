from setuptools import setup

setup(name='molywood',
      version='0.1',
      description='A script to automate the production of molecular movies in VMD',
      url='https://gitlab.com/KomBioMol/pyvmd_movies',
      author='Milosz Wieczor',
      author_email='milafternoon@gmail.com',
      license='GNU GPLv3',
      packages=['molywood'],
      entry_points={'console_scripts': ['molywood = molywood.moly:molywood']},
      python_requires='>=3.4',
      zip_safe=False)
