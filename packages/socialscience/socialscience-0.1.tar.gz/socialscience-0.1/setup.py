from setuptools import setup

setup(name='socialscience',
      version='0.1',
      description='',
      url='https://github.com/scarsellifi/socialscience.git',
      author='Marco Scarselli',
      author_email='scarselli@gmail.com',
      license='MIT',
      packages=['socialscience'],
      install_requires=[
          'numpy',
          'pandas',
          'matplotlib',
          'seaborn'
      ],
      zip_safe=False)