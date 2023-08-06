from distutils.core import setup
setup(
    name='pwlf',
    version=open('pwlf/VERSION').read().strip(),
    author='Charles Jekel',
    author_email='cjekel@gmail.com',
    packages=['pwlf'],
    package_data={'pwlf': ['VERSION']},
    url='https://github.com/cjekel/piecewise_linear_fit_py',
    license='MIT License',
    description='fit piecewise linear functions to data',
    long_description=open('README.rst').read(),
    platforms=['any'],
    install_requires=[
        "numpy >= 1.14.0",
        "scipy >= 0.19.0",
        "pyDOE >= 0.3.8",
    ],
    extras_require={
        'PiecewiseLinFitTF':  ["tensorflow < 2.0.0"]
    }
)
