from setuptools import setup, find_packages


setup(
    name='TimeWheel',
      version='0.0.2',
      description='Python implementation of time wheel,Task runer,Cache',
      url='https://www.pkold.com',
      author='zhenruyan',
      author_email='baiyangwangzhan@hotmail.com',
      license='WTFPL',
      packages=find_packages(),
      zip_safe=False,
      platforms=["linux"],
      long_description=open('README.rst').read(),
classifiers=[
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries'
    ],include_package_data=True,
          )