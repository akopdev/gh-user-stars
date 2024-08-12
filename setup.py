from setuptools import find_packages, setup

from starsmd import __version__

setup(
    name="stars.md",
    version=__version__,
    packages=find_packages(),
    install_requires=["aiohttp", "pydantic>=2.0.0"],
    extras_require={
        "dev": [
            "setuptools>65.5.0",
            "flake8",
            "pydocstyle",
            "piprot",
            "pytest",
            "pytest-cov",
            "pytest-asyncio",
            "isort",
            "black",
            "safety",
            "aioresponses",
        ],
    },
    entry_points={"console_scripts": ["starsmd=starsmd.__main__:main"]},
)
