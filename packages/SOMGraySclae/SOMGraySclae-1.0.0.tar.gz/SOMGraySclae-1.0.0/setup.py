import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


install_requires=[
"cycler==0.10.0",
"decorator==4.4.1",
"httplib2==0.14.0",
"imageio==2.6.1",
"joblib==0.14.0",
"kiwisolver==1.1.0",
"matplotlib==3.1.1",
"networkx==2.4",
"nltk==3.4.5",
"numpy==1.17.3",
"opencv-python==4.1.2.30",
"pandas==0.25.3",
"Pillow==6.2.1",
"pyparsing==2.4.4",
"python-dateutil==2.8.1",
"pytz==2019.3",
"PyWavelets==1.1.1",
"scikit-image==0.16.2",
"scikit-learn==0.21.3",
"scipy==1.3.1",
"six==1.13.0",
"sklearn==0.0",
]


setuptools.setup(
    name="SOMGraySclae", # Replace with your own username
    version="1.0.0",
    author="yelhuang",
    author_email="xiegeixiong@gmail.com",
    description="Using mainifest to improve a grayscale method based on Color-to-gray conversion using ISOMAP [Cui et al. 2010]",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/freedomofme/Grayscale",
    project_urls={
        "Bug Reports": "https://github.com/freedomofme/Grayscale/issues",
        "Source": "https://github.com/freedomofme/Grayscale",
    },
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries",
    ],
    python_requires='>=3.6',
)