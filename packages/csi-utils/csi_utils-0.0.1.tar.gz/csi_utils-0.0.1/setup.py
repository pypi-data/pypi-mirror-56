from setuptools import setup
__version__ = "0.0.1"


setup(
    name="csi_utils",
    version=__version__,
    author="ykone",
    author_email="245403188gm@gmail.com",
    #    url='https://github.com/ykoneee/k4a-python',
    description="utils for Wifi CSI data process",
    long_description="",
    packages=["csi_utils"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.5, <4",
    install_requires=["zmq", "numpy"],
)
