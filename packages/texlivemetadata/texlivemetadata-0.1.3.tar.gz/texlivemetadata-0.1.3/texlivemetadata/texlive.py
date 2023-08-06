# -*- coding: utf-8 -*-
"""
Get metadata on TexLive installation itself.

Documentation at: https://github.com/YtoTech/python-texlivemetadata

Copyright (c) 2019 Yoan Tournade <yoan@ytotech.com>
Released under MIT License. See LICENSE file.
"""
import subprocess
import re
import datetime
from operator import is_not
from functools import partial

# --------------------
# Texlive version information
# --------------------

TEXLIVE_MODULE_REVISION_REGEX_PATTERN = r"^(\S+):\s+(\d+)$"
TEXLIVE_MODULE_REVISION_REGEX = re.compile(TEXLIVE_MODULE_REVISION_REGEX_PATTERN)


def parse_texlive_module_revision_line(line):
    regex_match = TEXLIVE_MODULE_REVISION_REGEX.match(line)
    if not regex_match:
        raise RuntimeError(
            "Unable to parse TeXLive module revision line ouput: {}".format(line)
        )
    return {
        "module_name": regex_match.group(1),
        "module_revision": regex_match.group(2),
    }


def parse_tlmgr_version_verbose_line(line, line_index):
    if "tlmgr revision" in line:
        version, remaining = line.split("tlmgr revision ")[1].split(" (")
        return {
            "tlmgr_revision": version,
            "tlmgr_revision_date": remaining.split(")")[0],
        }
    if "tlmgr using installation" in line:
        return {
            "texlive_installation_path": line.split("tlmgr using installation: ")[1]
        }
    if "TeX Live" in line and "version" in line:
        return {"texlive_version": line.split("version ")[1]}
    if "Revisions of TeXLive:: modules:" in line:
        return {}
    parsed_module = parse_texlive_module_revision_line(line)
    return {
        "module_revision_{}".format(parsed_module["module_name"]): parsed_module[
            "module_revision"
        ]
    }


def parse_tlmgr_version_verbose(output):
    parsed_entries = {}
    for line_index, line in enumerate(output.splitlines()):
        parsed_entries = {
            **parsed_entries,
            **parse_tlmgr_version_verbose_line(line, line_index),
        }
    # Reshape parsed entries.
    module_revisions = []
    for entry_name, entry_value in parsed_entries.items():
        if "module_revision_" in entry_name:
            module_revisions.append(
                {"name": entry_name.split("module_revision_")[1], "value": entry_value}
            )
    return {
        "tlmgr": {
            "revision": parsed_entries["tlmgr_revision"],
            "revision_date": parsed_entries["tlmgr_revision_date"],
        },
        "texlive": {
            "version": parsed_entries["texlive_version"],
            "installation_path": parsed_entries["texlive_installation_path"],
            "modules": module_revisions,
        },
    }


def get_texlive_version_information():
    cmd = ["tlmgr", "version", "-v"]
    cmd_output = subprocess.run(
        cmd, stdout=subprocess.PIPE, check=True, encoding="utf-8"
    )
    return parse_tlmgr_version_verbose(cmd_output.stdout)
