from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='lgm',
    version='0.1.0',
    description='Lightweight python3 library for natural LanGuage Modeling (LGM), useful for deep learning and reinforcement learning experiments with natural language data.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/abrsvn/lgm',
    author='Adrian Brasoveanu',
    author_email='abrsvn@gmail.com',
    license='GNU General Public License v3.0',
    packages=['lgm'],
    zip_safe=False
)
