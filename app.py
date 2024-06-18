"""App: Ingress Point."""

from services.cli import Cli


def main():
    """CLI Interface."""

    cli = Cli()
    cli.run()


if __name__ == "__main__":
    main()
