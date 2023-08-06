import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="OAuthWb",  # Replace with your own username
    version="0.0.5",
    author="DAHANGZAIYA",
    author_email="y17505251998@163.com",
    description="weibo_login",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yinbohang/weibo_login",
    packages=setuptools.find_packages(include=['json', 'requests']),
    license="MIT",
    install_requires=['json', 'requests'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
