from setuptools import setup, find_packages
import os

package_name = "gitlab-events"
package_dir  = "gitlabevents"

with open("README.md", "r") as fh:
    long_description = fh.read()

def fullsplit(path, result=None):
    """
    Split a pathname into components (the opposite of os.path.join) in a
    platform-neutral way.
    """
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == '':
        return [tail] + result
    if head == path:
        return result
    return fullsplit(head, [tail] + result)

# Compile the list of packages available, because distutils doesn't have
# an easy way to do this.
packages, data_files = [], []
root_dir = os.path.dirname(__file__)
if root_dir != '':
    os.chdir(root_dir)

for dirpath, dirnames, filenames in os.walk(package_dir):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'): del dirnames[i]
    if '__init__.py' in filenames:
        packages.append('.'.join(fullsplit(dirpath)))
    elif filenames:
        data_files.append([dirpath, [os.path.join(dirpath, f) for f in filenames]])

setup(
    name=package_name,
    version="0.0.3",
    author="Viktor Prymak",
    author_email="sammorow@gmail.com",
    description="Gitlab events to CSV table",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Iheiko/gitlab-events/",
    packages=packages,
    scripts=["scripts/gitlab-events"],
    install_requires=[
          'termcolor',
          'colorama',
          'python-gitlab',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Topic :: Education",
        'Environment :: Console',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
