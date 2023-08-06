# -*- coding: utf-8 -*-

import os
from xml.etree.ElementTree import ElementTree, Element, fromstring
import xmltodict
import json


def readfromxml(in_path):
    tree = ElementTree()
    tree.parse(in_path)
    return tree


def readfromstr(str):
    return ElementTree(fromstring(str))


def write_xml(tree, out_path):
    tree.write(out_path, encoding="utf-8", xml_declaration=True)


def if_match(node, kv_map):
    for key in kv_map:
        if node.get(key) != kv_map.get(key):
            return False
    return True


def find_nodes(tree, path):
    return tree.findall(path)


def find_node(tree, path):
    return tree.find(path)


def find_text(tree, path, defaultValue):
    node = tree.find(path)
    if node is not None:
        return node.text
    return defaultValue


def get_node_by_keyvalue(nodelist, kv_map):
    result_nodes = []
    for node in nodelist:
        if if_match(node, kv_map):
            result_nodes.append(node)
    return result_nodes


def change_node_properties(nodelist, kv_map, is_delete=False):
    for node in nodelist:
        for key in kv_map:
            if is_delete:
                if key in node.attrib:
                    del node.attrib[key]
            else:
                node.set(key, kv_map.get(key))


def change_node_text(nodelist, text, is_add=False, is_delete=False):
    for node in nodelist:
        if is_add:
            node.text += text
        elif is_delete:
            node.text = ""
        else:
            node.text = text


def create_node(tag, property_map, content):
    element = Element(tag, property_map)
    element.text = content
    return element


def add_child_node(nodelist, element):
    for node in nodelist:
        node.append(element)


def del_node_by_tagkeyvalue(nodelist, tag, kv_map):
    for parent_node in nodelist:
        children = list(parent_node)
        for child in children:
            if child.tag == tag and if_match(child, kv_map):
                parent_node.remove(child)


def xmlstrtojson(xmlstr):
    xmlparse = xmltodict.parse(xmlstr)
    jsonstr = json.dumps(xmlparse, ensure_ascii=False, check_circular=False, indent=1)
    return jsonstr


def xmlstrtodict(xmlstr):
    return xmltodict.parse(xmlstr)


def jsontoxml(jsonstr):
    return xmltodict.unparse(jsonstr)


def read_file_as_str(file_path):
    if not os.path.isfile(file_path):
        raise TypeError(file_path + " does not exist")

    all_the_text = open(file_path).read()
    return all_the_text
