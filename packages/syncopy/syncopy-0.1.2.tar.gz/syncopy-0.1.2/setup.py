import io
import setuptools
import syncopy

setuptools.setup(
    zip_safe=True,
    name=syncopy.__name__,
    version=syncopy.__version__,
    url='http://bitbucket.org/neogeny/' + syncopy.__name__,
    author='Juancarlo Añez',
    author_email='apalala@gmail.com',
    description=syncopy.__name__ + ' implements hierarchical command lines',
    long_description=io.open('README.md', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    license='BSD License',
    packages=setuptools.find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
        ]
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Environment :: Console',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
        'Topic :: Utilities',
    ],
    requires=[
        'docopt',
    ],
    extras_require={
    },
)

