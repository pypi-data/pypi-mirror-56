
# python packages import:
import numpy as np
import itertools
import uuid

# user defined imports:
from PySimultan.config import use_class_extension as use_class_extension
from PySimultan.base_classes import GeoBaseClass
from PySimultan import settings


class BaseVertex(object):

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


class ExtendedVertex(GeoBaseClass):

    visible_class_name = 'Vertex'
    new_vertex_id = itertools.count()

    def __init__(self,
                 vertex_id=None,
                 layers=None,
                 name=None,
                 is_visible=True,
                 position=np.array((0, 0, 0)),
                 color=np.append(np.random.rand(1, 3), 0)*255,
                 color_from_parent=False
                 ):

        super().__init__(id=vertex_id,
                         pid=next(self.new_vertex_id),
                         color=color,
                         name=name,
                         color_from_parent=color_from_parent,
                         is_visible=is_visible,
                         layers=layers
                         )

        self._x = None
        self._y = None
        self._z = None

        self._x = position[0]
        self._y = position[1]

        if position.shape[0] == 3:
            self._z = position[2]

        self._Position = position

        # name
        if name is None:
            self._Name = 'Vertex{}'.format(self._PID)
        else:
            self._Name = name

        # add to the collection
        settings.building_collection.Vertex_collection.append(self)

        # -----------------------------------------------
        # bindings

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, value):
        self._z = value

    @property
    def Position(self):
        if self._z is None:
            return np.array([self._x, self._y])
        else:
            return np.array([self._x, self._y, self._z])

    @Position.setter
    def Position(self, value):
        self._default_set_handling('Position', value)
        self.x = value[0]
        self.y = value[1]
        if value.shape == 3:
            self.z = value[2]

    def layer_updated(self, **kwargs):
        self.print_status('layer has updated')
        for key, value in kwargs.items():
            self.print_status("{0} = {1}".format(key, value))

    def reprJSON(self):
        return dict(ID=self._ID,
                    PID=self._PID,
                    Name=self._Name,
                    IsVisible=self._IsVisible,
                    Color=self._Color,
                    ColorFromParent=self.ColorFromParent,
                    Position=self._Position)


if use_class_extension:
    class Vertex(ExtendedVertex, BaseVertex):
        pass
else:
    Vertex = BaseVertex
