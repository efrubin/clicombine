from setuptools import setup

setup(name='clicombine',
      version='0.1',
      description='Image combination tool for CASA',
      url='https://github.com/efrubin/clicombine',
      author='Elias Rubin',
      author_email='erubin@princeton.edu',
      license='MIT',
      packages=['clicombine'],
      install_requires=[
          'drive-casa'],
      scripts=['bin/cli-combine'],
      zip_safe=False)
