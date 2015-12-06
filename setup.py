from setuptools import find_packages, setup

dependencies = [] #removed original dependencies

setup(
    name='koto',
    version='0.1.0',
    url='https://github.com/shukmeister/koto',
    license='BSD', #what is BSD license
    author='Ben Shukman',
    author_email='shukipost@gmail.com',
    description='Track Communications in your Terminal ',
    long_description=__doc__,
    packages=find_packages(exclude=['tests']), #mebbe change dis
    package_data={'':['configs.txt']}, #mebbe change dis
    include_package_data=False, #changed from True
    zip_safe=False,
    platforms='any',
    install_requires=dependencies, #mebbe change dis
    entry_points={
        'console_scripts': [
          'koto=koto.koto:main' #what dis? originally: 'find_email=find_email.find_email:main'
        ]
    },
    classifiers=[
        # As from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        # 'Development Status :: 1 - Planning',
          'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)