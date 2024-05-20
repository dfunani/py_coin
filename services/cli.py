from argparse import ArgumentParser, RawDescriptionHelpFormatter
import textwrap

from lib.interfaces.cli import CLIError
from services.blockchain import BlockChainService


class Cli:
    ACTIVE = True
    __FORMATTER__ = RawDescriptionHelpFormatter
    __EPILOG__ = "🪙   New Age BlockChain Services. 🪙"
    __PROLOG__ = """
🚀  Welcome to the Block Type CLI! 🌟

🔹  Explore the Power of PYCoin  🔹

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                                                      ┃
┃  Simplifying smart transacting and contracting.      ┃
┃  Unlock the potential of effortless block chaining!  ┃
┃                                                      ┃
┃  📈  Seamless integration with your workflows        ┃
┃  💡  Intelligent options tailored just for you       ┃
┃  🌐  Global reach, local convenience                 ┃
┃                                                      ┃
┃  Go ahead, let's shape the future of transactions    ┃
┃  and contracts together!                             ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

"""
    __INSTANCE__ = None
    __GENERAL_ARGS__ = {
        "create": {"args": ("create",), "kwargs": {"help": "Creates Resource."}},
        "read": {"args": ("read",), "kwargs": {"help": "Gets Resource."}},
        "update": {"args": ("update",), "kwargs": {"help": "Updates Resource."}},
        "delete": {"args": ("delete",), "kwargs": {"help": "Deletes Resource."}},
        "exit": {"args": ("exit",), "kwargs": {"help": "exit CLI."}},
    }
    __TRANSACTION_ARGS__ = {
        "transaction": {
            "args": ("--transaction", "-T"),
            "kwargs": {
                "action": "store_true",
                "help": "Create a Transaction",
            },
        },
        "sender": {
            "args": ("--sender", "-s"),
            "kwargs": {
                "help": "Sender/Contractor's ID",
            },
        },
        "receiver": {
            "args": ("--receiver", "-r"),
            "kwargs": {
                "help": "Receiver/Contractee's ID",
            },
        },
        "amount": {
            "args": ("--amount", "-a"),
            "kwargs": {
                "type": float,
                "help": "Transaction Amount",
            },
        },
    }
    __CONTRACT_ARGS__ = {
        "contract": {
            "args": ("--contract", "-C"),
            "kwargs": {
                "action": "store_true",
                "help": "Create a Contract",
            },
        },
        "contractor": {
            "args": ("--contractor", "-cr"),
            "kwargs": {
                "help": "Sender/Contractor's ID",
            },
        },
        "contractee": {
            "args": ("--contractee", "-ce"),
            "kwargs": {
                "help": "Receiver/Contractee's ID",
            },
        },
        "contract_data": {
            "args": ("--contract-data", "-cd"),
            "kwargs": {
                "help": "Update the Contract Location",
            },
        },
    }

    def __new__(cls) -> "Cli":
        """Singleton Class Constructor."""
        if cls.__INSTANCE__:
            return cls.__INSTANCE__

        cls.parser = ArgumentParser(
            formatter_class=cls.__FORMATTER__,
            epilog=textwrap.dedent(cls.__EPILOG__),
            description=textwrap.dedent(cls.__PROLOG__),
        )
        cls.__set_cli_help__()
        cls.__set_cli_args__()
        cls.__INSTANCE__ = super().__new__(cls)
        print(
            f"{Cli.__PROLOG__}\n{Cli.__EPILOG__}\nCLI App started. Type 'exit' to quit."
        )
        return cls.__INSTANCE__

    @classmethod
    def __set_cli_help__(cls):
        cls.subparsers = cls.parser.add_subparsers(
            dest="command", required=True, help="Sub-command help"
        )

    @classmethod
    def __set_cli_args__(cls):
        # Add subparsers for general commands
        for command, command_args in cls.__GENERAL_ARGS__.items():
            subparser = cls.subparsers.add_parser(
                command, help=command_args["kwargs"]["help"]
            )
            cls.__add_transaction_args__(subparser)
            cls.__add_contract_args__(subparser)

    @classmethod
    def __add_transaction_args__(cls, subparser):
        for key, arg in cls.__TRANSACTION_ARGS__.items():
            subparser.add_argument(*arg["args"], **arg["kwargs"])

    @classmethod
    def __add_contract_args__(cls, subparser):
        for key, arg in cls.__CONTRACT_ARGS__.items():
            subparser.add_argument(*arg["args"], **arg["kwargs"])

    @classmethod
    def args_parser(cls, args):
        match (args.command):
            case "create":
                if args.transaction:
                    return BlockChainService().create_transaction()
                if args.contract:
                    return BlockChainService().create_contract()
            case "update":
                if args.transaction:
                    return BlockChainService().update_transaction()
                if args.contract:
                    return BlockChainService().update_contract()

    @classmethod
    def run(cls):
        while True:
            try:
                # Capture input from standard input
                if cls.ACTIVE:
                    command = input("iPYCoin: ")

                    if command == "kill":
                        cls.kill()
                        continue

                    # Parse the input command and handle it
                    args = cls.parser.parse_args(command.split())
                    cls.args_parser(args)
            except (KeyboardInterrupt, EOFError, CLIError):
                raise CLIError("CLI Server Was Terminated.")
            except SystemExit as exc:
                continue

    @classmethod
    def kill(cls):
        print("PYCoin CLI Terminated.")
        cls.ACTIVE = False
