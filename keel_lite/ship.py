from dataclasses import dataclass, field

import numpy as np

from .keel import Keel
from .rib import Rib

from typing import List, Any

@dataclass
class Ship:
    keel:Keel = field(default=None)
    ribs:List[Rib] = field(default_factory=list)
    parent:any = field(default=None)
    parents:List[Any] = field(default_factory=list)
    parents_dirty_flag:bool = field(default=False)
    transration_dirty_flag:bool = field(default=False)
    parent_keels_position:float =  field(default=1.)

    smoothing:bool = field(default=False)
    smoothing_from:any = field(default=None)
    smoothing_to:any = field(default=None)

    def length(self):
        return self.keel.length()

    def set_parent(self, parent, position=1.):
        self.parent_keels_position = position
        self.parent = parent
        self.sanitize_keel()
        self.parents = []
        self.get_parents()
        return self

    def get_parents(self):
        self.parents_dirty_flag = False
        if self.parent == None:
            return []
        self.parents = []
        self.parents.extend(self.parent.get_parents())
        self.parents.append(self.parent)
        return self.parents

    def end(self, child):
        child.end = self
        return self

    def relative_vector(self):
        if self.keel is None:
            return None
        return self.keel.end - self.keel.start

    def write_stl(self, f):
        if self.keel is None:
            return
        if self.smoothing:
            pass
            if self.smoothing_from is None\
                or self.smoothing_from.ribs is None or len(self.smoothing_from.ribs) == 0\
                or self.smoothing_to is None\
                or self.smoothing_to.ribs is None or len(self.smoothing_to.ribs) == 0:
                return
            rib_from = self.get_rib_end(self.smoothing_from)
            translated_edges_from = []
            for edge in rib_from.edges:
                translated_edge_from = np.dot(np.array([edge[0], edge[1], 0., 1.]), self.smoothing_from.keel.translation(rib_from.position))
                translated_edges_from.append(translated_edge_from)

            rib_to = self.get_rib_start(self.smoothing_to)
            translated_edges_to = []
            for edge in rib_to.edges:
                translated_edge_to = np.dot(np.array([edge[0], edge[1], 0., 1.]), self.smoothing_to.keel.translation(rib_to.position))
                translated_edges_to.append(translated_edge_to)
            
            xy_cross_product = rib_from.edges_xy_only_cross_product_trial()
            Rib.write_stl_inter_edges(translated_edges_from, translated_edges_to, xy_cross_product, f)
        else:
            if len(self.ribs) == 0:
                return
            rib_start = self.get_rib_start(self)
            rib_start.write_stl_start(self.keel, f)
            rib_end = self.get_rib_end(self)
            rib_end.write_stl_end(self.keel, f)
            former_rib_edges = None
            for rib in self.ribs:
                former_rib_edges = rib.write_stl_beam(self.keel, former_rib_edges, f)
        
        

    def init_keel(self):
        self.keel = Keel()
        return self.keel
    
    def sanitize_keel(self):
        self.keel.set_start(self.parent.keel.translation(self.parent_keels_position))

    def add_rib(self, position=0., edges=None):
        new_rib = Rib()
        new_rib.position = position
        new_rib.edges = edges
        self.ribs.append(new_rib)
    
    def set_smoothing(self, ship_smoothing_from, ship_smoothing_to=None):
        self.smoothing = True
        self.smoothing_from = ship_smoothing_from
        self.smoothing_to = ship_smoothing_to
    
    def set_smoothing_to(self, ship_smoothing_to):
        self.smoothing = True
        self.smoothing_to = ship_smoothing_to

    def get_rib_end(self, ship):
        rib_end = ship.ribs[-1]
        for rib in ship.ribs:
            if rib.position > rib_end.position:
                rib_end = rib
        return rib_end

    def get_rib_start(self, ship):
        rib_start = ship.ribs[0]
        for rib in ship.ribs:
            if rib.position < rib_start.position:
                rib_start = rib
        return rib_start

