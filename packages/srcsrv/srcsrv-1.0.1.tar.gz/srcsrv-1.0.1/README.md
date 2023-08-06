# Source Indexing
Python script to add source indexing to **.PDB** files. The source will be automatically pulled from Git
The python script can be invoked on each **.PDB** file after the link phase of the build is completed. Alternatively, the script can receive a list of one or more directories where the **.PDBs** are placed at the end of the build. Internally, the script simply scans each directory recursively and invoke itself on each file with **.pdb** extension. The script takes the following arguments:

>**-p**, **--pdb** - Path to .PDB file to process *(e.g.: -p c:\path\file.pdb)*. (see also: **--pdbs** option).  
>**-P**, **--pdbs** - One or more directories containing **.PDB** files *(e.g.: --pdbs dir1 dir2 ...)*. The script will recurse to each sub-directory under the specified list. The path is assumed to be fully-qualified or relative to **--build-base**.  
>**-b**, **--build-base** - Root of the build directory. This path correspond with top of the repository branch being built.  
>**-g**, **--github** - URL of the repository. The default value is *github.com*  
>**-r**, **--repo** - Repository path.  
>**-s**, **--srcsrv** - Path to SDK or DDK source indexing directory. Default path is **C:\Program Files (x86)\Windows Kits\10\Debuggers\x64\srcsrv**  
>**-o**, **--output** - Path of the source indexing file used for the *srcsrv* stream in the **.PDB**. If this parameter is not used if **--pdbs** option is present. The script will use a file with the same name as the binary with .ini extension *(i.e.: prog.exe will produce prog.pdb which is embedded with prog.ini)*. For build troubleshooting you can use the **--pdb** option without specifying **--output** file. The content of this file is sent to *stdout* and the **.PDB** will not be modified (see: **--no-process**)

Build diagnostic options

>**-k**, **--keep** - Be default the file specified by the **--output** parameter (or .ini file) is deleted after processing. With this option specified the file is kept in the same directory as the **.PDB**  
>**-n**, **--no-process** - The script is run without modifying the **.PDB**. Should be used with with **--keep** option or with logging enabled.  
>**-l**, **--log** - Path to log file. By default all logging is visible in *stdout*.

The script can also be invoked with a response file. Using **@path\resp_file_name**. The file can contain any of the above parameters. Response file and command line parameters can be combined. Example:

```
-P debug release amd64dbg amd64rel  
--repo myrepo/myproj
```