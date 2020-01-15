from keel_lite import Dock, Shipwright
import numpy as np
import os

sw = Shipwright(Dock())

base = sw.rotate(np.pi/2, 0.).void(0.)

rectangular = sw.parent(base).rectangular(2., 3., 4.)

sw.parent(rectangular).spin(\
    [(1., 1.), (1., 0.), (0., 0.), (0., 1.)], \
    1., 16)

# sw.generate_stl(".", "spin_object.stl")
sw.generate_stl("../../storage/shared/", "spin_object.stl")
