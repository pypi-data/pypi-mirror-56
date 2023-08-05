




from codecs import open
from os import path

from setuptools import setup ,Extension

here = path.abspath(path.dirname(__file__))
try:
    # Try to format our PyPi page as rst so it displays properly
    import pypandoc

    with open('README.md', 'rb') as read_file:
        readme_text = read_file.readlines()
    # Change our README for pypi so we can get analytics tracking information for that separately
    readme_text = [row.decode() for row in readme_text]

    long_description = pypandoc.convert(''.join(readme_text), 'rst', format='md')
except ImportError:
    print('!' * 64)
    print('!' * 64)
    print('pypandoc (and possibly pandoc) are not installed.')
    print('This means the PyPi package info will be formatted as .md instead of .rst.')
    print('If you are encountering this before uploading a PyPi distribution, please install these')
    print('!' * 64)
    print('!' * 64)
    # Get the long description from the README file
    with open(path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()


setup(
    name='brainless',
    version=open("brainless/_version.py").readlines()[-1].split()[-1].strip("\"'"),
    description='Automated Machine Learning for production and analytics',
    long_description=long_description,
    url='https://github.com/darvis-ai/Brainless',
    author='Darvis.ai Team',
    author_email='loaiabdalslam@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    keywords=[
        'machine learning', 'data science', 'automated machine learning', 'regressor', 'regressors',
        'regression', 'classification', 'classifiers', 'classifier', 'estimators', 'predictors',
        'XGBoost', 'Random Forest', 'sklearn', 'scikit-learn', 'analytics', 'analysts',
        'coefficients', 'feature importances','darvis-ai','darvis-research',
        'analytics', 'artificial intelligence', 'subpredictors', 'ensembling', 'stacking',
        'blending', 'feature engineering', 'feature extraction', 'feature selection', 'production',
        'pandas', 'dataframes', 'machinejs', 'deep learning', 'tensorflow', 'deeplearning',
        'lightgbm', 'gradient boosting', 'gbm', 'keras', 'production ready', 'test coverage'
    ],
    packages=['brainless'],

    # We will allow the user to install XGBoost themselves. Since it can be difficult to
    # install, we will not force them to go through that install challenge if they're just
    # checking out the package and want to get running with it quickly.
    install_requires=[
        'coveralls>=1.5.0',
        'dill>=0.2.5',
        'h5py>=2.7.0',
        'lightgbm>=2.0.11',
        'nose>=1.3.0',
        'numpy>=1.11.0',
        'pandas>=0.18.0',
        'pathos>=0.2.1',
        'scikit-learn>=0.18.1',
        'scipy>=0.14.0',
        'six>=1.11.0',
        'sklearn-deap2>=0.2.1',
        'tabulate>=0.7.5',
        'tables>=3.4.0',
    ],
    test_suite='nose.collector',
    tests_require=['nose', 'coveralls'])
