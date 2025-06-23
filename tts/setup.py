# setup.py
import setuptools

setuptools.setup(
    name="ai-tts",
    version="0.1",
    author="Nanyun",
    description="AI helper tts backend",
    packages=setuptools.find_packages(),
    install_requires=[
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11',
    entry_points={
        'console_scripts': [
            'ai-tts=cli:cli'
        ],
    },
)