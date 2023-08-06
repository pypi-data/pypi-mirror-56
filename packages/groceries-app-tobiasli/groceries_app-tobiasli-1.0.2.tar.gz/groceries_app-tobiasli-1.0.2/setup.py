import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='groceries_app-tobiasli',
                 version='1.0.2',
                 description='App for compiling shopping lists.',
                 author='Tobias Litherland',
                 author_email='tobiaslland@gmail.com',
                 url='https://github.com/tobiasli/groceries_app',
                 packages=['groceries_app',
                           'groceries_app/email_sender',
                           'groceries_app/wunderlist',
                           'groceries_app/test'
                           ],
                 package_data={'': ['groceries_app/cookbook.yaml']},
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 install_requires=['groceries-tobiasli', 'wunderpy2', 'pytest', 'pyyaml'],
                 classifiers=[
                     "Programming Language :: Python :: 3",
                     "License :: OSI Approved :: MIT License",
                     "Operating System :: OS Independent",
                 ],
                 )
