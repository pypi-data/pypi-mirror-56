import setuptools

print(setuptools.find_packages())

setuptools.setup(
    name="cloudwright_slack_webhook",
    version="0.0.0",
    author="cloudwright",
    url="http://localhost",
    author_email="contact@rainshadow.cloud",
    description="cloudwright_slack_webhook",
    packages=setuptools.find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
)
