from setuptools import setup, find_packages

setup(
    name="my_city_greeting",
    version='1.0.0',
    description="test description.",
    long_description="test long description",
    author="Dovhanenko Mykhailo",
    author_email="mdovha@softserveinc.com",
    url="https://github.com/ement06/my-package",
    license="MIT",
    py_modules=['greeting'],
    install_requires=[
        'requests',
        'Click',
        'Jinja2'
    ],
    # entry_points='''
    #     [console_scripts]
    #     greeting=city:weather [Lviv]
    # ''',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',      # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   # Again, pick a license
        'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    include_package_data=True,
    python_requires='>=3.6',
)