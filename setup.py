from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name='torrent-maker',
    version='1.3.0',
    author='Torrent Maker Team',
    author_email='torrent-maker@example.com',
    description='基于 mktorrent 的半自动化影视剧种子制作工具',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/torrent-maker",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Communications :: File Sharing",
        "Topic :: Multimedia :: Video",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'torrent-maker=main:main',
        ],
    },
    keywords="torrent bittorrent mktorrent tv-series video automation",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/torrent-maker/issues",
        "Source": "https://github.com/yourusername/torrent-maker/",
        "Documentation": "https://github.com/yourusername/torrent-maker#readme",
    },
)