"""Main function."""
from ttc.TremTecCLI import TremTecCLI

import click_completion


def main():
    """Create Main function."""
    click_completion.init()
    cli = TremTecCLI()
    cli.main()


if __name__ == '__main__':
    main()
