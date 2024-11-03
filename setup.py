from setuptools import setup, find_packages

setup(
    name='django-logging-easy',
    version='0.2',
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    description='A Django app to log model changes',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/hasan-furkan/django-model-logger',
    author='Hasan Furkan',
    author_email='hsnfrkn32@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 3.2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
    ],
    install_requires=[
        'Django>=3.2',
    ],
) 