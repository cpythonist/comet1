#
# Comet 1 standard library command
# Filename: src\\bin\\wc.py
# Copyright (c) 2025, Infinite Inc.
# Written by Thiruvalluvan Kamaraj
# Licensed under the Apache-2.0 License.
#

import os
import sys
import typing  as ty

# Add src\\core to sys.path
srcDir = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(1, os.path.join(srcDir, "core"))
import commons as comm
sys.path.pop(1)

helpStr = (
    b"x\x9cm\x90A\x8b\x021\x0c\x85\xef\xf9\x15\xef\xa8`\xf5\xeeM\xc4u\xf7\xb0"
    b"*\x8e\x9e\xc4Cl\xa33\x10gdZ\x19\x04\x7f\xbcmU\x90e{x\xe4\xf5{$!SV{U\x0e"
    b"\x82\xaei\x1dls\xad\xc3\x00Z\xd5\xf2\xae\xb9v8\xdc\xc2\xcb\x0f\x89\xb6"
    b"\xc5d>\x1b\xa3\xb3\xd8\x99r\x1f\xc5&\xe9\x92\xe8\x1e=\x1fZ\xdca\x8e8V*}"
    b"\xa2\xc9z\xbe\xfd\x9d-6\x05EB\x88\xaf\x08mU\x9f\x10\x1a\x1c$\xb6g\xbdyq"
    b"\x94\xe2\x19\x7f\xc5\xe2/\xa4\xe5j\xf3\xb3\\\x14d,F0\xc6\x96\xdc\xfa\x9c"
    b"\x9e\xa6\xad\x90<\xdb \xf13NN\x89\xff\xdai\xc3N\x1c\xd8\xc3q`2eN\x96\xa2"
    b"\x97\x9c\xfc\x8e\x05\xce\xe2=\x9f\x84\x8cf\x98.\xf19\xe8\xe9M\x97a:\xd9'"
    b"\xcc\xfe\x01A\x94fi"
)


def HELPER_WC(data: str, chars: bool, words: bool, lines: bool) -> list[str]:
    """
    Helper function to calculate word count, line count, and byte count.
    > param data: String to be analysed
    > param bytes_: Count bytes
    > param words: Count words
    > param lines: Count lines
    > return: List of strings containing word count, line count, and byte count
    """
    toPrint = []
    if chars:
        toPrint.append(f"b: {len(data.encode())}")
    if words:
        toPrint.append(f"w: {len(data.split())}")
    if lines:
        toPrint.append(f"l: {len(data.split('\n'))}")
    return toPrint


def WC(varTable: dict[str, str], origPth: str, prevErr: int, cmd: str,
       args: dict[int, str], opts: dict[int, str], fullCmd: str,
       stream: ty.TextIO, op: str, debug: bool) -> int:
    """
    Checks for the existance of a path.
    > param varTable: Variable table
    > param origPth: Path to the interpreter
    > param prevErr: Previous error code
    > param command: Name of the command
    > param args: Dictionary of arguments
    > param opts: Dictionary of options
    > param fullComm: Full command
    > param stream: Original STDOUT
    > param op: Operation next in line to be performed
    > param debug: Is debugging enabled?
    > return: Error code (ref. src\\errCodes.txt)
    """
    optVals    = comm.LOWERLT(opts.values())
    validOpts  = {'b', 'f', 'l', 'w', 'h',
                  "-bytes", "-file", "-lines", "-words", "-help"}
    bytes_     = False
    words      = False
    lines      = False
    isFl       = False
    toPrint    = []

    if opts:
        if tmp := (set(optVals) - validOpts):
            comm.ERR(f"Unknown option(s): {comm.OPTSJOIN(tmp)}")
            return 2
        if 'h' in optVals or "-help" in optVals:
            helpStrTmp = comm.DECOMPSTR(helpStr)
            if isinstance(helpStrTmp, int):
                  return comm.ERR_INVHELPSTRTYPE
            print(helpStrTmp)
            return comm.ERR_SUCCESS

        for pos in opts:
            opt = opts[pos].lower()
            if opt == 'b' or opt == "-bytes":
                bytes_ = True
            elif opt == 'l' or opt == "-lines":
                lines = True
            elif opt == 'w' or opt == "-words":
                words = True
            elif opt == 'f' or opt == "-file":
                if isFl:
                    comm.ERR(f"Cannot accept multiple files")
                    return comm.ERR_INCOPTUSAGE
                if pos + 1 not in args:
                    comm.ERR(f"Missing argument for -{opt}: file")
                    return comm.ERR_INCOPTUSAGE
                txtOrFl = args[pos + 1]
                isFl    = True

    if not bytes_ and not words and not lines:
        bytes_ = True
        words  = True
        lines  = True

    if not args or len(args) != 1:
        comm.ERR("Incorrect format")
        return comm.ERR_INCFORMAT

    if 'f' not in optVals and "-file" not in optVals:
        txtOrFl = args[sorted(args)[0]]

    if isFl:
        if not os.path.isfile(txtOrFl):
            comm.ERR(f"No such file: \"{txtOrFl}\"")
            return comm.ERR_NOFL
        try:
            with open(txtOrFl, buffering=1) as f:
                data = f.read()
        except PermissionError:
            comm.ERR(f"Access is denied: \"{txtOrFl}\"")
            return comm.ERR_PERMDENIED
        except UnicodeDecodeError:
            comm.ERR(f"Cannot decode file: \"{txtOrFl}\"")
            return comm.ERR_CANTDECODE

    else:
        data = txtOrFl

    toPrint = HELPER_WC(data, bytes_, words, lines)
    print("; ".join(toPrint))
    return comm.ERR_SUCCESS
