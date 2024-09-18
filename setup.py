from setuptools import setup, find_packages

setup(
    name="gym_pipedream", 
    version="1.0", 
    description="OpenAI gym environment for pipedream",
    author="James Elson",
    url="https://github.com/Jelso13/gym-pipedream",
    packages=find_packages(),
    package_data={
        "gym_pipedream": ["images/**/*"],  # Include all files in images/ and its subfolders
    },
)
