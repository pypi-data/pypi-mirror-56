from setuptools import setup, find_packages

setup(
    name='haxball.py',
    author='Point#4171',
    url='https://github.com/Pointsz/haxball.py',
    version='1.0.2',
    packages=find_packages(),
    install_requires=['pypeteer'],
    description='Haxball web module.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='MIT License',
    keywords=['haxball', 'haxball.py'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Natural Language :: Portuguese (Brazilian)',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)