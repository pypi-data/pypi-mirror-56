#!/usr/bin/env python

# Copyright 2018 Informatics Matters Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function
import inspect, os, sys, gzip, json, uuid
from math import log10, floor
from pipelines_utils.BasicObjectWriter import BasicObjectWriter
from pipelines_utils.TsvWriter import TsvWriter


def log(*args, **kwargs):
    """Log output to STDERR
    """
    print(*args, file=sys.stderr, **kwargs)


def round_sig(x, sig):
    """Round the number to the specified number of significant figures"""
    return round(x, sig - int(floor(log10(abs(x)))) - 1)


def open_file(filename, as_text=False):
    """Open the file gunzipping it if it ends with .gz.
    If as_text the file is opened in text mode,
    otherwise the file's opened in binary mode."""
    if filename.lower().endswith('.gz'):
        if as_text:
            return gzip.open(filename, 'rt')
        else:
            return gzip.open(filename, 'rb')
    else:
        if as_text:
            return open(filename, 'rt')
        else:
            return open(filename, 'rb')


def create_simple_writer(outputDef, defaultOutput, outputFormat, fieldNames,
                         compress=True, valueClassMappings=None,
                         datasetMetaProps=None, fieldMetaProps=None):
    """Create a simple writer suitable for writing flat data
    e.g. as BasicObject or TSV."""

    if not outputDef:
        outputBase = defaultOutput
    else:
        outputBase = outputDef

    if outputFormat == 'json':
        write_squonk_datasetmetadata(outputBase, True, valueClassMappings,
                                     datasetMetaProps, fieldMetaProps)
        return BasicObjectWriter(open_output(outputDef, 'data', compress)), outputBase

    elif outputFormat == 'tsv':
        return TsvWriter(open_output(outputDef, 'tsv', compress), fieldNames), outputBase

    else:
        raise ValueError("Unsupported format: " + outputFormat)

def determine_output_format(outformat):
    if outformat:
        return outformat
    else:
        log("No output format specified - assuming sdf")
        return 'sdf'

def open_output(basename, ext, compress):
    if basename:
        fname = basename + '.' + ext
        if compress:
            fname += ".gz"
            return gzip.open(fname, 'at')
        else:
            return open(fname, 'w+')
    else:
        if compress:
            # TODO - work out how to write compressed data to STDOUT
            return sys.stdout
        else:
            return sys.stdout


def write_squonk_datasetmetadata(outputBase, thinOutput, valueClassMappings, datasetMetaProps, fieldMetaProps, size=None):
    """This is a temp hack to write the minimal metadata that Squonk needs.
    Will needs to be replaced with something that allows something more complete to be written.

    :param outputBase: Base name for the file to write to
    :param thinOutput: Write only new data, not structures. Result type will be BasicObject
    :param valueClasses: A dict that describes the Java class of the value properties (used by Squonk)
    :param datasetMetaProps: A dict with metadata properties that describe the datset as a whole.
            The keys used for these metadata are up to the user, but common ones include source, description, created, history.
    :param fieldMetaProps: A list of dicts with the additional field metadata. Each dict has a key named fieldName whose value
            is the name of the field being described, and a key name values wholes values is a map of metadata properties.
            The keys used for these metadata are up to the user, but common ones include source, description, created, history.
    """
    meta = {}
    props = {}
    # TODO add created property - how to handle date formats?
    if datasetMetaProps:
        props.update(datasetMetaProps)

    if fieldMetaProps:
        meta["fieldMetaProps"] = fieldMetaProps

    if len(props) > 0:
        meta["properties"] = props

    if valueClassMappings:
        meta["valueClassMappings"] = valueClassMappings
    if thinOutput:
        meta['type'] = 'org.squonk.types.BasicObject'
    else:
        meta['type'] = 'org.squonk.types.MoleculeObject'
    if size != None:
        meta['size'] = size
    s = json.dumps(meta)
    meta = open(outputBase + '.metadata', 'w')
    meta.write(s)
    meta.close()


def write_metrics(baseName, values):
    """Write the metrics data

    :param baseName: The base name of the output files.
                     e.g. extensions will be appended to this base name
    :param values dictionary of values to write
    """
    m = open(baseName  + '_metrics.txt', 'w')
    for key in values:
        m.write(key + '=' + str(values[key]) + "\n")
    m.flush()
    m.close()


def generate_molecule_object_dict(source, format, values):
    """Generate a dictionary that represents a Squonk MoleculeObject when
    written as JSON

    :param source: Molecules in molfile or smiles format
    :param format: The format of the molecule. Either 'mol' or 'smiles'
    :param values: Optional dict of values (properties) for the MoleculeObject
    """
    m = {"uuid": str(uuid.uuid4()), "source": source, "format": format}
    if values:
        m["values"] = values
    return m


def get_undecorated_calling_module():
    """Returns the module name of the caller's calling module.
    If a.py makes a call to b() in b.py, b() can get the name of the
    calling module (i.e. a) by calling get_undecorated_calling_module().

    The module also includes its full path.

    As the name suggests, this does not work for decorated functions.
    """
    frame = inspect.stack()[2]
    module = inspect.getmodule(frame[0])
    # Return the module's file and its path
    # and omit the extension...
    # so /a/c.py becomes /a/c
    return module.__file__.rsplit('.', 1)[0]
