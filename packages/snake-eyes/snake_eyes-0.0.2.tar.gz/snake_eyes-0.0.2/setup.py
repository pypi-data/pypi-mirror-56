import setuptools

import snake_eyes_data as snake_eyes

setuptools.setup(
    name='snake_eyes',
    version=snake_eyes.__version__,
    url=snake_eyes.__url__,
    author=snake_eyes.__author__,
    packages=['snake_eyes', 'snake_eyes_data'],
    python_requires='>=3.7.0',
    include_package_data=True,
    data_files=[
        ('', ['README.md', 'CHANGELOG.md']),
    ],
    install_requires=["dyndis", "numpy", 'scipy', 'containerview']
)
