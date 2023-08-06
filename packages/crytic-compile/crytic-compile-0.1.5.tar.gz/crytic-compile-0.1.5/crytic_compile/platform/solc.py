import os
import json
import logging
import subprocess
import re

from .types import Type
from ..utils.naming import (
    extract_filename,
    extract_name,
    combine_filename_name,
    convert_filename,
)
from .exceptions import InvalidCompilation
from ..compiler.compiler import CompilerVersion

logger = logging.getLogger("CryticCompile")


def compile(crytic_compile, target, **kwargs):
    crytic_compile.type = Type.SOLC
    solc = kwargs.get("solc", "solc")
    solc_disable_warnings = kwargs.get("solc_disable_warnings", False)
    solc_arguments = kwargs.get("solc_args", "")
    solc_remaps = kwargs.get("solc_remaps", None)
    solc_working_dir = kwargs.get("solc_working_dir", None)

    crytic_compile.compiler_version = CompilerVersion(
        compiler="solc",
        version=get_version(solc),
        optimized=_is_optimized(solc_arguments),
    )

    # From config file, solcs is a dict (version -> path)
    # From command line, solc is a list
    # The guessing of version only works from config file
    # This is to prevent too complex command line
    solcs_path = kwargs.get("solc_solcs_bin")
    # solcs_env is always a list. It matches solc-select list
    solcs_env = kwargs.get("solc_solcs_select")

    if solcs_path:
        if not isinstance(solcs_path, dict):
            solcs_path = solcs_path.split(",")
        targets_json = _run_solcs_path(
            crytic_compile,
            target,
            solcs_path,
            solc_disable_warnings,
            solc_arguments,
            solc_remaps=solc_remaps,
            working_dir=solc_working_dir,
        )

    elif solcs_env:
        solcs_env = solcs_env.split(",")
        targets_json = _run_solcs_env(
            crytic_compile,
            target,
            solc,
            solc_disable_warnings,
            solc_arguments,
            solcs_env=solcs_env,
            solc_remaps=solc_remaps,
            working_dir=solc_working_dir,
        )

    else:
        targets_json = _run_solc(
            crytic_compile,
            target,
            solc,
            solc_disable_warnings,
            solc_arguments,
            solc_remaps=solc_remaps,
            working_dir=solc_working_dir,
        )

    if crytic_compile.compiler_version.version in [f"0.4.{x}" for x in range(0, 10)]:
        skip_filename = True
    else:
        skip_filename = False

    if "contracts" in targets_json:
        for original_contract_name, info in targets_json["contracts"].items():
            contract_name = extract_name(original_contract_name)
            contract_filename = extract_filename(original_contract_name)
            # for solc < 0.4.10 we cant retrieve the filename from the ast
            if skip_filename:
                contract_filename = convert_filename(
                    target,
                    _relative_to_short,
                    crytic_compile,
                    working_dir=solc_working_dir,
                )
            else:
                contract_filename = convert_filename(
                    contract_filename,
                    _relative_to_short,
                    crytic_compile,
                    working_dir=solc_working_dir,
                )
            crytic_compile.contracts_names.add(contract_name)
            crytic_compile.contracts_filenames[contract_name] = contract_filename
            crytic_compile.abis[contract_name] = json.loads(info["abi"])
            crytic_compile.bytecodes_init[contract_name] = info["bin"]
            crytic_compile.bytecodes_runtime[contract_name] = info["bin-runtime"]
            crytic_compile.srcmaps_init[contract_name] = info["srcmap"].split(";")
            crytic_compile.srcmaps_runtime[contract_name] = info[
                "srcmap-runtime"
            ].split(";")

    if "sources" in targets_json:
        for path, info in targets_json["sources"].items():
            if skip_filename:
                path = convert_filename(
                    target,
                    _relative_to_short,
                    crytic_compile,
                    working_dir=solc_working_dir,
                )
            else:
                path = convert_filename(
                    path,
                    _relative_to_short,
                    crytic_compile,
                    working_dir=solc_working_dir,
                )
            crytic_compile.filenames.add(path)
            crytic_compile.asts[path.absolute] = info["AST"]


