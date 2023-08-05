# SPDX-FileCopyrightText: 2017-2019 Free Software Foundation Europe e.V.
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""All linting happens here. The linting here is nothing more than reading
the reports and printing some conclusions.
"""

import sys
from gettext import gettext as _
from typing import Iterable

from . import __REUSE_version__
from ._util import PathType
from .project import create_project
from .report import ProjectReport


def _write_element(element, out=sys.stdout):
    out.write("* ")
    out.write(str(element))
    out.write("\n")


def lint(report: ProjectReport, out=sys.stdout) -> bool:
    """Lint the entire project."""
    files_without_cali = lint_files_without_copyright_and_licensing(
        report, out
    )
    bad_licenses_result = lint_bad_licenses(report, out)
    missing_licenses_result = lint_missing_licenses(report, out)
    read_errors_result = lint_read_errors(report, out)

    lint_summary(report, out=out)

    success = not any(
        any(result)
        for result in (
            files_without_cali,
            bad_licenses_result,
            missing_licenses_result,
            read_errors_result,
            # TODO: Should this be a separate entry if it's already in the
            # summary?
            report.unused_licenses,
        )
    )

    out.write("\n")
    if success:
        out.write(
            _(
                "Congratulations! Your project is compliant with version "
                "{} of the REUSE Specification :-)"
            ).format(__REUSE_version__)
        )
    else:
        out.write(
            _(
                "Unfortunately, your project is not compliant with version "
                "{} of the REUSE Specification :-("
            ).format(__REUSE_version__)
        )
    out.write("\n")

    return success


def lint_bad_licenses(report: ProjectReport, out=sys.stdout) -> Iterable[str]:
    """Lint for bad licenses. Bad licenses are licenses that are not in the
    SPDX License List or do not start with LicenseRef-.
    """
    bad_files = []

    if report.bad_licenses:
        out.write("# ")
        out.write(_("BAD LICENSES"))
        out.write("\n")
        for lic, files in sorted(report.bad_licenses.items()):
            out.write("\n")
            out.write(_("'{}' found in:").format(lic))
            out.write("\n")
            for file_ in sorted(files):
                bad_files.append(file_)
                _write_element(file_, out=out)
        out.write("\n\n")

    return bad_files


def lint_missing_licenses(
    report: ProjectReport, out=sys.stdout
) -> Iterable[str]:
    """Lint for missing licenses. A license is missing when it is referenced
    in a file, but cannot be found.
    """
    bad_files = []

    if report.missing_licenses:
        out.write("# ")
        out.write(_("MISSING LICENSES"))
        out.write("\n")

        for lic, files in sorted(report.missing_licenses.items()):
            out.write("\n")
            out.write(_("'{}' found in:").format(lic))
            out.write("\n")
            for file_ in sorted(files):
                bad_files.append(file_)
                _write_element(file_, out=out)
        out.write("\n\n")

    return bad_files


def lint_read_errors(report: ProjectReport, out=sys.stdout) -> Iterable[str]:
    """Lint for read errors."""
    bad_files = []

    if report.read_errors:
        out.write("# ")
        out.write(_("READ ERRORS"))
        out.write("\n\n")
        out.write(_("Could not read:"))
        out.write("\n")
        for file_ in report.read_errors:
            bad_files.append(file_)
            _write_element(file_, out=out)
        out.write("\n\n")

    return bad_files


def lint_files_without_copyright_and_licensing(
    report: ProjectReport, out=sys.stdout
) -> Iterable[str]:
    """Lint for files that do not have copyright or licensing information."""
    # TODO: The below three operations can probably be optimised.
    both = set(report.files_without_copyright) & set(
        report.files_without_licenses
    )
    only_copyright = set(report.files_without_copyright) - both
    only_licensing = set(report.files_without_licenses) - both

    if any((both, only_copyright, only_licensing)):
        out.write("# ")
        out.write(_("MISSING COPYRIGHT AND LICENSING INFORMATION"))
        out.write("\n\n")
        if both:
            out.write(
                _(
                    "The following files have no copyright and licensing "
                    "information:"
                )
            )
            out.write("\n")
            for file_ in sorted(both):
                _write_element(file_, out=out)
            out.write("\n")
        if only_copyright:
            out.write(_("The following files have no copyright information:"))
            out.write("\n")
            for file_ in sorted(only_copyright):
                _write_element(file_, out=out)
            out.write("\n")
        if only_licensing:
            out.write(_("The following files have no licensing information:"))
            out.write("\n")
            for file_ in sorted(only_licensing):
                _write_element(file_, out=out)
            out.write("\n")
        out.write("\n")

    return both | only_copyright | only_licensing


def lint_summary(report: ProjectReport, out=sys.stdout) -> None:
    """Print a summary for linting."""
    out.write("# ")
    out.write(_("SUMMARY"))
    out.write("\n\n")

    file_total = len(report.file_reports)

    out.write("* ")
    out.write(_("Bad licenses:"))
    for i, lic in enumerate(sorted(report.bad_licenses)):
        if i:
            out.write(",")
        out.write(" ")
        out.write(lic)
    out.write("\n")

    out.write("* ")
    out.write(_("Missing licenses:"))
    for i, lic in enumerate(sorted(report.missing_licenses)):
        if i:
            out.write(",")
        out.write(" ")
        out.write(lic)
    out.write("\n")

    out.write("* ")
    out.write(_("Unused licenses:"))
    for i, lic in enumerate(sorted(report.unused_licenses)):
        if i:
            out.write(",")
        out.write(" ")
        out.write(lic)
    out.write("\n")

    out.write("* ")
    out.write(_("Used licenses:"))
    for i, lic in enumerate(sorted(report.used_licenses)):
        if i:
            out.write(",")
        out.write(" ")
        out.write(lic)
    out.write("\n")

    out.write("* ")
    out.write(_("Read errors: {count}".format(count=len(report.read_errors))))
    out.write("\n")

    out.write("* ")
    out.write(
        _(
            "Files with copyright information: {count} / {total}".format(
                count=file_total - len(report.files_without_copyright),
                total=file_total,
            )
        )
    )
    out.write("\n")

    out.write("* ")
    out.write(
        _(
            "Files with license information: {count} / {total}".format(
                count=file_total - len(report.files_without_licenses),
                total=file_total,
            )
        )
    )
    out.write("\n")


def add_arguments(parser):
    """Add arguments to parser."""
    parser.add_argument("path", action="store", nargs="*", type=PathType("r"))


def run(args, out=sys.stdout):
    """List all non-compliant files."""
    project = create_project()
    project.include_submodules = args.include_submodules
    paths = args.path
    if not paths:
        paths = [project.root]

    report = ProjectReport.generate(project, paths, do_checksum=False)
    result = lint(report, out=out)

    return 0 if result else 1
