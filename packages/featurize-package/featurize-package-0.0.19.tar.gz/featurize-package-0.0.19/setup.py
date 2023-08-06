import setuptools


setuptools.setup(
    name='featurize-package',
    description='Official packages for featurize.',
    version='0.0.19',
    packages=setuptools.find_packages(),
    url="https://github.com/louis-she/featurize-package",
    author='louis',
    author_email='chenglu.she@gmail.com',
    keywords='pytorch minecraft',
    include_package_data=True,
    install_requires=[
        'featurize-jupyterlab',
        'torchvision>=0.4.0',
        'albumentations',
        'torch',
        'pandas',
        'numpy',
        'opencv-python',
        'scikit-learn',
        'pretrainedmodels',
        'kaggle'
    ],
)
