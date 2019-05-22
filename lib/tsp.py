"""
Map represents the map of all points in the problem.
"""
import numpy as np
from typing import List, Tuple
from .graph_resolver import GraphResolver
from .graphical import GraphicalTSP


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
    return np.sqrt(diff_x*diff_x + diff_y*diff_y)


class TSP():
    def __init__(self, graphical_tsp: GraphicalTSP, distance_function ='euclidean') -> None:
        '''
        Builds the map from the file given in filename kwarg
        or from array of points(2-tuples). Raises exception
        when none of arguments were specified
        '''
        if distance_function == 'euclidean':
            self.distance_function = euclidean_distance
        else:
            raise AttributeError('Function was not specified')

        self.graphical_tsp = graphical_tsp
        self.points = [node[1] for node in self.graphical_tsp.nodes]

        self._dist_map = GraphResolver.build_dist_map(graphical_tsp, self.distance_function)
        # self._path_map = GraphResolver.build_path_map(graphical_tsp, self._dist_map)


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

    def get_point(self, index: int) -> Tuple[float, float]:
        return self.points[index]

    def get_points_count(self):
        return len(self.points)
