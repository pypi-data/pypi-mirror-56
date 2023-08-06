from setuptools import setup

setup(
    name = 'talkweb',
    version = '1.0',
    license = 'Apache Software License',
    url = 'http://www.github.com/pytalkweb',
    description = "A small framework for developing web applications",
    long_description = __doc__,
    author = 'Madhukumar Seshadri',
    author_email = 'madhuseshadri@icloud.com',
    zip_safe = False,
    platforms = 'any',
    packages = [
	    'talkweb',
    ],
    include_package_data=True,
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
