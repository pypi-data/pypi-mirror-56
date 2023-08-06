from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

install_requires = [
    'djangorestframework',
    'django-imagekit',
    'django-road',
    'content-licencing',
    'anycluster',
    'rules==2.1',
    'django-el-pagination',
    'django-octicons',
    'django-countries',
    'django-cors-headers',
    'Pillow',
]

setup(
    name='localcosmos_server',
    version='0.4.1',
    description='LocalCosmos Private Server. Run your own server for localcosmos.org apps.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='The MIT License',
    platforms=['OS Independent'],
    keywords='django, localcosmos, localcosmos server, biodiversity',
    author='Thomas Uher',
    author_email='thomas.uher@sisol-systems.com',
    url='https://github.com/SiSol-Systems/localcosmos-server',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    include_package_data=True,
    install_requires=install_requires,
)
