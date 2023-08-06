![ ](../logo.jpg)

# Capco Command Line Interface (Capco-Cli)

Capco-cli is a tool used to generates the file structures with relevant code snippets based on the selected templates.

# Installing capoc-cli

1) Install python using homebrew or by visiting (https://www.python.org/downloads/)
    * pip install capco-cli

2) To view the list of all the available templates in the bitbucket repository(this may required you to login using your bitbucket profile), run the following:
	* capco templates list

3) To view all the list of configurable options
	* capco templates inspect <TEMPLATE-NAME>

4) To build the capco-template application, run the following:
    * capco projects create --template <TEMPLATE-NAME> --target_dir PATH.

5) To add configurable options i.e.
    * capco projects create --template <TEMPLATE-NAME> --option database=NAME –target_dir PATH
    You can view list of all the configurable options by running
    * capco templates inspect <TEMPLATE-NAME>

   For more help run:
    * capco --help

# Folder structure for the templates
common: This folder only consists of the files which are similar across all the templates.
Folder Structure
  - common
    - files – Files that are common across all the different templates i.e. .gitignore, docker-compose.yml
    - files.yml – Source and destination path for the common files.
    - info.yml – Any configurable options are added here.

  - template-name
    - files – Required files and folders for the template
    - file.yml – Source and target destination for the files.
    - info.yml – All the configurable options for the templates i.e. database, message broker.

   More detail about files.yml and info.yml can be found in https://bitbucket.org/ilabs-capco/capco-cli/src/master/docs/
