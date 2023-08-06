import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name = 'PyMonoBankAPI',
    version="0.1",
    author="Tynukua",
    author_email = 'tynuk.ua@gmail.com',
    description = 'simple lib for monobank API:)',
    
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/Tynukua/mono',
    packages=setuptools.find_packages(),
    requires_python='>=3.5',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        "Operating System :: OS Independent",] ,
    install_requires=[
        'requests']
    )