from io import open

from setuptools import find_packages, setup

with open("requirements.txt") as f:
    parsed_requirements = f.read().splitlines()
# remove blank lines and comments
parsed_requirements = [
    x.strip()
    for x in parsed_requirements
    if ((x.strip()[0] != "#") and (len(x.strip()) > 3))
]


setup(
    name="farm-haystack",
    version="0.1.0.post2",
    author="Malte Pietsch, Timo Moeller, Branden Chan, Tanay Soni",
    author_email="malte.pietsch@deepset.ai",
    description="Neural Question Answering at Scale. Use modern transformer based models like BERT to find answers in large document collections",
    long_description=open("README.rst", "r", encoding="utf-8").read(),
    long_description_content_type="text/x-rst",
    keywords="QA Question-Answering Reader Retriever BERT roberta albert squad mrc transfer-learning language-model transformer",
    license="Apache",
    url="https://github.com/deepset-ai/haystack",
    download_url="https://github.com/deepset-ai/haystack/archive/0.1.0.tar.gz",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    install_requires=parsed_requirements,
    python_requires=">=3.6.0",
    tests_require=["pytest"],
    classifiers=[
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)
