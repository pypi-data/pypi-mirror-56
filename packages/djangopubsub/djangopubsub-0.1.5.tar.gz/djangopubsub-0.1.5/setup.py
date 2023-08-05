from setuptools import setup, find_packages

setup(name='djangopubsub',
      version='0.1.5',
      description='Base redis pubsub django wrapper',
      url='https://gitlab.com/kas-factory/packages/django-pubsub',
      author='Antonio @ KF',
      author_email='antonio@kasfactory.net',
      license='MIT',
      packages=find_packages(),
      package_data={'djangopubsub': ['djangopubsub/*',
                                     'djangopubsub/management/*',
                                     'djangopubsub/management/commands/*']},
      install_requires=[
            'Django',
            'kfpubsub>=0.1.3'
      ],
      zip_safe=False
)
