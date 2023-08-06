"""CLI hook module to PySubmit."""

import argparse

import pysubmit.template as t


def main():

    parser = argparse.ArgumentParser(description="PySubmit computation submission tool.")

    parser.add_argument('-pf', '--pysubmit-file', required=True,
                        help='The pysubmit file to use.')
    parser.add_argument('-o', '--outdir', required=True,
                        help='The output directory to save the output to.')
    parser.add_argument('-ds', '--dont-summarise', action='store_true',
                        help='Do not summarise the generated start scripts if set.')
    parser.add_argument('-b', '--boilerplate-file', default=None,
                        help='Boilerplate file as required by the file format from PySubmit v0.1. '
                             'Use this to achieve backward compatibility for PySubmit templates from older PySubmit versions.')
    parser.add_argument('-sc', '--start-command', default='qsub',
                         help='Command to submit a start script to the scheduler.')

    args = parser.parse_args()

    pysubmit_file = args.pysubmit_file
    outdir = args.outdir
    dont_summarise = args.dont_summarise
    boilerplate_file = args.boilerplate_file
    start_command = args.start_command

    template = t.Template(pysubmit_file, boilerplate_file)

    # Create files
    files = template.create_files(outdir, start_command=start_command if not dont_summarise else None)
    print()
    print("Done.")
    print()
    print("Created files:")
    for filename in files:
        print(f"\t{filename}")
    print()
    
