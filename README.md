# Project-Dependency-Finder
This project lists all the dependencies of a GitHub repository using GitHub API v4 and gives you the output as csv file.

You need a personal GitHub token to be able to use GitHub API. Therefore, edit the "cred.json" file and replace the token key with yours.

# **How to run** 
After entering your GitHub token in cred.json, enter command "python main.py --depth 1 repo_owner/repo_name" for example:
 
 
python main.py --depth 1 facebook/react

**depth** defines the dependency depth you want to search. Set --depth 0 if you want to search maximum dependenciy depth, until no dependencies are left.

The output in csv is printed according to repository relation(From). From being the origin repository.
