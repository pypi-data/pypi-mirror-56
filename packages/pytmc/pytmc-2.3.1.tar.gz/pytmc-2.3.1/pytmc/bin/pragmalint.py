"""
"pytmc pragmalint" is a command line utility for linting PyTMC pragmas in a
given TwinCAT project or source code file
"""

import argparse
import logging
import pathlib
import re
import sys
import types
import textwrap

from .. import parser
from . import util
from .db import LinterError


DESCRIPTION = __doc__
logger = logging.getLogger(__name__)

PRAGMA_START_RE = re.compile('{attribute')
PRAGMA_RE = re.compile(
    r"^{\s*attribute[ \t]+'pytmc'[ \t]*:=[ \t]*'(?P<setting>[\s\S]*)'}$",
    re.MULTILINE
)
PRAGMA_LINE_RE = re.compile(r"([^\r\n$;]*)", re.MULTILINE)
PRAGMA_SETTING_RE = re.compile(
    r"\s*(?P<title>[a-zA-Z0-9]+)\s*:\s*(?P<setting>.*?)\s*$")
PRAGMA_PV_LINE_RE = re.compile(r"pv\s*:")


def build_arg_parser(argparser=None):
    if argparser is None:
        argparser = argparse.ArgumentParser()

    argparser.description = DESCRIPTION
    argparser.formatter_class = argparse.RawTextHelpFormatter

    argparser.add_argument(
        'filename', type=str,
        help='Path to .tsproj project or source code file'
    )

    argparser.add_argument(
        '--markdown', dest='use_markdown',
        action='store_true',
        help='Make output more markdown-friendly, for easier sharing'
    )

    argparser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show all pragmas, including good ones'
    )

    return argparser


def match_single_pragma(code):
    '''
    Given a block of code starting at a pragma, return the pragma up to its
    closing curly brace.
    '''
    curly_count = 0
    for i, char in enumerate(code):
        if char == '{':
            curly_count += 1
        elif char == '}':
            curly_count -= 1
            if i > 0 and curly_count == 0:
                return code[:i + 1]


def find_pragmas(code):
    for match in PRAGMA_START_RE.finditer(code):
        yield match.start(0), match_single_pragma(code[match.start(0):])


def lint_pragma(pragma):
    '''
    Lint a pragma against the PRAGMA_RE regular expression. Raises LinterError
    '''
    if 'pytmc' not in pragma:
        return

    pragma = pragma.strip()
    match = PRAGMA_RE.match(pragma)
    if not match:
        raise LinterError()

    try:
        pragma_setting = match.groupdict()["setting"]
    except KeyError:
        # if no configuration region in the pragma was detected then fail
        raise LinterError()

    config_lines = PRAGMA_LINE_RE.findall(pragma_setting)
    if len(config_lines) == 0:
        raise LinterError("""It is not acceptable to lack configuration lines.
        At a minimum "pv: " must exist""")

    config_lines_detected = 0
    pv_line_detected = 0

    for line in config_lines:
        line_match = PRAGMA_SETTING_RE.match(line)
        if line_match:
            config_lines_detected += 1
            pv_match = PRAGMA_PV_LINE_RE.search(line)
            if pv_match:
                pv_line_detected += 1

    # There shall be at one config line at minimum
    if config_lines_detected <= 0:
        raise LinterError("No configuration line(s) detected in a pragma.")

    # There shall be a config line for pv even if it's just "pv:"
    if pv_line_detected <= 0:
        raise LinterError("No pv line(s) detected in a pragma")

    return match


def _build_map_of_offset_to_line_number(source):
    '''
    For a multiline source file, return {character_pos: line}
    '''
    start_index = 0
    index_to_line_number = {}
    # A slow and bad algorithm, but only to be used in parsing declarations
    # which are rather small
    for line_number, line in enumerate(source.splitlines(), 1):
        for index in range(start_index, start_index + len(line) + 1):
            index_to_line_number[index] = line_number
        start_index += len(line) + 1
    return index_to_line_number


def lint_source(filename, source, verbose=False):
    '''
    Lint `filename` given TwincatItem `source`.

    Parameters
    ----------
    filename : str
        Target file name to be linted.

    source : subclass of pytmc.parser.TwincatItem
        Representation of TwinCAT project chunk in which to search for the
        filename argument

    verbose : bool
        Show more context around the linting process, including all source file
        names and number of pragmas found
    '''
    heading_shown = False
    for decl in source.find(parser.Declaration):
        if not decl.text.strip():
            continue

        offset_to_line_number = _build_map_of_offset_to_line_number(decl.text)

        parent = decl.parent
        path_to_source = []
        while parent is not source:
            if parent.name is not None:
                path_to_source.insert(0, parent.name)
            parent = parent.parent
        pragmas = list(find_pragmas(decl.text))
        if not pragmas:
            continue

        if verbose:
            if not heading_shown:
                print()
                util.sub_heading(f'{filename} ({source.tag})')
                heading_shown = True

            util.sub_sub_heading(
                f'{".".join(path_to_source)}: {decl.tag} - '
                f'{len(pragmas)} pragmas'
            )

        for offset, pragma in pragmas:
            info = dict(
                pragma=pragma,
                filename=filename,
                tag=source.tag,
                line_number=offset_to_line_number.get(offset),
                exception=None,
            )

            try:
                lint_pragma(pragma)
            except LinterError as ex:
                info['exception'] = ex

            yield types.SimpleNamespace(**info)


def main(filename, use_markdown=False, verbose=False):
    proj_path = pathlib.Path(filename)
    project = parser.parse(proj_path)
    pragma_count = 0
    linter_errors = 0

    if hasattr(project, 'plcs'):
        for i, plc in enumerate(project.plcs, 1):
            util.heading(f'PLC Project ({i}): {plc.project_path.stem}')
            for fn, source in plc.source.items():
                for info in lint_source(fn, source, verbose=verbose):
                    pragma_count += 1
                    if info.exception is not None:
                        linter_errors += 1
                        logger.error('Linter error: %s\n%s:line %s: %s',
                                     info.exception, info.filename,
                                     info.line_number,
                                     textwrap.indent(info.pragma, '    '))
    else:
        source = project
        for info in lint_source(filename, source, verbose=verbose):
            pragma_count += 1
            if info.exception is not None:
                linter_errors += 1
                logger.error('Linter error: %s\n%s:line %s: %s',
                             info.exception, info.filename, info.line_number,
                             textwrap.indent(info.pragma, '    '))

    logger.info('Total pragmas found: %d Total linter errors: %d',
                pragma_count, linter_errors)

    if linter_errors > 0:
        sys.exit(1)
