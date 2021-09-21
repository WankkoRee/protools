import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
with open("requirements.txt", "r", encoding="utf-8") as fh:
    install_requires = fh.read().split('\n')

setuptools.setup(
    name="protools",
    version="1.0.0",
    author="Wankko Ree",
    author_email="wkr@wkr.moe",
    description="一个实现了批量将 protobuf 数据自动识别为类 json 格式，批量将 proto 定义文件转为 python 类。适用于需要转换大量的 protobuf 数据或 proto 定义文件。",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="GPLv3",
    url="https://github.com/WankkoRee/protools",
    project_urls={
        "Bug Tracker": "https://github.com/WankkoRee/protools/issues",
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Natural Language :: Chinese (Simplified)",
    ],
    include_package_data=True,
    packages=setuptools.find_packages(),
    setup_requires=['wheel'],
    install_requires=install_requires,
    python_requires=">=3.7",
    entry_points={
        'console_scripts': ['protools=protools.cli:main']
    }
)
