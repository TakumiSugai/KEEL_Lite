from dataclasses import dataclass, field

import numpy as np

from .ship import Ship

from typing import List

@dataclass
class Dock:
    ships:List[Ship] = field(default_factory=list)

    def translate_matrix(self, x, y, z):
        return np.array([\
            [1., 0., 0., 0.],\
            [0., 1., 0., 0.],\
            [0., 0., 1., 0.],\
            [x, y, z, 1.]])

    def rotate_matrix_x(self, theta):
        return np.array([\
            [1., 0., 0., 0.],\
            [0., np.cos(theta), np.sin(theta), 0.],\
            [0., -np.sin(theta), np.cos(theta), 0.],\
            [0., 0., 0., 1.]])

    def rotate_matrix_y(self, theta):
        return np.array([\
            [np.cos(theta), 0., -np.sin(theta), 0.],\
            [0., 1., 0., 0.],\
            [np.sin(theta), 0., np.cos(theta), 0.],\
            [0., 0., 0., 1.]])

    def generate_ship(self):
        ship = Ship()

        self.ships.append(ship)
        ship.init_keel()
        return ship

    def rotate_keel(self, ship, y_axis_rotate=0., z_axis_rotate=0.):
        ship.keel.rotation(y_axis_rotate, z_axis_rotate)
        self.make_translation_dirty_recursively(ship)
    
    def resize_keel(self, ship, keel_length):
        ship.keel.length = keel_length
        self.make_translation_dirty_recursively(ship)
    
    def set_parent(self, ship ,parent, position=1.):
        ship.set_parent(parent, position)
        self.make_parents_dirty_recursively(ship)
        self.make_translation_dirty_recursively(ship)

    def set_parents_position(self, ship, position=1.):
        ship.set_parent(ship.parent, position)
        self.make_translation_dirty_recursively(ship)

    def make_parents_dirty_recursively(self, ship):
        for target_ship in self.ships:
            for parent in target_ship.parents:
                if ship is parent:
                    target_ship.parents_dirty_flag = True

    def make_translation_dirty_recursively(self, ship):
        for target_ship in self.ships:
            for parent in target_ship.parents:
                if ship is parent:
                    target_ship.transration_dirty_flag = True

    def sanitize_dock(self, force=False):
        for target_ship in reversed(self.ships):
            if force or target_ship.parents_dirty_flag:
                target_ship.get_parents()
        self.ships.sort(key=lambda ship: len(ship.parents))

        for target_ship in self.ships:
            if target_ship.parent != None and (force or target_ship.transration_dirty_flag):
                target_ship.sanitize_keel()

    def get_object_areas(self):
        right_max = 0.
        left_max = 0.
        top_max = 0.
        bottom_max = 0.
        front_max = 0.
        back_max = 0.
        for target_ship in self.ships:
            keel_translation = target_ship.keel.translation(1.)
            if (keel_translation[3][0] < 0.):
                if keel_translation[3][0] < left_max:
                    left_max = keel_translation[3][0]
            else:
                if keel_translation[3][0] > right_max:
                    right_max = keel_translation[3][0]

            if (keel_translation[3][1] < 0.):
                if keel_translation[3][1] < bottom_max:
                    bottom_max = keel_translation[3][1]
            else:
                if keel_translation[3][1] > top_max:
                    top_max = keel_translation[3][1]
            
            if (keel_translation[3][2] < 0.):
                if keel_translation[3][2] < back_max:
                    back_max = keel_translation[3][2]
            else:
                if keel_translation[3][2] > front_max:
                    front_max = keel_translation[3][2]
            
        return (right_max, left_max, top_max, bottom_max, front_max, back_max)

    def write_stl(self, f):
        self.sanitize_dock()
        if self.ships is None or len(self.ships) == 0:
            return
        for ship in self.ships:
            ship.write_stl(f)
