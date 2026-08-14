from setuptools import setup, find_packages
from typing import List

# Define the constant to filter out '-e .' from requirements
HYPHEN_E_DOT = "-e ."

def get_requirements(file_path: str) -> List[str]:
    """
    Reads requirements.txt and returns a list of packages.
    Filters out '-e .' if present.
    """
    requirements = []
    try:
        with open(file_path, 'r') as file_obj:
            # Read lines and strip newlines
            requirements = file_obj.readlines()
            # Clean up the list: remove \n and filter out '-e .'
            requirements = [req.replace("\n", "") for req in requirements]
            
            # Remove the '-e .' entry if it exists in the list
            if HYPHEN_E_DOT in requirements:
                requirements.remove(HYPHEN_E_DOT)
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return []
    
    return requirements

setup(
    name="ml_project",
    version="0.0.1",
    author="Adarsh Pandey",
    author_email="adarshpandey111110@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements("requirements.txt")
)