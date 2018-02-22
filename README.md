# UnRAR wrapper

UnRAR wrapper (`unrar_wrapper.py`) is a wrapper python script that transforms the basic UnRAR commands to unar and lsar calls in order to provide a backwards compatibility.

## Reasons for wrapper
[UnRAR](https://www.rarlab.com) is freeware command-line application for extracting RAR file archives. Unfortunately, this piece of software is non-free and therefore in many distributions, it's beeing replaced by LGPL [the Unarchiver (unar/lsar)](https://theunarchiver.com/command-line).

In general, the Unarchiver seems to be a good alternative to non-free unrar. It supports basically the same formats (except for UUE and JAR and a limited support for ARJ (no multi-part) and ACE (no support for Ace 2.0)) and it also supports RAR5. 

Unfortunately, UnRAR and Unarchiver are not CLI compatible at all, they have a different set of options. Unrar supports quite a big set of options (sometimes rather obscure and unnecessary) while Unarchiver only supports a relatively small subset of it. Unarchiver also distributes this functionality between `unar` (unpacking) and `lsar` (listing and testing) utilities.


## Supported functionality
As it was already written, UnRAR provides a huge set of commands and options, while Unarchiver only a relatively small subset of it. As the main purpose of this wrapper is to preserve the basic backwards compatibility, only the essential commands and options are supported.

### Synopsis
`unrar command [option1] [optionN] archive [files...] [@listfiles...] [path_to_extract/]`

`unar [OPTION]... ARCHIVE [FILE]...`

`lsar [OPTION]... ARCHIVE...`

As you can see even UnRAR and Unarchiver synopsis is different. Wrapper supports UnRAR synopsis as is only for extract (`x`) command. For list (`l`) and test (`t`) commands it supports neither `files`, `@listfiles` nor `path_to_extract/` as Unarchiver doesn't provide this functionality.

| UnRAR | unar | wrapper implementation |
|--|--|--|
| `[files...]` | `[FILE]`  | direct  | 
| `[@listfiles...]` | not supported  | via multiple `[FILE]` | 
| `[path_to_extract/]` | `unar -output-directory`  | direct  | 


### Commands
#### Extract
| UnRAR cmd | unar cmd | wrapper implementation |
|--|--|--|
| `e` | not supported | not implemented |
| `x` | `unar`  | direct  | 

UnRAR command `e` extracts files without an archived path. Unarchiver doesn’t support this behaviour and therefore it would need to be simulated by this wrapper. Unfortunately, this would be quite a complex feature for example because of the interactivity when files conflicts emerge and therefore it’s not implemented within this wrapper.

#### List 
UnRAR supports many variants for listing the information about the archive. `l[t[a],b]` for listing of a archive  `[technical[all],bare]` and `v[t[a],b]` for verbose listing of a archive. Practically it means the following combinations: `l`, `lt`, `lta`, `lb` ( and vice versa for the `v` option). However, `lsar` supports only basic listing and options `l` and `L` for print more/all information about each file in the archive.

According to my tests, there is no difference in the output for `l` and `v` command except for plain `unrar l` and `unrar v`, where `unrar v` adds `packed` and `ratio` column to the output. As the purpose of this wrapper is not to precisely simulate the output, the following simplified projection was used:

| UnRAR cmd| lsar cmd | 
|--|--|
| `lb`, `vb`  | `lsar` |
| `l`, `v` | `lsar -l` |
| `lt`, `lta`,`vt`, `vta` | `lsar -L` |

#### Test
| UnRAR cmd | lsar cmd | wrapper implementation
|--|--|--|
| `t` | `-t` |direct

#### Print
| UnRAR cmd | unar cmd | wrapper implementation
|--|--|--|
| `p` | not supported | not implemented
UnRAR's `p` command simply prints the file to stdout. It's not supported in unar and as I don't find this command critical, I didn't implement it.

### Options
UnRAR contains many options but only the following are directly supported in the Unarchiver. Simulation of the other options is beyond the scope of this wrapper.

|UnRAR opt| unar/lsar opt|  wrapper implementation
|--|--|--|
| `-o+` | `unar-force-overwrite` | direct
| `-o-` | `unar -force-skip`| direct
| `-or` | `unar -force-rename`| direct
| `-p[password]` | `p PASSWORD`| direct

For UnRAR, all these options can be used with all commands, even if it doesn't make any sense. In that case, it's simply ignored (e.g. when you use `-o+` with `l` command). Based on what is supported in `unar` I decided to support these options only for extract command, with the exception of `-p` that is supported for all commands. 

#### Default options

If the archive has no directory (i.e. files are present directly in the archive) then UnRAR unpack them as is. But unar create a containing directory by default if there is more than one top-level file or folder. Because of this, we need to use `-D, -no-directory` unar option as default. This option means to never create an extra containing directory for the contents of the unpacked archive.

### Return codes

UnRAR supports many return codes that indicate what was wrong (e.g. wrong password, write error, file create error etc.). However, Unarchiver uses only two basic return codes - 0 (success) and 1 (error). As it's impossible to translate return code 1 to any other more specific description of the error, only these two codes are supported by this wrapper with the addition of code 2 that indicates wrapper argument error.

## Tests

This project contains two types of tests - unit and functional. Unit tests test the basic functionality of the particular python functions. Functional tests perform tests on real RAR archives (located in `tests/testdata` directory).

If you want to run unit tests then run `python3 -m unittest tests.test_unrar_wrapper` from the main directory.

If you want to run functional tests then run `./tests/functional_tests.sh  tests/testdata/functional/ unrar_wrapper.py` from the main directory.


