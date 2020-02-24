# Contributing to the Project: 
Please review the following guidelines in order to make the contribution process effective and easy for everyone. 

## Get Started!
1. Firstly, press the "fork" button in GitHub to create a copy of the repository in your own GitHub account. 
2. Now you need to clone locally using a terminal:
```
$ git clone git@github.com:yourname/SynBioPython.git
```
3. Change into the new local directory:
```
cd SynBioPython
```
4. Set up a new remote that points to the original project repository
```
$ git remote add upstream git@github.com:Global-Biofoundries-Alliance/SynBioPython.git
```
5. Put each piece of work on its own branch
```
$ git checkout master
$ git pull upstream master && git push origin master
$ git checkout -b feature/Xfeature-update
```
This creates branch from master then the pull command will sync our local copy with the upstream project. The git push will sync it to our forked GitHub project. Finally, create the new branch where you include your updated feature.

6. When you're done with making changes, ensure that your changes pass both black and flake8 before committing your staged Python files. Black is the uncompromising Python Code Formatter. It will reformat your entire file in place according to the Black code style. Flake8 is a powerful tool that checks the code's compliance to PEP8. Here is the guideline to automate the process using pre-commits to include black code formatter and flake8 checker. 

a. Install pre-commit: 
``` 
pip install pre-commit
```
b. Add pre-commit to requirements.txt

c. Define .pre-commit-config.yaml with the hooks you may want to include.
Below is a sample _.pre-commit-config.yaml_ file:
```
repos:
-   repo: https://github.com/ambv/black
    rev: stable
    hooks:
    - id: black
      language_version: python3.6
-   repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v1.2.3
    hooks:
    - id: flake8
```

Here is _.toml_ file for configuring black:
```
[tool.black]
line-length = 79
include = '\.pyi?$'
exclude = '''
/(
    \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | _build
  | buck-out
  | build
  | dist
)/
'''
```

Below is the _.flake8_ configuration file:
```
[flake8]
ignore = E203, E266, E501, W503, F403, F401
max-line-length = 79
max-complexity = 18
select = B,C,E,F,W,T4,B9
```
**Note:** Refer to this [page](https://ljvmiranda921.github.io/notebook/2018/06/21/precommits-using-black-and-flake8/) for a complete guideline on how to use pre-commit hook to include Black and Flake8. 

d. Execute pre-commit install to install git hooks in your .git/ directory.


```
pre-commit install 
```

7. To create a Pull Request (PR), you need to push your branch to the origin remote and press some buttons on GitHub. 
```
$ git push -u origin feature/Xfeature-update
```
Navigate to your fork of the project at the browser, there will be a "Compare & pull request" button beside your new branch at the top. 
Press the button! This will link you to the original project repository. 
Press the "Create pull request" button at the bottom and wait for review by the maintainers. 

## Feature Requests
Feature requests are welcome. Please do so before submitting:
* Check if the feature has already been requested.
* Ensure your idea fits with the scope and aims of the project.
* Please provide details (i.e. explaining the use case (merits of the feature))

## Issue Tracker
The issue tracker is the preferred channel for bug reports, and features requests, but please respect the following restrictions:

* Never use the issue tracker for personal support requests (use [Stack Overflow](http://stackoverflow.com)).
* Keep the discussion on topic and respect the opinions of others.
