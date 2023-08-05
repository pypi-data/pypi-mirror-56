from setuptools import setup, find_packages
import json

with open('metadata.json', encoding='utf8') as f:
    metadata = json.load(f)

requirements = []
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open('README.md', encoding='utf8') as f:
    long_description = f.read()

setup(
    name="modmailtranslation",
    version=metadata["version"],
    description="A translator utility package for modmail-plugins",
    long_description=long_description,
    packages=find_packages(),
    license="GPLv3",
    url="https://github.com/officialpiyush/modmailtranslation",
    author="Piyush Bhangale",
    author_email="bhangalepiyush@gmail.com",
    keywords=["modmail", "translator", "translations"],
    install_requires=requirements,
    python_requires='>=3.5',
    project_urls={
        'Source Code': 'https://github.com/officialpiyush/modmailtranslation',
        'Issue Tracker': 'https://github.com/officialpiyush/modmailtranslation/issues',
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Natural Language :: English'
    ]
)
