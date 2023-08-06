import xml.dom.minidom
import json
import shutil
import os
import re


def read_file_string(abs_file):
    f = open(abs_file, "r")
    content = f.read()
    f.close()
    return content


def read_file_array(abs_file):
    f = open(abs_file, "r")
    content = f.readlines()
    f.close()
    return content


def read_file_binary(abs_file):
    f = open(abs_file, "rb")
    content = f.read()
    f.close()
    return content


def write_file(abs_file, content):
    f = open(abs_file, "w")
    stripped_content = re.sub(r'\t*\r*\n*', '', content)
    try:
        f.write(xml.dom.minidom.parseString(stripped_content).toprettyxml())
    except xml.parsers.expat.ExpatError:
        try:
            f.write(json.dumps(json.loads(stripped_content), indent=4))
        except json.decoder.JSONDecodeError:
            f.write(content)
    f.close()


def copy_dir_files(src_folder, dst_folder):
    for (_, _, copy_files) in os.walk(src_folder, topdown=True):
        for copy_file in copy_files:
            shutil.copyfile(os.path.join(src_folder, copy_file), os.path.join(dst_folder, copy_file))


# method that adds _n to a filename, where n is a counter to indicate multiple output files
def add_suffix(filename, suf):
    return ("_" + str(suf) + ".").join(filename.rsplit(".", 1))
