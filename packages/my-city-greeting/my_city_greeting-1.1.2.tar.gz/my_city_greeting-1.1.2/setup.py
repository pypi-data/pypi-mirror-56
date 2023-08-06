from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="my_city_greeting",  # Required
    version='1.1.2',  # Required
    description="test description.",  # Optional
    long_description=long_description,  # Optional
    long_description_content_type='text/markdown',  # Optional
    author="Dovhanenko Mykhailo",  # Optional
    author_email="mdovha@softserveinc.com",  # Optional
    url="https://github.com/ement06/my-package",  # Optional
    license="MIT",
    py_modules=['greeting'],  # Optional
    install_requires=[  # Optional
        'requests',
        'Click',
        'Jinja2'
    ],
    keywords='sample test setuptools',  # Optional
    packages=find_packages(),  # Required
    classifiers=[  # Optional
        'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',      # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   # Again, pick a license
        'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    include_package_data=True,  # Optional
    python_requires='>=3, !=2.7, <4',  # Optional
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/ement06/my-package/issues',
        'Funding': 'https://donate.pypi.org',
        'Say Thanks!': 'http://saythanks.io/to/example',
        'Source': 'https://github.com/ement06/my-package',

    },

)


