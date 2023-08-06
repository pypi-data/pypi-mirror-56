import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="BattleBreakers", # Replace with your own username
    version="0.0.1",
    author="xMistt",
    description="Async library for interacting with Battle Breakers/Epic Games API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xMistt/BattleBreakers",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'aiohttp',
        'asyncio',
        'pyglet'
    ]
)
