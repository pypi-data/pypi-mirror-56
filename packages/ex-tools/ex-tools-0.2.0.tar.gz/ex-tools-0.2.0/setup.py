from setuptools import setup

setup(
    name='ex-tools',
    version='0.2.0',
    description='Tools that include/extend functools/itertools +alpha',
    url='https://github.com/yu-ichiro/ex-tools',
    author='Yuichiro Luke Smith',
    author_email='yuichiro.luke@gmail.com',
    license='MIT',
    packages=['ex_tools', 'ex_tools.functools', 'ex_tools.itertools'],
    zip_safe=False
)
