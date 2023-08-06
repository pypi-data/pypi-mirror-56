#!python
# coding: utf-8
""""""
import sys
from argparse import ArgumentParser

from ogt import FORMATS
from ogt.ogt_doc import create_doc_from_json_file, create_doc_from_ags4_file
from ogt import ags4 #validate_ags4_file, update, report_to_string


"""CLI Main Parser"""
parser = ArgumentParser(description="Toolkit for geotechnical")

sub_parsers = parser.add_subparsers(help="commands", dest="command")


#=======================
## Convert Parser
p_convert = sub_parsers.add_parser("convert", help="Convert files")

p_convert.add_argument("-b", "--beside", dest="beside", action="store_true",
                       help="save beside original file and appends `.ext`")

p_convert.add_argument("-e", "--extended", dest="extended", action="store_true",
                       help="Outputs header/group data, eg descriptions, picklists, etcs")

p_convert.add_argument("-f", "--format", dest="format", default="json",
                       help="output format and ext", choices=FORMATS)

p_convert.add_argument("-m", "--minify", dest="minify", action="store_true",
                       help="minify the output by removing whitespace")

p_convert.add_argument("-o", "--overwrite", dest="overwrite", action="store_true",
                       help="overwrite output file if it exists")

p_convert.add_argument("--stats", dest="inc_stats", action="store_true",
                       help="include stats in output (only json/yaml)")
p_convert.add_argument("--source", dest="inc_source", action="store_true",
                       help="include source text and cells")

p_convert.add_argument("-w", "--write_file", dest="write_file", help="output file to write")

p_convert.add_argument("-z", "--zip", dest="zip", action="store_true",
                       help="output as a zip file containing original and converted file")

p_convert.add_argument("source_file", type=str, help="AGS4 file to convert")

#=======================
## Validator parser
p_validate = sub_parsers.add_parser("validate", help="Validate files")
p_validate.add_argument("-p", action="store_false", dest="printable",
                        help="Human print output")
p_validate.add_argument("-r", "--rules", type=int, dest="rules", nargs='+', default=[],
                        help="Rules to check")
p_validate.add_argument("-t", "--tests", action="store_true", dest="run_tests",
                        help="Run Tests")
p_validate.add_argument("source_file", type=str, help="AGS4 file to validate")



## Add some standard items to all commands
for pra in [p_convert, p_validate]:
    pra.add_argument("--debug", dest="debug", action="store_false", help="debug")

if __name__ == "__main__":
    args = parser.parse_args()



    if args.command == "validate" and args.source_file.endswith(".ags"):
        report, error = ags4.validate_ags4_file(args.source_file, args.rules)

        if error is not None:
            print(error)
            sys.exit(0)

        if args.printable:
            print(ags4.report_to_string(report))
        else:
            print(report)

    elif args.command == "convert":
        if args.source_file.endswith(".json"):
            doc, error = create_doc_from_json_file(args.source_file)
        elif args.source_file.endswith(".ags"):
            doc, error = create_doc_from_ags4_file(args.source_file)

        if error is not None:
            print(error)
            sys.exit(0)

        doc.opts.minify = args.minify
        doc.opts.extended = args.extended
        doc.opts.include_stats = args.inc_stats
        doc.opts.include_source = args.inc_source
        message, error = doc.write(ext=args.format, beside=args.beside,
                                   file_path=args.write_file,
                                    to_zip=args.zip, overwrite=args.overwrite)
        if error:
            print(error)
            sys.exit(0)

        print(message)
        sys.exit(0)


    else:
        print("Nothings to do !\n")
        parser.print_help()
        sys.exit(0)
