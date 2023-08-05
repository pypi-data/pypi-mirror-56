from setuptools import find_packages, setup

setup(
    name='DLHelper',
    packages=find_packages(),
    version='0.0.9.5',
    license='MIT',
    description='Tensorflow/keras based toolset to speed up DL model creation and training',
    author='Lukas Norbutas',
    author_email='lukas.norbutas@gmail.com',
    url='https://github.com/user/LukasNorbutas',
    download_url='https://github.com/LukasNorbutas/DLHelper',
    keywords=[],
    install_requires=[
        'numpy',
        'pandas',
        'matplotlib',
        'seaborn',
        'scikit-image',
        'scikit-learn',
        'scikit-optimize',
        'tensorflow>=2',
    ],
)
