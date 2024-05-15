from argparse import ArgumentParser, RawDescriptionHelpFormatter
import textwrap


def main():
    """Main Application."""
    return "Completed"


if __name__ == "__main__":
    parser = ArgumentParser(
        formatter_class=RawDescriptionHelpFormatter,
        epilog="Creates a Block Type.",
        description=textwrap.dedent("""
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

"""),
    )

    # Create subparsers for 'create' and 'update' commands
    subparsers = parser.add_argument_group(
        "Operations", description="Block Operations Available.",
    )

    # Subparser for 'create' command
    create_parser = subparsers.add_argument("create", help="Creates Resource.")
    update_parser = subparsers.add_argument("update", help="Update Resource.")

    create_parser_group = parser.add_argument_group("Transaction options")
    create_parser_group.add_argument(
        "--transaction", "-T", action="store_true", help="Create a Transaction"
    )
    create_parser_group.add_argument(
        "--sender", "-s", action="store_true", help="Sender/Contractor's ID"
    )
    create_parser_group.add_argument(
        "--receiver", "-r", action="store_true", help="Receiver/Contractee's ID"
    )
    create_parser_group.add_argument(
        "--amount",
        "-a",
        action="append_const",
        const=int,
        dest="types",
        help="Transaction Amount",
    )

    # Subparser for 'update' command
    update_parser_group = parser.add_argument_group("Contract options")
    update_parser_group.add_argument(
        "--contract", "-C", action="store_true", help="Update a Contract"
    )
    update_parser_group.add_argument(
        "--contractor",
        "-cr",
        action="store_true",
        help="Update the Sender/Contractor's ID",
    )
    update_parser_group.add_argument(
        "--contractee",
        "-ce",
        action="store_true",
        help="Update the Receiver/Contractee's ID",
    )
    update_parser_group.add_argument(
        "--contract-data",
        "-cd",
        action="store_true",
        help="Update the Contract Location",
    )

    args = parser.parse_args()

    # Call the main function based on the command
    if args.command == "create":
        print("Create command selected.")
        # Add logic to handle 'create' command
    elif args.command == "update":
        print("Update command selected.")
        # Add logic to handle 'update' command
    main()
