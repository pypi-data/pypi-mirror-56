from setuptools import setup, find_packages

setup(
    name='pyWireGuard_proto',  # How you named your package folder (MyLib)
    packages=find_packages(exclude=['*.tests', '*.tests.*', 'tests.*', 'tests', 'setup_builder.py']),  # Chose the same as 'name',
    version='2019.12.0',
    # Start with a small number and increase it with every change you make
    license='MIT',  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    long_description='''# pyWireGuard
Python controller for WireGuard.  
Status: Alpha  
More info soon''',
    long_description_content_type='text/markdown',
    description='Controller for WireGuard',  # Give a short description about your library
    author='Yurzs (Yury)',  # Type in your name
    author_email='development+pyWireGuard_proto@yurzs.dev',  # Type in your E-Mail
    url='https://git.yurzs.dev/yurzs/pywireguard',
    # Provide either the link to your github or to your website
    keywords=['wireguard'],  # Keywords that define your package best
    install_requires=[],
    classifiers=[
        'Development Status :: 3 - Alpha',
        # Chose either '3 - Alpha', '4 - Beta' or '5 - Production/Stable' as the current state of your package
        'Intended Audience :: Developers',  # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',  # Again, pick a license
        'Programming Language :: Python :: 3',  # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.6',
    ],
)
