'''Program Database (PDB) parsing and modifying class
'''
# Python modules
import os
import sys
import subprocess
# Source index modules
from . import base

PROLOGUE = '''SRCSRV: ini ------------------------------------------------
VERSION=2
VERCTRL=
SRCSRV: variables ------------------------------------------
GITHUB_BASE={github}
GITHUB_REPO={repo}
GITHUB_REPO_SHA={hexsha}
BUILD_BASE={build_base}
SRCSRVTRG=%curl_extract_target%
SRCSRVCMD=%curl_cmd%
CURL_EXTRACT_TARGET=%userprofile%\%fnbksl%(%github_repo%)\%curl_repo_sha%\%fnbksl%(%var2%)
CURL_REPO_SHA=%github_repo_sha%
CURL_CMD=curl.exe -H "Accept: application/vnd.github.v3.raw" -L https://%curl_token%@%github_base%/raw/%github_repo%/%github_repo_sha%/%var2% --create-dirs -o %SRCSRVTRG%
CURL_TOKEN=%github_token%
SRCSRV: source files ---------------------------------------
'''
# ... more files ...
# d:\build_path\somedir\somefile.h*somedir/somefile.h
# ... more files ...
EPILOGUE = '''SRCSRV: end ------------------------------------------------'''


class PDB(base.Base):
    '''.PDB processing
    '''
    def __init__(self, args):
        super(PDB, self).__init__(args)
        self.path_match = (self.build_base + '*.cpp').replace('\\', '\\\\')

    @property
    def sources(self):
        '''Property containing a list of source files in the current source tree
        :return List of source files
        '''
        if self._sources:
            return self._sources

        srctool = os.path.join(self.args.srcsrv, 'srctool.exe')
        self.args.pdb = os.path.join(self.args.build_base, self.args.pdb)
        try:
            cp = subprocess.run([srctool, '-r', '-z', f'-l:{self.path_match}', self.args.pdb], stdout=subprocess.PIPE, check=True)
        except subprocess.CalledProcessError:
            self.logger.error(f'{srctool} returned an error processing {self.args.pdb}')
            self._sources = []
            return self._sources

        files = cp.stdout.splitlines()
        self._sources = [file.decode() for file in files if file.endswith(b'.cpp')]
        if len(self._sources):
            self.logger.info(f'{self.args.pdb} contains: {self._sources}')
        else:
            self.logger.warning(f'{self.args.pdb} no source files found')
        return self._sources

    def process(self, si):
        ''' Process a single .PDB
        '''
        self.args.__dict__.update({'hexsha': si.hexsha})
        self.args.output.write(PROLOGUE.format(**self.args.__dict__))
        for src in self.sources:
            try:
                code = si.sources[src]
            except KeyError:
                si.logger.warning(f'Could not found {src} in {self.args.pdb}')
            self.args.output.write(f'{src}*{code[0]}/{code[1].name}\n')
        self.args.output.write(EPILOGUE)

        if self.args.output != sys.stdout:
            # Write the the output file onto the .PDB
            self.args.output.close()
            if not self.args.no_process:
                pdbstr = os.path.join(self.args.srcsrv, 'pdbstr.exe')
                try:
                    cp = subprocess.run([pdbstr, '-w', f'-p:{self.args.pdb}', f'-s:srcsrv', f'-i:{self.args.output.name}'], check=True)
                except subprocess.CalledProcessError:
                    self.logger.error(f'{pdbstr} returned an error processing {self.args.pdb}')

            if not self.args.keep:
                # Remove the output file
                os.remove(self.args.output.name)


__all__ = ['PDB']

if __name__ == '__main__':
    import sys
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--pdb',        help='Path to .PDB file')
    parser.add_argument('-b', '--build-base', help='Build directory path')
    parser.add_argument('-s', '--srcsrv',     help='SRCSRV tools directory',  default=r'C:\Program Files (x86)\Windows Kits\10\Debuggers\x64\srcsrv')
    pdb = PDB(parser.parse_args())
    print(pdb.sources)
