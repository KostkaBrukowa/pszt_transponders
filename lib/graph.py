"""
Map represents the map of all points in the problem.
"""
import numpy as np
from typing import List, Tuple
from .graphical import Graphical


def euclidean_distance(a, b):
    '''
    Calculates the euclidean distance between two points(2-tuples)
    Parameters
    ----------
    a,b : points
        points to calculate distance between them
    Returns
    -------
    float
        euclidean distance between points
    '''
    diff_x = (a[0] - b[0])
    diff_y = (a[1] - b[1])
    return np.sqrt(diff_x*diff_x + diff_y*diff_y) * 69


class Graph():
    def __init__(self, graphical: Graphical, distance_function='euclidean') -> None:
        '''
        Builds the map from the file given in filename kwarg
        or from array of points(2-tuples). Raises exception
        when none of arguments were specified
        '''
        if distance_function == 'euclidean':
            self.distance_function = euclidean_distance
        else:
            raise AttributeError('Function was not specified')

        self.graphical = graphical
        self.points = [node[1] for node in self.graphical.nodes]

        self._build_dist_map()

    def _build_dist_map(self):
        '''
        builds 2d array of all given points. This array
        allows to retrieve the distance from node to
        any other node in the map
        '''
        self.dimension = len(self.graphical.nodes)
        self._dist_map = np.zeros([self.dimension, self.dimension])

        nodes = self.graphical.nodes

        for i, node_1 in enumerate(nodes):
            for j, node_2 in enumerate(nodes[:i]):
                if self.graphical.are_neighbors(node_1, node_2):
                    dist = self.distance_function(node_1[1], node_2[1])
                else:
                    dist = float("inf")
                self._dist_map[i, j] = self._dist_map[j, i] = dist

    def dist_map(self):
        return self._dist_map

    def distance(self, point_index_1: int, point_index_2: int):
        '''
        Returns the distance between two points identified by their id's
        Parameters
        ----------
        point_index_1,point_index_2 : int
            id's of the points
        Returns
        -------
        float
            distance between two points
        '''
        return self._dist_map[point_index_1, point_index_2]

    def path_length(self, path: List[int]):
        if len(path) == 0:
            return 0

        length = 0
        last_node = path[0]
        for node in path[1:]:
            length += self.distance(last_node, node)
            last_node = node

        return length

    def get_point(self, index: int) -> Tuple[float, float]:
        return self.points[index]

    def get_points_count(self):
        return len(self.points)
