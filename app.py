"""Main App Entry."""

from services.cli import Cli


def main():
    cli = Cli()
    cli.run()


if __name__ == "__main__":
    main()
