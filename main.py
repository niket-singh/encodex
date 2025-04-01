import argparse
from utils.banner import print_banner
from utils.formats import formats
from utils.customhelp import CustomHelpAction
from utils.decodejwt import decode_jwt
from lib.EncodingChain import EncodingChain

def handle_encode(args):
    """Encodes the data using the specified format"""
    encoder = formats.get(args.format)()
    if args.format == "base64":
        print(encoder.encode(args.data, url_safe=args.url_safe))
    else:
        print(encoder.encode(args.data))


def handle_decode(args):
    """Handle the 'decode' command and decode the data using the specified format"""
    if args.format == "jwt":
        try:
            header, payload, signature = decode_jwt(args.data)
            print("Header:", header)
            print("Payload:", payload)
            print("Signature:", signature)
        except Exception as e:
            print(f"Error decoding JWT: {e}")
    else:
        decoder = formats.get(args.format)()
        if args.format == "base64":
            print(decoder.decode(args.data, url_safe=args.url_safe))
        else:
            print(decoder.decode(args.data))

def handle_chain_encode(args):
    chain = EncodingChain()
    for format_name in args.formats:
        chain.add(format_name)
    print(chain.encode(args.data))

def handle_chain_decode(args):
    chain = EncodingChain()
    for format_name in reversed(args.formats):
        chain.add(format_name)
    result = chain.decode(args.data)
    print(f"Final result: {result}")


def show_info(args) -> str:
    """Show information about the encoding format"""
    encoder = formats.get(args.format)()
    print(encoder.info())


def get_formats() -> list[str]:
    """Prints the list of available encoding formats"""
    print("Available encoding formats:")
    for format in formats:
        print(format)


def main():
    parser = argparse.ArgumentParser(
        description="EncodeX CLI - Encoding and Decoding Utility", add_help=False
    )
    parser.add_argument(
        "-h", "--help", action=CustomHelpAction, help="Show this help message and exit"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    encode_parser = subparsers.add_parser("encode", help="Encode data")
    encode_parser.add_argument(
        "format",
        choices=["base64", "ascii", "url", "hex", "html"],
        help="Encoding format",
    )
    encode_parser.add_argument("data", help="Data to encode")
    encode_parser.add_argument(
        "--url-safe", action="store_true", help="Use URL-safe Base64 encoding"
    )

    decode_parser = subparsers.add_parser("decode", help="Decode data")
    decode_parser.add_argument(
        "format",
        choices=["base64", "ascii", "url", "hex", "html", "jwt"],
        help="Decoding format",
    )
    decode_parser.add_argument("data", help="Data to decode")
    decode_parser.add_argument(
        "--url-safe", action="store_true", help="Use URL-safe Base64 decoding"
    )

    chain_encode_parser = subparsers.add_parser("chain-encode", help="Encode data using multiple formats")
    chain_encode_parser.add_argument("formats", nargs="+", choices=list(formats.keys()), help="Encoding formats in order")
    chain_encode_parser.add_argument("data", help="Data to encode")

    chain_decode_parser = subparsers.add_parser("chain-decode", help="Decode data using multiple formats")
    chain_decode_parser.add_argument("formats", nargs="+", choices=list(formats.keys()), help="Decoding formats in reverse order")
    chain_decode_parser.add_argument("data", help="Data to decode")

    info_parser = subparsers.add_parser("info", help="Get info about encoding format")
    info_parser.add_argument(
        "format",
        choices=["base64", "ascii", "url", "hex", "html"],
        help="Encoding format",
    )

    list_parser = subparsers.add_parser("list", help="List available encoding formats")
    list_parser.add_argument("--format", help="Filter by format")

    args = parser.parse_args()

    # If no command is provided, print the help message and return
    if not args.command:
        print_banner()
        parser.print_help()
        return

    if args.command in ["encode", "-e"]:
        handle_encode(args)
    elif args.command == "decode":
        handle_decode(args)
    elif args.command == "chain-encode":
        handle_chain_encode(args)
    elif args.command == "chain-decode":
        handle_chain_decode(args)
    elif args.command == "info":
        show_info(args)
    elif args.command == "list":
        get_formats()


if __name__ == "__main__":
    main()
