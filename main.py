import argparse
import mogavity

argument_parser = argparse.ArgumentParser()
argument_parser.add_argument("-f", "--file", help="Filename")
argument_parser.add_argument("--quadruples", help="Show Quadruples")
argument_parser.add_argument("--tables", help="Show Variable and Function Tables")
argument_parser.set_defaults(quadruples=True)
argument_parser.set_defaults(tables=True)
args = argument_parser.parse_args()

file_name = args.file

mogavity.compile_and_run(file_name, args.quadruples, args.tables)
