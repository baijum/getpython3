from setuptools import setup

setup(
    name="getpython3",
    version="0.1",
    description='Website for porting status of packages to Python 3',
    long_description=open('README').read(),
    license='Simplified BSD',
    author='Baiju M.',
    author_email='baiju.m.mail@gmail.com',
    url='http://getpython3.net/',
    platforms=['linux', 'osx', 'win32'],
    py_modules=['py3k'],
    install_requires = ['Flask',
                        'SQLAlchemy',
                        'Flask-SQLAlchemy',
                        'Flask-OpenID',
                        'Flask-Script',
                        'Flask-Gravatar',
                        'captchaimage'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python'],
)
