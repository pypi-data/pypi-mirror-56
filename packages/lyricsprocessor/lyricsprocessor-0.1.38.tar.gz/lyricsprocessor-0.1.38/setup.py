from setuptools import setup, find_namespace_packages

def readme():
    with open("README.rst") as f:
        return f.read()

setup(
    name='lyricsprocessor',
    packages = find_namespace_packages(), 
    python_requires='>=3.6',
    version='0.1.38',
    description='Lyrics processing code',
    long_description=readme(),
    classifiers=[
                    "Programming Language :: Python :: 3.7",
                    "License :: OSI Approved :: MIT License",
                    "Operating System :: OS Independent"
                ],
    keywords='lyricsgenius genius lyrics',
    url='https://github.com/Mitchwatts93/lyrics_generator',
    author='https://github.com/Mitchwatts93',
    author_email='',
    license='MIT',
    install_requires = [
                        'pandas>=0.23.4',
                        'argparse>=1.1',
                        'lyricsgenius>=1.8.0',
                        'tables>=3.6.1'
                        ],
    include_package_data=True,
    test_suite='nose.collector',
    tests_require=['nose'],
    entry_points={
        "console_scripts": [
                            'get_processed_lyrics = lyricsprocessor.lyrics_generation_script:main'
                            ]
                    },
    )
