import numpy as np
import itertools

import uuid

# user defined imports:
from PySimultan.base_classes import ObjectBaseClass
from PySimultan import settings

class Position(ObjectBaseClass):

    visible_class_name = 'Position'
    new_vertex_id = itertools.count()

