from setuptools import setup, find_packages

setup(
    name = "django-segmented-uploads",
    version = "0.0.1",
    packages=find_packages(),
    classifiers = [
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Framework :: Django',
    ],
    install_requires=[
        'django',
    ],
)