def is_solc(target):
    return os.path.isfile(target) and target.endswith(".sol")


def is_dependency(_path):
    return False


def export(crytic_compile, **kwargs):
    # Obtain objects to represent each contract
    contracts = dict()
    for contract_name in crytic_compile.contracts_names:
        abi = str(crytic_compile.abi(contract_name))
        abi = abi.replace("'", '"')
        abi = abi.replace("True", "true")
        abi = abi.replace("False", "false")
        abi = abi.replace(" ", "")
        exported_name = combine_filename_name(
            crytic_compile.contracts_filenames[contract_name].absolute, contract_name
        )
        contracts[exported_name] = {
            "srcmap": ";".join(crytic_compile.srcmap_init(contract_name)),
            "srcmap-runtime": ";".join(crytic_compile.srcmap_runtime(contract_name)),
            "abi": abi,
            "bin": crytic_compile.bytecode_init(contract_name),
            "bin-runtime": crytic_compile.bytecode_runtime(contract_name),
        }

    # Create additional informational objects.
    sources = {
        filename: {"AST": ast} for (filename, ast) in crytic_compile.asts.items()
    }
    source_list = [x.absolute for x in crytic_compile.filenames]

    # Create our root object to contain the contracts and other information.
    output = {"sources": sources, "sourceList": source_list, "contracts": contracts}

    # If we have an export directory specified, we output the JSON.
    export_dir = kwargs.get("export_dir", None)
    if export_dir:
        if not os.path.exists(export_dir):
            os.makedirs(export_dir)
        path = os.path.join(export_dir, "combined_solc.json")

        with open(path, "w", encoding="utf8") as f:
            json.dump(output, f)
        return path
    return None


def get_version(solc):
    cmd = [solc, "--version"]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, _ = process.communicate()
    stdout = stdout.decode()  # convert bytestrings to unicode strings
    version = re.findall("\d+\.\d+\.\d+", stdout)
    assert len(version)
    return version[0]


def _is_optimized(solc_arguments):
    if solc_arguments:
        return "--optimize" in solc_arguments
    return False


def _run_solc(
    crytic_compile,
    filename,
    solc,
    solc_disable_warnings,
    solc_arguments,
    solc_remaps=None,
    env=None,
    working_dir=None,
):
    """
    Note: Ensure that crytic_compile.compiler_version is set prior calling _run_solc
    :param crytic_compile:
    :param filename:
    :param solc:
    :param solc_disable_warnings:
    :param solc_arguments:
    :param solc_remaps:
    :param env:
    :param working_dir:
    :return:
    """
    if not os.path.isfile(filename):
        raise InvalidCompilation(
            "{} does not exist (are you in the correct directory?)".format(filename)
        )

    if not filename.endswith(".sol"):
        raise InvalidCompilation("Incorrect file format")

    compiler_version = crytic_compile.compiler_version
    assert compiler_version
    if compiler_version.version in [
        f"0.4.{x}" for x in range(0, 12)
    ] or compiler_version.version.startswith("0.3"):
        options = "abi,ast,bin,bin-runtime,srcmap,srcmap-runtime"
    else:
        options = "abi,ast,bin,bin-runtime,srcmap,srcmap-runtime,hashes,compact-format"

    cmd = [solc]
    if solc_remaps:
        if isinstance(solc_remaps, str):
            solc_remaps = solc_remaps.split(" ")
        cmd += solc_remaps
    cmd += [filename, "--combined-json", options]
    if solc_arguments:
        # To parse, we first split the string on each '--'
        solc_args = solc_arguments.split("--")
        # Split each argument on the first space found
        # One solc option may have multiple argument sepparated with ' '
        # For example: --allow-paths /tmp .
        # split() removes the delimiter, so we add it again
        solc_args = [("--" + x).split(" ", 1) for x in solc_args if x]
        # Flat the list of list
        solc_args = [item for sublist in solc_args for item in sublist if item]
        cmd += solc_args

    additional_kwargs = {"cwd": working_dir} if working_dir else {}

    if not compiler_version.version in [f"0.4.{x}" for x in range(0, 11)]:
        # Add . as default allowed path
        if "--allow-paths" not in cmd:
            relative_filepath = filename

            if not working_dir:
                working_dir = os.getcwd()

            if relative_filepath.startswith(working_dir):
                relative_filepath = relative_filepath[len(working_dir) + 1 :]

            cmd += ["--allow-paths", ".", relative_filepath]

    if env:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
            **additional_kwargs,
        )
    else:
        process = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, **additional_kwargs
        )
    stdout, stderr = process.communicate()
    stdout, stderr = (
        stdout.decode(),
        stderr.decode(),
    )  # convert bytestrings to unicode strings

    if stderr and (not solc_disable_warnings):
        logger.info("Compilation warnings/errors on %s:\n%s", filename, stderr)

    try:
        ret = json.loads(stdout)
        return ret
    except json.decoder.JSONDecodeError:
        raise InvalidCompilation(f"Invalid solc compilation {stderr}")


