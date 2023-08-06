from setuptools import setup

setup(
    name="inner-class",
    version="0.1",
    description="Advanced inner classes for Python",
    author="S.Keim",
    author_email="s.keim@free.fr",
    license="MIT",
    py_modules=["inner"],
    zip_safe=True,
    test_suite="test",
    url="https://github.com/sebkeim/inner-class",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
