'''Indexer class
'''
# Python modules
import os
import git
import argparse
import pyteamcity
# Source index modules
from . import pdb
from . import base


class Indexer(base.Base):
    '''Source indexer class
    '''
    def __init__(self, args):
        super(Indexer, self).__init__(args)
        self._sources = None
        self.repo = git.Repo(self.args.build_base)
        self.hexsha = self.repo.active_branch.object.hexsha
        self.tree = self.repo.tree()

    @property
    def tags(self):
        ''' Return list of all repo tags
        '''
        return self.repo.tags

    @property
    def sources(self):
        '''Create a list of all source files in the repository
        '''
        if not self._sources:
            self._sources = {}
            self._sources_tree(self.tree.trees)
        return self._sources

    def _sources_tree(self, trees):
        '''Private method to recursively process source tree
        '''
        for tree in trees:
            for blob in tree.blobs:
                self._sources.update({blob.abspath.lower(): (tree.name, blob)})
            # traverse tree
            if len(tree.trees):
                self._sources_tree(tree.trees)

    def _index(self):
        ''' Initial indexing during build
        '''
        for bld_dir in self.args.pdbs:
            bld_dir = os.path.join(self.args.build_base, bld_dir)
            if not os.path.isdir(bld_dir):
                self.logger.error('Directory: {bld_dir} not found')
                continue    # Non-fatal error, skip invalid directory

            for dir, subdirs, files in os.walk(bld_dir):
                for fname in files:
                    if fname.endswith('.pdb'):
                        self.args.pdb = os.path.join(dir, fname)
                        self.args.output = argparse.FileType('w')(self.args.pdb[:-4] + '.ini')
                        pdb.PDB(self.args).process(self)

    def _reindex(self):
        ''' @TODO: Process .PDB files after build. This assumes that there's a
                   way to tie back the symbols to the original repo commit hash.
        '''
        pass

    def process(self):
        ''' Process each of the .PDBs
        '''
        if not self.args.pdbs:
            return pdb.PDB(self.args).process(self)

        if self.args.action == 1:
            self._index()
        else:
            self._reindex()


__all__ = ['Indexer']
