#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
In this module you find a method (read_cif_folder) to read in all .cif files
from a folder and store the structures in the database.
"""

# TODO maybe also save the cif files in the AiiDA repository
# and set the source to there. Might make a difference for
# structure visualization, because cif file has more information
# also keep connection to ICSD id number

__copyright__ = (u"Copyright (c), 2016, Forschungszentrum Jülich GmbH, "
                 "IAS-1/PGI-1, Germany. All rights reserved.")
__license__ = "MIT license, see LICENSE.txt file"
__version__ = "0.27"
__contributors__ = "Jens Broeder"

import os

from aiida import load_dbenv, is_dbenv_loaded
if not is_dbenv_loaded():
    load_dbenv()
from aiida.orm import DataFactory
from ase.io import cif

structuredata = DataFactory('structure')

def read_cif_folder(path=os.getcwd(), rekursive=True,
                    store=False, log=False,
                    comments='', extras=''):
    """
    Method to read in cif files from a folder and its subfolders.
    It can convert them into AiiDA structures and store them.

    defaults input parameter values are:
    path=".", rekursive=True, store=False, log=False, comments='', extras=''

    :params: path: Path to the dictionary with the files (default, where this method is called)
    :params: rekursive: bool, If True: looks aso in subfolders, if False: just given dir
    :params: store: bool, if True: stores structures in database
    :params: log: bool, if True, writes a logfile with information (pks, and co)
    :params: comments: string: comment to add to the structures
    :params: extras: dir/string/arb: extras added to the structures stored in the db

    """
    ############ parameters for the user to set ########

    parent_cif_folder = path    # folder path
    store_db = store            # True # store stuff in database?
    write_log = log             # write a logfiles on what was saved
    comment = comments          # comments and extras to add to the structure nodes.
    extra = extras              # helpfull for findng them again in the db
    rek = rekursive             # search also in subfolders or only given folder

    #####################
    filenames = []
    filepaths = []
    logfile_name = 'read_cif_folder_logfile'
    infofilestring = ('Structure Formula, Structuredata pk, Structure Data uuid,'
                      ' cif-file-path, comment, extras \n')

    #1. get all the files
    if rek:
        for root, dirs, files in os.walk(parent_cif_folder):
            for file1 in files:
                if file1.endswith(".cif"):
                    filenames.append(file)
                    filepath = os.path.join(root, file1)
                    filepaths.append(filepath)
    else:
        dir_list = os.listdir(parent_cif_folder)
        for filename in dir_list:
            if filename.endswith(".cif"):
                filenames.append(filename)
                filepath = os.path.join(parent_cif_folder, filename)
                filepaths.append(filepath)

    nfiles = len(filenames)
    print '{} cif-files found in folder "{}" '.format(nfiles, parent_cif_folder)

    structuredatas = []

    #2. read all the files and store stuff.
    saved_count = 0
    for i in range(nfiles):
        structuredatas.append(DataFactory('structure'))
        asecell = list(cif.read_cif(filepaths[i], index=slice(None)))[-1]
        struc = structuredatas[i](ase=asecell)
        formula = struc.get_formula()
        if store_db:
            struc.store()
            saved_count = saved_count + 1

            # add comment or extras, only possible after storing
            if comment:
                user = struc.get_user() # we are the creator
                struc.add_comment(comment, user)
            if extra:
                if isinstance(extra, type(dict())):
                    struc.set_extras(extra)
                else:
                    struc.set_extra('specification', extra)
            struc.set_extra('formula', formula)
        if write_log:
            # This file is a logfile/info file created by 'read_cif_folder'
            # Structure Formula, structuredata pk, Structure Data uuid,
            #'cif-file-path', comment, extras
            # TODO? if not stored write not stored
            if store_db:
                infofilestring = infofilestring + '{} {} {} {} {} {} \n'.format(
                    formula, struc.dbnode.pk, struc.uuid,
                    filepaths[i], struc.get_comments(), struc.get_extras())
            else:
                infofilestring = (infofilestring + '{} notstored notstored {}'
                                  'notstored notstored \n'
                                  ''.format(formula, filepaths[i]))

    # write a logfile
    if write_log:
        file1 = os.open(logfile_name, os.O_RDWR|os.O_CREAT)
        os.write(file1, infofilestring)
        os.close(file1)
    print '{} cif-files were saved in the database'.format(saved_count)

if __name__ == "__main__":
    import argparse
    import json
    #  maybe change names?
    parser = argparse.ArgumentParser(description="Read '.cif' files from the current"
                                     " folder and store in AiiDA database. If no"
                                     " arguements are given, read_cif_folder is"
                                     " using default arguments")

    parser.add_argument('-p', metavar='path', type=str, required=False,
                        action='store',
                        help='specify path as string, if not current folder')

    parser.add_argument('-r', required=False,
                        action='store_true',
                        help='if given, search also in subfolders for .cif files. (os.walk subfolders')

    parser.add_argument('-s', required=False,
                        action='store_true',
                        help='if given, store all structures in database.')

    parser.add_argument('-l', required=False,
                        action='store_true',
                        help='if given, write a logfile')

    parser.add_argument('-c', metavar='comments', type=str, required=False, default='',
                        action='store',
                        help='string, add a comment to the node(s) if stored. '
                             'exp: -c crystal data for my project')

    parser.add_argument('-e', metavar='extras', required=False, type=json.loads,
                        action='store',
                        help='string, or dictionary to add to the node(s) extras'
                             ' if stored. exp: -e {"project" : "myproject", "type" : "simple metal"}')

    args = parser.parse_args()
    if args.p:
        read_cif_folder(path=args.p, rekursive=args.r, store=args.s, log=args.l,
                        comments=args.c, extras=args.e)
    else:
        read_cif_folder(rekursive=args.r, store=args.s, log=args.l,
                        comments=args.c, extras=args.e)