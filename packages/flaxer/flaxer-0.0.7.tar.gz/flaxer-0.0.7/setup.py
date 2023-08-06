import setuptools

print(setuptools.find_packages())
setuptools.setup(
    name="flaxer",
    version="0.0.7",
    author="yana",
    author_email="yana021022@example.com",
    description="A python fixer",
    url="https://github.com/yangyangxcf/flaxer",
    packages=setuptools.find_packages(),
    install_requires=["click", "yapf"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={"console_scripts": ["flaxer=flaxer.flaxer:main"],},
    python_requires=">=3.6",
)
