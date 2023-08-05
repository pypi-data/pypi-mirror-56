from setuptools import setup, find_packages


with open('README.md', encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='django-pianoforte',
    version='0.1.0',
    description='Pianoforte-style django basic utilities',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/team-pianoforte/django-piano',
    author='z@kuro',
    author_email='z@kuro.red',
    license='MIT',
    keywords='django utility pianoforte',
    packages=find_packages(exclude=['demo*']),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
    ],
)
