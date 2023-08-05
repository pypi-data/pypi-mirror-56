from setuptools import setup
 
setup(
    name="helllohuirong",
    version="0.1",
    scripts=['cluster.py'],
    data_files = [('.', ['data-1.csv'])],
    install_requires=['matplotlib', 'pandas'],
    author="Me",
    author_email="zhuhuirong_sh@hotmail.com",
    description="This is an Example Package",
    classifiers=[
        'License :: OSI Approved :: Python Software Foundation License'
    ]
)