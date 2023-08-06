from setuptools import setup, find_packages


setup(
    name='restore-mtime',
    version='0.1.0',
    author='Eero Rikalainen',
    author_email='eerorika@gmail.com',
    url='https://github.com/eerorika/restore-mtime',
    description='Command line utility for resotration of modification time (mtime) of files from tar archive into filesystem if the content matches',
    license='MIT',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'restore-mtime = restore_mtime.restore_mtime:main'
        ]
    },
    zip_safe=False
)
