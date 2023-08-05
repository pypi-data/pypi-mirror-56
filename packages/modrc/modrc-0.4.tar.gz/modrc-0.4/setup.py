from os.path import abspath, dirname, join
from setuptools import setup


this_dir = abspath(dirname(__file__))
with open(join(this_dir, 'README.md'), encoding='utf-8') as file:
    long_description = file.read()

setup(
    name='modrc',
    description='The CLI to make managing your config files across systems easier.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['modrc'],
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    install_requires=['click', 'clint', 'distro', 'pyyaml'],
    entry_points={
        'console_scripts': [
            'modrc = modrc.__main__:main'
        ]
    },
    license='MIT',
    keywords='cli dotfiles config',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Utilities'
    ]
)
