import setuptools

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setuptools.setup(
    name='beet',
    version='0.0.1',
    description='Utility for tracking flow of behive with video',
    long_description=readme,
    author="verbetam",
    author_email="comptonrj@appstate.edu",
    url="htps://github.com/verbetam/beet",
    license=license,
    packages=setuptools.find_packages(exclude=('tests', 'docs'))
)
