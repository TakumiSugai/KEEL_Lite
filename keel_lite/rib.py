from dataclasses import dataclass, field

import numpy as np

from typing import List

from .facet import Facet

@dataclass
class Rib:

    edges: list = field(default_factory=list)
    position: float = field(default=0.)

    def write_stl_beam(self, keel, former_rib_edges, f):
        edges_count = len(self.edges)
        if self.edges is None or edges_count <= 2:
            return None
        return_edges = []
        for edge in self.edges:
            translated_edge = np.dot(np.array([edge[0], edge[1], 0., 1.]), keel.translation(self.position))
            return_edges.append(translated_edge)
        if former_rib_edges is not None \
            and len(former_rib_edges) != 0 \
            and len(return_edges) != 0:
            xy_cross_product = self.edges_xy_only_cross_product_trial()
            Rib.write_stl_inter_edges(former_rib_edges, return_edges, xy_cross_product, f)
        return return_edges

    def write_stl_start(self, keel, f):
        edges_count = len(self.edges)
        if edges_count <= 2:
            return
        else:
            xy_cross_product = self.edges_xy_only_cross_product_trial()
            if xy_cross_product < 0.:
                for i in range(edges_count - 2):
                    facet = Facet()
                    facet.vertex_1 = np.array([self.edges[0][0], self.edges[0][1], 0., 1.])
                    facet.vertex_2 = np.array([self.edges[i+1][0], self.edges[i+1][1], 0., 1.])
                    facet.vertex_3 = np.array([self.edges[i+2][0], self.edges[i+2][1], 0., 1.])
                    facet.translation(keel.translation(self.position))
                    facet.calc_normal()
                    facet.write(f)
            elif xy_cross_product > 0.:
                for i in range(edges_count - 2):
                    facet = Facet()
                    facet.vertex_1 = np.array([self.edges[0][0], self.edges[0][1], 0., 1.])
                    facet.vertex_2 = np.array([self.edges[i+2][0], self.edges[i+2][1], 0., 1.])
                    facet.vertex_3 = np.array([self.edges[i+1][0], self.edges[i+1][1], 0., 1.])
                    facet.translation(keel.translation(self.position))
                    facet.calc_normal()
                    facet.write(f)

    def write_stl_end(self, keel, f):
        edges_count = len(self.edges)
        if edges_count <= 2:
            return
        else:
            xy_cross_product = self.edges_xy_only_cross_product_trial()
            if xy_cross_product < 0.:
                for i in range(edges_count - 2):
                    facet = Facet()
                    facet.vertex_1 = np.array([self.edges[0][0], self.edges[0][1], 0., 1.])
                    facet.vertex_2 = np.array([self.edges[i+2][0], self.edges[i+2][1], 0., 1.])
                    facet.vertex_3 = np.array([self.edges[i+1][0], self.edges[i+1][1], 0., 1.])
                    facet.translation(keel.translation(self.position))
                    facet.calc_normal()
                    facet.write(f)
            elif xy_cross_product > 0.:
                for i in range(edges_count - 2):
                    facet = Facet()
                    facet.vertex_1 = np.array([self.edges[0][0], self.edges[0][1], 0., 1.])
                    facet.vertex_2 = np.array([self.edges[i+1][0], self.edges[i+1][1], 0., 1.])
                    facet.vertex_3 = np.array([self.edges[i+2][0], self.edges[i+2][1], 0., 1.])
                    facet.translation(keel.translation(self.position))
                    facet.calc_normal()
                    facet.write(f)
    
    def edges_xy_only_cross_product_trial(self):
        point_zero = np.array([self.edges[0][0], self.edges[0][1]])
        point_one = np.array([self.edges[1][0], self.edges[1][1]])
        point_two = np.array([self.edges[2][0], self.edges[2][1]])
        vector_one = point_one - point_zero
        vector_two = point_two - point_zero
        return np.cross(vector_one, vector_two)

    @staticmethod
    def write_stl_inter_edges(former_rib_edges, edges, xy_cross_product, f):
        edges_count = len(edges)
        if xy_cross_product < 0.:
            for i in range(edges_count):
                facet = Facet()
                facet.vertex_1 = edges[i]
                facet.vertex_2 = former_rib_edges[i-1]#i==0の時も成立
                facet.vertex_3 = edges[i-1]
                facet.calc_normal()
                facet.write(f)

                facet = Facet()
                facet.vertex_1 = edges[i]
                facet.vertex_2 = former_rib_edges[i]
                facet.vertex_3 = former_rib_edges[i-1]
                facet.calc_normal()
                facet.write(f)
        elif xy_cross_product > 0.:
            for i in range(edges_count):
                facet = Facet()
                facet.vertex_1 = edges[i]
                facet.vertex_2 = edges[i-1]
                facet.vertex_3 = former_rib_edges[i-1]
                facet.calc_normal()
                facet.write(f)

                facet = Facet()
                facet.vertex_1 = edges[i]
                facet.vertex_2 = former_rib_edges[i-1]
                facet.vertex_3 = former_rib_edges[i]
                facet.calc_normal()
                facet.write(f)
            
