import numpy as np
from typing import List, Callable
from .graphical import GraphicalTSP


class GraphResolver():

    @staticmethod
    def build_dist_map(graphical: GraphicalTSP, distance_function: Callable[[int, int], float]):
        '''
        builds 2d array of all given points. This array
        allows to retrieve the distance from node to
        any other node in the map
        '''
        dimension = len(graphical.nodes)
        dist_map = np.zeros([dimension, dimension])

        nodes = graphical.nodes

        for i, node_1 in enumerate(nodes):
            for j, node_2 in enumerate(nodes[:i]):
                if graphical.are_neighbors(node_1, node_2):
                    dist = distance_function(node_1[1], node_2[1])
                else:
                    dist = float("inf")
                dist_map[i, j] = dist_map[j, i] = dist

        return dist_map

    @staticmethod
    def build_path_map(graphical: GraphicalTSP, dist_map):
        '''
        Builds the data structure with all possible paths
        from any node to another
        '''
        def findAllPaths(node: int, destination: int,  all_paths: List[List[int]], current_path: List[int]):
            if node == destination:
                all_paths.append(current_path)
                return

            for neighbor in range(dimension):
                if (dist_map[node, neighbor] != float('inf') and neighbor != node and
                        neighbor not in current_path):
                    findAllPaths(neighbor, destination,
                                 all_paths, current_path + [neighbor])

        dimension = len(graphical.nodes)
        path_map = np.ndarray((dimension, dimension), dtype=object)

        nodes = graphical.nodes

        for i, node_1 in enumerate(nodes):
            for j, node_2 in enumerate(nodes[:i]):
                paths: List[List[int]] = []
                findAllPaths(i, j, paths, [i])
                path_map[i, j] = path_map[j, i] = paths

        return path_map
