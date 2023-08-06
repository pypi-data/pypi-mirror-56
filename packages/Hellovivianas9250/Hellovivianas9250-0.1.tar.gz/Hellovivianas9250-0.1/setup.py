from setuptools import setup

setup(
    name = "Hellovivianas9250",
    version ="0.1",
    scripts = ['week9project.py'],

    data_files = [('.',['data1.csv'])],
    


    install_requires = ['matplotlib','pandas'],

    author = "Me",
    description = "This is my project",
    keywords = "clusters example",

    classifiers=[
        'License :: OSI Approved :: Python Software Foundation License'
    ]
)