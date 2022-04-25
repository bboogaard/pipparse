from setuptools import setup


setup(name='pip_parse',
      version='0.1',
      description='Parse pip list output',
      url='https://github.com/bboogaard/pip_parse',
      author='Bram',
      author_email='padawan@hetnet.nl',
      license='MIT',
      packages=['pip_parse'],
      install_requires=[
          'semantic_version==2.9.0'
      ],
      scripts=['bin/pipparse'],
      zip_safe=False)
