#!/usr/bin/env python
import os
import shutil
from glob import glob
from pathlib import Path
import xml.etree.ElementTree as ET
from tempfile import TemporaryDirectory as td

from fuck_yes24py.utils import zipdirs

DEBUG = False

MAGIC_DIR = 'Styles'
POSTFIX = ".fuck.css"

DC = "{http://purl.org/dc/elements/1.1/}"
OPF = "{http://www.idpf.org/2007/opf}"


def pathify(func):
    def wrapper(path=None):
        if path:
            path = Path(path)
        func(path)
    return wrapper


@pathify
def parse(path):
    if not (path / 'OEBPS').exists():
        return

    opf_path = path / 'OEBPS/content.opf'
    root = ET.parse(opf_path)

    title = root.find(f".//{DC}title").text
    creator = root.find(f".//{DC}creator").text

    oebps_path = path / 'OEBPS'
    magic_path = oebps_path / MAGIC_DIR
    os.makedirs(magic_path, exist_ok=True)

    #################
    # 1. HTML -> CSS
    #################

    items = root.findall(f".//{OPF}item")

    paths = {}
    for item in items:
        if item.attrib['media-type'] != 'application/xhtml+xml':
            continue

        src = oebps_path / Path(item.attrib['href'])
        dst = magic_path / (src.name + POSTFIX)
        shutil.copyfile(src, dst)

        paths[src] = dst

    #################
    # 2. Decode
    #################

    while True:
        answer = input(" [*] Open {} (WAIT until 100% [y]/n)?".format(title))
        if answer.lower() == 'n':
            return

        bdb_path = path / ".bdb_view"
        if bdb_path.exists():
            break

    #################
    # 3. Build EPUB
    #################

    tmp_path = Path(str(path) + "_decrypt")
    epub_path = f"{title}.epub"

    if os.path.exists(tmp_path): shutil.rmtree(tmp_path)
    if os.path.exists(epub_path): shutil.rmtree(epub_path)

    bdb_path = path / ".bdb_view"
    shutil.copytree(bdb_path, tmp_path)

    for src, dst in paths.items():
        if not DEBUG: os.remove(dst)
        new_src = bdb_path / '/'.join(dst._parts[1:])
        new_dst = tmp_path / '/'.join(src._parts[1:])
        shutil.move(new_src, new_dst)

    epub_path = "{}.epub".format(title)
    if os.path.exists(epub_path):
        shutil.rmtree(epub_path)

    os.chdir(tmp_path)

    zipdirs('mimetype', epub_path, False)
    zipdirs(['META-INF', 'OEBPS'], epub_path)

    os.chdir('..')
    shutil.move(os.path.join(tmp_path, epub_path), epub_path)

    if os.path.exists(tmp_path) and not DEBUG: shutil.rmtree(tmp_path)


@pathify
def main(path):
    for child in path.iterdir():
        # skip _CremaLogs, _decrypt, __pycache__
        if child.is_dir() and \
                all(x not in child.name for x in ("_", ".epub")) and \
                not str(child).startswith('.'):
            parse(child)
