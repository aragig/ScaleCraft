from setuptools import setup, find_packages
setup(
    name='ScaleCraft',
    version='0.1.0',
    packages=find_packages(),
    description='画像をリサイズするPythonパッケージ',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Toshihiko Arai',
    author_email='i.officearai@gmail.com',
    license='MIT',
    url='https://github.com/aragig/ScaleCraft',
    install_requires=[
        'pillow==10.2.*',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)
