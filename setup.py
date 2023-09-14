from setuptools import setup, find_packages
from typing import List

PROJECT_NAME = "FRAUD_DETECTION_PREDICTION"
VERSION = "0.01"
DESCRIPTION = "END_TO_END_ML_PROJECT"
AUTHOR = "VISWA PRAKASH"
AUTHOR_EMAIL = "prakashviswa1990.gmail.com"

HYPEN_E_DOT = "-e ."
REQUIREMENT_FILE_NAME = "requirements.txt"

def get_requirement_list() -> List[str]:
    with open(REQUIREMENT_FILE_NAME) as requirement_files:
        requirement_list = requirement_files.readlines()
        requirement_list = [requirement_name.replace("\n", "") for requirement_name in requirement_list]
        
        if HYPEN_E_DOT in requirement_list:
            requirement_list.remove(HYPEN_E_DOT)
        return requirement_list

setup(name= PROJECT_NAME,
      version= VERSION,
      description= DESCRIPTION,
      author= AUTHOR,
      author_email= AUTHOR_EMAIL,
      packages=find_packages(),
      install_requires = get_requirement_list()
     )