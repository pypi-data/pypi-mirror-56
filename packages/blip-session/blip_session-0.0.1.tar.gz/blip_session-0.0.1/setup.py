from setuptools import setup


setup(
    name='blip_session',
    packages=['blip_session'],
    version='v0.0.1',
    license='MIT',
    description='Provide a session class from requests module to use as a BLiP Session.',
    author='Gabriel Rodrigues dos Santos',
    author_email='gabrielr@take.net',
    url='https://github.com/chr0m1ng/blip-session',
    download_url='https://github.com/chr0m1ng/blip-session/archive/v0.0.1.tar.gz',
    keywords=['lime', 'blip', 'chatbot'],
    install_requires=[
        'requests'
    ],
    classifiers=[
        # "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ]
)
