from setuptools import setup
from incenp.davpoint import __version__

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
        name = 'incenp.davpoint',
        version = __version__,
        description = 'Davfs2 wrapper to mount SharePoint filesystems',
        long_description = long_description,
        long_description_content_type = 'text/markdown',
        author = 'Damien Goutte-Gattat',
        author_email = 'dgouttegattat@incenp.org',
        url = 'https://git.incenp.org/damien/davpoint',
        classifiers = [
            'Development Status :: 3 - Alpha',
            'Environment :: Console',
            'Intended Audience :: End Users/Desktop',
            'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.7',
            ],
        packages = [
            'incenp',
            'incenp.davpoint'
            ],
        entry_points = {
            'console_scripts': [
                'davpoint = incenp.davpoint.__main__:main'
                ]
            }
        )