def _run_solcs_path(
    crytic_compile,
    filename,
    solcs_path,
    solc_disable_warnings,
    solc_arguments,
    solc_remaps=None,
    env=None,
    working_dir=None,
):
    targets_json = None
    if isinstance(solcs_path, dict):
        guessed_solcs = _guess_solc(filename, working_dir)
        for guessed_solc in guessed_solcs:
            if not guessed_solc in solcs_path:
                continue
            try:
                targets_json = _run_solc(
                    crytic_compile,
                    filename,
                    solcs_path[guessed_solc],
                    solc_disable_warnings,
                    solc_arguments,
                    solc_remaps=solc_remaps,
                    env=env,
                    working_dir=working_dir,
                )
            except InvalidCompilation:
                pass

    if not targets_json:
        solc_bins = solcs_path.values() if isinstance(solcs_path, dict) else solcs_path

        for solc_bin in solc_bins:
            try:
                targets_json = _run_solc(
                    crytic_compile,
                    filename,
                    solc_bin,
                    solc_disable_warnings,
                    solc_arguments,
                    solc_remaps=solc_remaps,
                    env=env,
                    working_dir=working_dir,
                )
            except InvalidCompilation:
                pass

    if not targets_json:
        raise InvalidCompilation(
            "Invalid solc compilation, none of the solc versions provided worked"
        )

    return targets_json


def _run_solcs_env(
    crytic_compile,
    filename,
    solc,
    solc_disable_warnings,
    solc_arguments,
    solc_remaps=None,
    env=None,
    working_dir=None,
    solcs_env=None,
):
    env = dict(os.environ) if env is None else env
    targets_json = None
    guessed_solcs = _guess_solc(filename, working_dir)
    for guessed_solc in guessed_solcs:
        if not guessed_solc in solcs_env:
            continue
        try:
            env["SOLC_VERSION"] = guessed_solc
            targets_json = _run_solc(
                crytic_compile,
                filename,
                solc,
                solc_disable_warnings,
                solc_arguments,
                solc_remaps=solc_remaps,
                env=env,
                working_dir=working_dir,
            )
        except InvalidCompilation:
            pass

    if not targets_json:
        solc_versions_env = solcs_env

        for version_env in solc_versions_env:
            try:
                env["SOLC_VERSION"] = version_env
                targets_json = _run_solc(
                    crytic_compile,
                    filename,
                    solc,
                    solc_disable_warnings,
                    solc_arguments,
                    solc_remaps=solc_remaps,
                    env=env,
                    working_dir=working_dir,
                )
            except InvalidCompilation:
                pass

    if not targets_json:
        raise InvalidCompilation(
            "Invalid solc compilation, none of the solc versions provided worked"
        )

    return targets_json


PATTERN = re.compile("pragma solidity[\^|>=|<=]?[ ]+?(\d+\.\d+\.\d+)")


def _guess_solc(target, solc_working_dir):
    if solc_working_dir:
        target = os.path.join(solc_working_dir, target)
    with open(target, encoding="utf8") as f:
        buf = f.read()
        return PATTERN.findall(buf)


def _relative_to_short(relative):
    return relative
