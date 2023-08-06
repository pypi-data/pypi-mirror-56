from distutils.core import setup
setup(
  name='hotool',         # How you named your package folder (MyLib)
  packages=['hotool'],   # Chose the same as "name"
  version='0.1.1000',      # Start with a small number and increase it with every change you make
  license='GPL-3.0',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description='Tools and tricks for python work',   # Give a short description about your library
  author='hotbless',                   # Type in your name
  author_email='hotbless@gmail.com',      # Type in your E-Mail
  url='https://github.com/hotbless/hotool',   # Provide either the link to your github or to your website
  download_url='https://github.com/hotbless/hotool/archive/0.1.1000.tar.gz',
  keywords=['python', 'hotool'],   # Keywords that define your package best
  install_requires=[],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
