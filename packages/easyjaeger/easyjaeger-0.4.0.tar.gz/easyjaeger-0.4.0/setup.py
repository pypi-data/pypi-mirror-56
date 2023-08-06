from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

install_requires = [
    'aiozipkin==0.6.0', 'aiohttp'
]

test_require = {
    'pytest',
    'pytest-asyncio',
    'aiozipkin==0.6.0'
}

setup(
    name='easyjaeger',
    version='0.4.0',
    description='Helper for easy breezy jaeger/zipkin in asyncio python services',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='http://github.com/borisrozumnuk/cognitojwt',
    author='Michail Shatalov',
    author_email='misha.shatalow@gmail.com',
    license='MIT',
    platforms='Any',
    install_requires=install_requires,
    keywords='zipkin jaeger tracing aiozipkin',
    packages=find_packages(exclude=('tests')),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Operating System :: OS Independent',
    ],
    zip_safe=False
)
