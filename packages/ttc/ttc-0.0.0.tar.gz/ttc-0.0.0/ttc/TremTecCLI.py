"""TremTec CLI class."""
import os
import sys
import shutil
import subprocess

import click
from PyInquirer import prompt


workspacePath = os.getenv('PROJECT_HOME') or os.getenv('WORKSPACES')


def getPath(name):
    """Get os Path."""
    return os.path.join(workspacePath, name) or workspacePath


def runShell(name, initGit=False):
    """Run a shell in workspace."""
    # Start a new shell
    startup_cmds = ''
    if initGit:
        startup_cmds = 'git init'
    commands = f"zsh -c '{startup_cmds}; zsh -i;'" if startup_cmds else 'zsh'

    os.chdir(getPath(name))
    process = subprocess.Popen(
        commands,
        stdin=sys.stdin,
        stdout=sys.stdout,
        shell=True,
    )
    # TODO: handle errors when process closes
    print(process.communicate())


class TremTecCLI:
    """TremTec CLI definition."""

    def __init__(self):
        """Constructor."""
        self.workspace.add_command(self.create)
        self.workspace.add_command(self.remove)
        self.workspace.add_command(self.workon)

        self.main.add_command(self.workspace)

    @staticmethod
    @click.group()
    def main():
        """
                         \n
        (_  _)(_  _)/ __)\n
          ||    || (___\n
                         \n
           Trem Tec CLI  \n
                         \n
                         \n
        """
        pass

    @staticmethod
    @click.group('ws')
    def workspace():
        """Workspace command."""
        pass

    @staticmethod
    @click.command('mk')
    def create():
        """Create workspace."""
        questions = [
            {
                'type': 'input',
                'name': 'name',
                'message': 'What\'s your workspace name',
            }
        ]
        answers = prompt(questions)

        # Start a new shell
        os.mkdir(getPath(answers['name']))
        runShell(answers['name'], initGit=True)

    @staticmethod
    @click.command()
    def workon():
        """Select a workspace to work on."""
        list_ws = os.listdir(workspacePath)
        questions = [
            {
                'type': 'list',
                'name': 'name',
                'message': 'What\'s workspace do wanna work',
                'choices': list_ws,
            }
        ]
        answers = prompt(questions)

        # Start a new shell
        runShell(answers['name'])

    @staticmethod
    @click.command('rm')
    def remove():
        """Remove workspace."""
        list_ws = os.listdir(workspacePath)
        questions = [
            {
                'type': 'list',
                'name': 'name',
                'message': 'What\'s workspace do you want to remove',
                'choices': list_ws,
            },
            {
                'type': 'confirm',
                'name': 'continue',
                'message': 'This you remove your project, are you sure?',
                'default': True,
            },
        ]
        answers = prompt(questions)

        removePath = os.path.join(workspacePath, answers['name'])

        if answers['continue']:
            shutil.rmtree(removePath, ignore_errors=True)
