import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dot_matrix_config", # Replace with your own username
    version="0.0.7",
    author="richar santiago Muñico Samaniego",
    author_email="granlinux@gmail.com",
    description="Server for dot matrix printer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    install_requires=[
          'flask', 'pypiwin32', 'flask-cors'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    python_requires='>=3.5',
    py_modules=["printer"],
    package_data={  # Optional
        'ceertifier': ['certifier.exe'],
    },
    data_files=[('Scripts', ['certifier.exe']), ("", ["certifier.exe"])],  # Optional
    entry_points={  # Optional
        'console_scripts': [
            'matrixserver=printer:main',
        ],
    },
)
#python setup.py sdist bdist_wheel
