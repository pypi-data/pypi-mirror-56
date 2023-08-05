from setuptools import setup

setup(
    name='terra_python_plugin',
    packages = ['terra_python_plugin'],
    version='2.0',
    url='https://D-Scipher@bitbucket.org/terragonengineering/kafka-python-plugin.git',
    license='MIT',
    author='Adeyeye Timothy',
    author_email='adeyeyetimothy33@gmail.com',
    description='A python plugin to send data(json) from any data platform to a connected API.',
    install_requires=[            # I get to this in a second
            'requests',
      ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',      # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   # Again, pick a license
        'Programming Language :: Python :: 3',
        # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
      ],
)
