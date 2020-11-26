# Contributing to the Project

Please review the following guidelines in order to make the contribution process effective and easy for everyone. 


## Governance

SynBioPython will be governed using a three-tiered system of contributors:
1. Five Editors, who have to be member of the GBA, will oversee the direction of the development of SynBiopython. The Editors will be elected by the current Editors and members of the Core Team (see point 2) and they will have to self-nominate. Editors serve 2 year-long terms.
2. The Core Team members, who are approved by the Editors. Interested contributors who like to be in the Core Team will submit an Expression of Interest to the Editors. The Core Team stays in regular contact (email group/calls) to discuss and actively contribute to the development of SynBioPython.
3. Ad-hoc contributors who contribute through posting issues in Github or submitting ideas/changes via email/any other communication route. There is no regular contact between ad-hoc contributors and Editors/Core Team.

SynBioPython is released on GitHub under the MIT licence. The project is committed to remain free and open source under a licence approved by the [FSF](https://www.fsf.org) and the [OSI](https://opensource.org).

## Feature requests

Feature requests are welcome. Please do so before submitting:
* Check if the feature has already been requested.
* Ensure your idea fits with the scope and aims of the project.
* Please provide details (i.e. explaining the use case (merits of the feature))


## Issue tracker

The issue tracker is the preferred channel for bug reports, and feature requests, but please respect the following restrictions:
* Never use the issue tracker for personal support requests (use [Stack Overflow](https://stackoverflow.com) or [Bioinformatics SE](https://bioinformatics.stackexchange.com)).
* Keep the discussion on topic and respect the opinions of others.


## Contributions

We welcome commits from contributors. We will consider code that is relevant to synthetic biology and meets the following criteria:
* you have the legal right to contribute the code under the project's licence
* the contribution follows the coding style outlined below
* docstrings are included in the code, if applicable
* tests are written for new code & all tests pass

For bigger contributions, such as modules or addition of dependencies, please contact the core team for a discussion and approval. Contributions should be submitted as GitHub pull requests. New feature or bug fix pull requests are reviewed and merged by a core team member. Large contributions, such as modules, are reviewed by at least two core team members.


## Coding conventions

SynBioPython conforms to Black and Flake8 requirements, which are enforced using pre-commit hooks.

Documentation is generated using [Portray](https://github.com/timothycrosley/portray).

Tests are included for each function, with total code coverage >90%.

[Travis CI](https://travis-ci.org/github/Global-Biofoundries-Alliance/SynBioPython) is used for continuous integration.

The project follows the [semantic versioning](https://semver.org) scheme. Major versions are prepared into [GitHub releases](https://github.com/Global-Biofoundries-Alliance/SynBioPython/releases) and also uploaded to [PyPI](https://pypi.org/project/synbiopython/) (Python Package Index).


## Get started!
0. Set up your development environment, then install pre-commit:
```
pip install pre-commit
```

1. Press the "fork" button in GitHub to create a copy of the repository in your own GitHub account.

2. Now you need to clone locally using a terminal:
```
git clone git@github.com:yourname/SynBioPython.git
```
3. Change into the new local directory and install the package and the git hooks:
```
cd SynBioPython
pip install --user -e .
pre-commit install
```
4. Set up a new remote that points to the original project repository:
```
git remote add upstream git@github.com:Global-Biofoundries-Alliance/SynBioPython.git
```
5. Set up Travis CI to watch your fork.

6. Develop on your fork's master branch or a feature branch, then commit:
```
git push origin master
```
Ensure that your changes pass both Black and Flake8 before committing your staged files. Black is the uncompromising Python Code Formatter. It will reformat your entire file in place according to the Black code style. Flake8 is a powerful tool that checks the code's compliance with PEP8.

7. Create a Pull Request (PR) with the "Compare & pull request" button. Describe your changes then "Create pull request" button at the bottom. and wait for review by the maintainers. Please pull again the latest GBA master into your fork and ensure that the Travis CI build of your fork passes before making a PR.

---

The project includes the configuration files for pre-commits hooks to automate the code formatting and checking process: _[.pre-commit-config.yaml](https://github.com/Global-Biofoundries-Alliance/SynBioPython/blob/master/.pre-commit-config.yaml)_, _[.flake8](https://github.com/Global-Biofoundries-Alliance/SynBioPython/blob/master/.flake8)_, and _[.toml](https://github.com/Global-Biofoundries-Alliance/SynBioPython/blob/master/.toml)_ for configuring Black.

Refer to [this page](https://ljvmiranda921.github.io/notebook/2018/06/21/precommits-using-black-and-flake8/) for a complete guideline on how to use pre-commit hook to include Black and Flake8.
