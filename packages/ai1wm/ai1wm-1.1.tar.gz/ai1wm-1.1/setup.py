from distutils.core import setup

setup(
    name='ai1wm',
    packages=['ai1wm'],
    version='1.1',
    license='MIT',
    description='Packs/Unpacks `All-in-One WP Migration` packages',
    author='Sander Wang',
    author_email='sw.online@outlook.com',
    url='https://github.com/sanderwang/ai1wm',
    download_url='https://github.com/sanderwang/ai1wm/archive/1.1.tar.gz',
    keywords=['WordPress', 'All-in-One WP Migration'],
    install_requires=[
        'six',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
