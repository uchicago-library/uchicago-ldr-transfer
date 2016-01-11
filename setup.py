from distutils.core import setup

setup(
    name = 'uchicagoldrtransfer',
    version = '1.0.0',
    author = "Tyler Danstrom,Fred Seaton,Keith Waclena",
    author_email = "tdanstrom@uchicago.edu,Fred Seaton,Keith Waclena",
    packages = ['uchicagoldrtransferring'],
    description = """\
    A command line module for ldr accessioners to transfer a new directory into
    the repository and transfer all ownership of resulting 
    directory to repository user, repository group
    """,
    keywords = ["uchicago","repository","file-level","processing"],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "Operating System :: Unix",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
    install_requires = [])
                        
