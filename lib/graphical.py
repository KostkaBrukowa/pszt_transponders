import numpy as np
import xml.etree.ElementTree as ET

from random import randint


class Graphical():
    def __init__(self, root):

        xml_nodes = (root.find('networkStructure')
                          .find('nodes')
                          .findall('node'))

        self.nodes = [self.parse_xml_node(node) for node in xml_nodes]

        xml_links = (root.find('networkStructure')
                          .find('links')
                          .findall('link'))

        self.links = [self.parse_xml_link(link) for link in xml_links]

    def parse_xml_node(self, node):
        city = node.attrib['id']
        x = float(node.find('coordinates').find('x').text)
        y = float(node.find('coordinates').find('y').text)
        return city, (x, y)

    def parse_xml_link(self, node):
        source = node.find('source').text
        target = node.find('target').text
        return source, target

    def are_neighbors(self, node_1, node_2):

        for link in self.links:
            if ((link[0] == node_1[0] and link[1] == node_2[0]) or
                    (link[0] == node_2[0] and link[1] == node_1[0])):
                return True

        return False


if __name__ == "__main__":

    tree = ET.parse('data/polska.xml')
    root = tree.getroot()

    graphical_tsp = Graphical(root)

