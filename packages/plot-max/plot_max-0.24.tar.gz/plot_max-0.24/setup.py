from setuptools import setup, find_packages
files = ['plot_max/msyh.ttf']

setup(name='plot_max',
      version='0.24',
      description='high level to use matplotlib',
      url='http://github.com/pringwong',
      author='pring',
      author_email='huppid@qq.com',
      packages=find_packages('plot_max'),
      package_dir={'':'plot_max'},
      include_package_data=True,
      package_data={'plot_max':['msyh.ttf']},
      license='None',
      zip_safe=False)
