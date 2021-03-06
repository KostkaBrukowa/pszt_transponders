from .telecommunication import Demand


def read_demands(root, graph):

    def reconstruct_path(source, xml_path):
        path = []

        for link in xml_path.findall('linkId'):
            link_node_1 = int(link.text.split('_')[1])
            link_node_2 = int(link.text.split('_')[2])
            # current_node = link_node_1 if path[-1] == link_node_2 else link_node_2
            edge = min(link_node_1, link_node_2), max(link_node_1, link_node_2)
            path.append(edge)

        return graph.path_length(path), path

    demands=[]
    xml_demands=root.find('demands').findall('demand')
    for index, demand in enumerate(xml_demands):
        source_index=demand.attrib['id'].split('_')[1]
        target_index=demand.attrib['id'].split('_')[2]
        demand_bitrate=float(demand.find('demandValue').text)
        paths=[reconstruct_path(source_index, path) for path in demand.find(
            'admissiblePaths').findall('admissiblePath')]

        demands.append(Demand(index, source_index,
                              target_index, demand_bitrate, paths))

    return demands
