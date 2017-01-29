# Copyright 2016-2017 F. Alexander Wolf (http://falexwolf.de). 
"""
Scanpy - Single-Cell Analysis in Python

This is the general purpose command-line utility. 
"""
# Notes
# -----
# Regarding command-line parsing, 'Click' does not seem to be necessary at the
# moment (http://click.pocoo.org/5/).

# this is necessary to import scanpy from within package
from __future__ import absolute_import
import argparse
from collections import OrderedDict as odict
from sys import argv, exit
import scanpy as sc

# description of simple inquiries
dsimple = odict([
    ('exdata', 'show example data'),
    ('examples', 'show example use cases'),
])

# description of standard tools
dtools = odict([
    ('pca', 'visualize using PCA'),
    ('diffmap', 'visualize using Diffusion Map'''),
    ('tsne', 'visualize using tSNE'),
    ('dpt', 'perform Diffusion Pseudotime analysis'),
    ('difftest', 'test for differential expression'),
    ('sim', 'simulate stochastic gene expression models'),
])

# assemble main description
def main_descr():
    descr = '\nsimple inquiries\n----------------'
    for key, help in dsimple.items():
        descr += '\n{:12}'.format(key) + help
    descr += '\n\ntools\n-----'
    for key, help in dtools.items():
        descr += '\n{:12}'.format(key) + help
    descr += '\n\nexkey tool\n----------'
    descr += ('\n{:12}'.format('exkey tool')
                   + 'shortcut for providing exkey for --exkey argument to tool')
    return descr

def init_main_parser():
    """
    Init subparser for each tool.
    """

    # the actual parser and parser container
    main_parser = argparse.ArgumentParser(
                      description=__doc__,
                      formatter_class=argparse.RawDescriptionHelpFormatter,
                      add_help=False)
    sub_parsers = main_parser.add_subparsers(metavar='',
                                             description=main_descr())

    for key, help in dtools.items():
        sub_p = sub_parsers.add_parser(
                    key,
                    description=sc.help(key,string=True),
                    formatter_class=argparse.RawDescriptionHelpFormatter,
                    add_help=False)
        try:
            sub_p = sc.get_tool(key).add_args(sub_p)
        except:
            sub_p = sc.utils.add_args(sub_p)
        sub_p.set_defaults(toolkey=key)
    
    return main_parser

def main():

    # check whether at least one subcommand has been supplied
    if len(argv) == 1 or argv[1] == 'h' or argv[1] == '--help':
        init_main_parser().print_help()
        exit(0)

    # simple inquiries
    if argv[1] in dsimple:
        # same keys as in dsimple
        func = {
            'exdata': sc.exdata,
            'examples': sc.examples
        }
        func[argv[1]]()
        exit(0)

    # init the parsers for each tool
    main_parser = init_main_parser()

    # test whether exkey is provided first
    if argv[1] not in dtools:
        if len(argv) > 2 and argv[2] in dtools:
            exkey = argv[1]
            argv[1] = argv[2]
            argv[2] = exkey
        else:
            print('normal usage:    ' + argv[0] + ' tool exkey')
            print('efficient usage: ' + argv[0] + ' exkey tool')
            print('help:            ' + argv[0] + ' -h')
            exit(0)

    args = vars(main_parser.parse_args(argv[1:]))
    args = sc.sett.process_args(args)
    # run Scanpy
    sc.run_args(args['toolkey'], args)

if __name__ == '__main__':
    main()

