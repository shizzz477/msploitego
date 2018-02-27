from setuptools import setup, find_packages

setup(
    name='oscp',
    author='Marc Gurreri',
    version='1.0',
    author_email='me@me.com',
    description='OSCP based transforms',
    license='GPL',
    packages=find_packages('src'),
    package_dir={ '' : 'src' },
    zip_safe=False,
    package_data={
        '' : [ '*.gif', '*.png', '*.conf', '*.mtz', '*.machine' ] # list of resources
    },
    install_requires=[
        'canari==1.1',
        'lxml',
        'python-libnmap',
        'python-nmap'
    ],
    dependency_links=[
        # custom links for the install_requires
    ]
)
