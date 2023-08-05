from setuptools import setup, find_packages

setup(name='hackpy',
      version='0.1.5.1',
      description='Full description here: https://github.com/LimerBoy/hackpy/blob/master/README.MD',
      url='https://github.com/LimerBoy/hackpy/blob/master/README.MD',
      author='LimerBoy',
      author_email='LimerBoyTV@gmail.com',
      license='MIT',
      packages=find_packages(),
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: Microsoft :: Windows",
      ],
      install_requires=[
          'wget',
          'getmac',
          'pyperclip',
          'pywin32',
      ],
      include_package_data=True,
      zip_safe=False)
