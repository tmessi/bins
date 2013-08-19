#!/usr/bin/env python2
'''
Simple script to get the number of world updates.

This only shows with packages in the ``world`` set need to be updated. It
does not list dependancies of the world set, thus an actual update will
likely have more packages.

To run simply::

    ./updates.py
'''

try:
    import portage
except ImportError:
    # If no portage, exit quietly since we probably aren't on Gentoo
    import sys
    sys.exit(-1)

def get_world_entries():
    '''
    Parse the world file for atoms.

    Return the set of atoms.
    '''
    f = open("/"+portage.WORLD_FILE, "r")
    atoms = set()
    for line in f.readlines():
        atom = line[:-1]
        if portage.isvalidatom(line[:-1]):
            atoms.add(atom)
    f.close()
    return atoms


def get_installed_versions(atom):
    '''
    Get the installed version of the atom.

    atom
        The atom to search for

    Return the installed version.
    '''
    return portage.db['/']['vartree'].dbapi.match(atom)


def get_best_version(atom):
    '''
    Get the best available version accounting for keywords and masking.

    atom
         The atom to search for

    Return the best availalbe version.
    '''
    available = portage.db['/']['porttree'].dbapi.match(atom)
    return portage.best(available)


def main():
    updatable = set()
    for atom in get_world_entries():
        if get_best_version(atom) not in get_installed_versions(atom):
            updatable.add(atom)
    print '{0}'.format(len(updatable))


if __name__ == "__main__":
    main()
