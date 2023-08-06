from setuptools import setup


def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="sycavision",
    version="3.0",
    description="Image processing library for FRC teams.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/enisgetmez/sycavision",
    author="Enis Getmez",
    author_email="enis@enisgetmez.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["sycavision"],
    include_package_data=True,
     install_requires=[            
          'pynetworktables',
          'numpy',
          'argparse',
          'imutils',
          'opencv-python',
          'pyfiglet',
      ],
    entry_points={
        "console_scripts": [
            "sycavision=sycavision.sycavision:main",
        ]
    },
)