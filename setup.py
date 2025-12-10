"""Setup configuration for user_display module."""

from setuptools import setup, find_packages

setup(
    name="user_display",
    version="1.0.0",
    description="High-performance, modular user display system",
    author="Bug Bash",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "pytest-timeout>=2.0",
        ]
    },
)
