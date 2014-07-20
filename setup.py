from setuptools import setup


setup(
  name='bump',
  version='1.0.0-dev',
  description='Bumps package version numbers',
  # long_description=open('README.rst').read(),
  license='MIT',
  url='https://github.com/marksteve/bump',
  author='Mark Steve Samson',
  author_email='hello@marksteve.com',
  classifiers=[
      "Programming Language :: Python :: 2.7",
      "Programming Language :: Python :: 3",
      "Programming Language :: Python :: 3.1",
      "Programming Language :: Python :: 3.2",
      "Programming Language :: Python :: 3.3",
  ],
  keywords='bump increment package version',
  zip_safe=False,
  py_modules=['bump'],
  install_requires=['click>=2,<3'],
  # entry_points=dict(console_scripts=['bump = bump:main']),
)
