from setuptools import setup

setup(
    
    name = 'smogn',
    version = '0.0.1',
    description = 'A Python implementation of Synthetic Minority Over-Sampling Technique for Regression with Gaussian Noise (SMOGN)',
    long_description = open('README.md').read(),
    long_description_content_type = "text/markdown",
    author = 'Nick Kunz',
    author_email = 'nick.kunz@columbia.edu',
    url = 'https://github.com/nickkunz/smogn',
    license = 'GPLv3',
    classifiers = [
        
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Education',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
        ],
    
    keywords = [
        
        'over-sampling',
        'synthetic data',
        'machine learning',
        'pre-processing'
    ],
    
    packages = ['smogn'],
    include_package_data = True,
    install_requires = ['numpy', 'pandas'],
    test_suite = 'nose.collector',
    tests_require = ['nose']
)
