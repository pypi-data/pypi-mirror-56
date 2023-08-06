
import numpy as np
# from geo_functions import *
# from material import *

import uuid
import itertools
# from polygon_triangulation import polygon_triangulate
import triangle
# import matplotlib.pyplot as plt
# import gmsh
import trimesh
import pyclipper
import weakref
from shapely.geometry import Polygon as SPolygon

from PySimultan.config import use_class_extension as use_class_extension
from PySimultan.geo_functions import unit_normal, convert_to_global, convert_to_local, polygon_area_3d, collinear_check, calc_plane_equation, throw_exception
from PySimultan.material import Part as NewPart
from PySimultan.base_classes import GeoBaseClass
from PySimultan.vertice import Vertex
from PySimultan.edge import Edge
from PySimultan.edge_loop import EdgeLoop
from PySimultan.floor import Floor
from PySimultan import settings


class BaseFace(object):
    def __init__(self,
                 boundary,
                 holes,
                 orientation):

        self.boundary = boundary
        self.holes = holes
        self.orientation = orientation


class ExtendedFace(GeoBaseClass):

    new_face_id = itertools.count(0)
    visible_class_name = 'Face'

    def __init__(self,
                 face_id=None,
                 name=None,
                 layers=None,
                 is_visible=True,
                 boundary=None,
                 holes=None,
                 orientation=0,
                 color=None,
                 color_from_parent=False,
                 overwrite_calcable=True,
                 area=0,
                 triangulation=None,
                 part=None,
                 opening=False,
                 floor=None
                 ):

        self._Normal = None
        self._Points = None
        self._Coords = None
        self._Part = None
        self._Triangulation = None
        self._Holes = list()
        self._Boundary = list()
        self._BoundaryID = None
        self._LocalCoord = None
        self._G2L_TransMat = None
        self._Opening = False
        self._Closed = None
        self._Zones = None
        self._OverwriteCalcable = True
        self._Centroid = None
        self._PlaneEQ = None
        self._Floor = None
        self._HoleCount = None
        self._HoleIDs = None

        self._Mesh = []
        self._Circumference = None

        self._observers = []

        super().__init__(id=face_id,
                         pid=next(type(self).new_face_id),
                         color=color,
                         name=name,
                         color_from_parent=color_from_parent,
                         is_visible=is_visible,
                         layers=layers
                         )

        if boundary is None:
            self.Boundary = []
        elif type(boundary) == list:
            self.Boundary = boundary
        else:
            self.Boundary = [boundary]

        self.BoundaryID = self.Boundary[0].ID

        if holes is None:
            self.Holes = list()
        elif type(holes) == list:
            self.Holes = holes
        else:
            self.Holes = [holes]

        if self.Holes.__len__() > 0:
            self.HoleIDs = list(x.ID for x in self._Holes)
        else:
            self.HoleIDs = []

        self.HoleCount = self.Holes.__len__()

        if name is None:
            self.Name = 'face{}'.format(self._PID)
        else:
            self.Name = name

        if part is None:
            if not NewPart.get_instances():
                self.Part = NewPart()
            else:
                self.Part = NewPart.get_instances()[0]
        else:
            self.Part = part

        if floor is None:
            self.find_floor()
        elif type(floor) == list:
            self.Floor = floor
        else:
            self.Floor = [floor]

        self.IsVisible = is_visible
        self.Orientation = orientation
        self.Color = color
        self.ColorFromParent = color_from_parent
        self.OverwriteCalcable = overwrite_calcable        # the attributes which can be calculated for this face are overwritten
        self.Triangulation = triangulation

        self.Area = area
        self.Closed = []

        self.Opening = opening

        # -----------------------------------------------
        # bindings
        # -----------------------------------------------

        # for hole in self._Holes:
        #     hole.bind_to(self.hole_updated)

        # for boundary in self._Boundary:
        #     boundary.bind_to(self.boundary_updated)

        # self.Part.bind_to(self.part_updated)

        # -----------------------------------------------
        # initial face calculations
        # -----------------------------------------------

        self.recalculate_dependent_attributes()

        # if self._OverwriteCalcable:
        #     self.calc_normal()
        #     self.create_poly_points()
        #     self.create_poly_coordinates()
        #     self.calculate_area()
        #     self.convert_to_local_coord()
        #     self.calc_centroid()
        #     self.triangulate()
        #     self.create_mesh()

        # add to the collection
        settings.building_collection.Face_collection.append(self)

    # --------------------------------------------------------
    # specific attributes
    # --------------------------------------------------------

    @property
    def Boundary(self):
        return self._Boundary

    @Boundary.setter
    def Boundary(self, value):
        if not(isinstance(value, list)):
            if value is None:
                value = []
            else:
                value = [value]

        self._default_set_handling('Boundary', value, bind_method=self.boundary_updated)

    @property
    def Mesh(self):
        if self._Mesh is None:
            self.create_mesh()
        return self._Mesh

    @Mesh.setter
    def Mesh(self, value):
        self._default_set_handling('Mesh', value)

    @property
    def OverwriteCalcable(self):
        return self._OverwriteCalcable

    @OverwriteCalcable.setter
    def OverwriteCalcable(self, value):
        self._default_set_handling('OverwriteCalcable', value)

    @property
    def BoundaryID(self):
        return self._Boundary[0].ID

    @BoundaryID.setter
    def BoundaryID(self, value):
        self._default_set_handling('BoundaryID', value)

    @property
    def Holes(self):
        return self._Holes

    @Holes.setter
    def Holes(self, value):
        if isinstance(value, list):
            if value:
                if not(type(value) == list):
                    value = [value]
            else:
                value = []
        else:
            value = [value]

        self._default_set_handling('Holes', value, bind_method=self.hole_updated)

        self.HoleCount = self.Holes.__len__()

        if self.Holes.__len__() > 0:
            self.HoleIDs = list(x.ID for x in self.Holes)
        else:
            self.HoleIDs = []

        self.hole_updated()

    @property
    def HoleCount(self):
        return self._HoleCount

    @HoleCount.setter
    def HoleCount(self, value):
        self._default_set_handling('HoleCount', value)

    @property
    def HoleIDs(self):
        return self._HoleIDs

    @HoleIDs.setter
    def HoleIDs(self, value):
        self._default_set_handling('HoleIDs', value)

    @property
    def Orientation(self):
        return self._Orientation

    @Orientation.setter
    def Orientation(self, value):
        self._default_set_handling('Orientation', value)

    @property
    def Points(self):
        if self._Points is None:
            self.create_poly_points()
        return self._Points

    @Points.setter
    def Points(self, value):
        self._default_set_handling('Points', value)

    @property
    def Area(self):
        if self._Area is None:
            self.calculate_area()
        return self._Area

    @Area.setter
    def Area(self, value):
        self._default_set_handling('Area', value)

    @property
    def Normal(self):
        if self._Normal is None:
            self.calc_normal()
        return self._Normal

    @Normal.setter
    def Normal(self, value):
        self._default_set_handling('Normal', value)

    @property
    def Coords(self):
        if self._Coords is None:
            self.create_poly_coordinates()
        return self._Coords

    @Coords.setter
    def Coords(self, value):
        self._default_set_handling('Coords', value)

    @property
    def Closed(self):
        if self._Closed is None:
            self.check
        return self._Closed

    @Closed.setter
    def Closed(self, value):
        self._default_set_handling('Closed', value)

    @property
    def LocalCoord(self):
        if self._LocalCoord is None:
            self.convert_to_local_coord()
        return self._LocalCoord

    @LocalCoord.setter
    def LocalCoord(self, value):
        self._default_set_handling('LocalCoord', value)

    @property
    def G2L_TransMat(self):
        if self._G2L_TransMat is None:
            self.convert_to_local_coord()
        return self._G2L_TransMat

    @G2L_TransMat.setter
    def G2L_TransMat(self, value):
        self._default_set_handling('G2L_TransMat', value)

    @property
    def Triangulation(self):
        if self._Triangulation is None:
            self.triangulate()
        return self._Triangulation

    @Triangulation.setter
    def Triangulation(self, value):
        self._default_set_handling('Triangulation', value)

    @property
    def Part(self):
        if self._Part is None:
            if not NewPart.get_instances():
                self.Part = NewPart()
            else:
                self.Part = NewPart.get_instances()[0]
        return self._Part

    @Part.setter
    def Part(self, value):
        self._default_set_handling('Part', value, bind_method=self.part_updated)

    @property
    def Circumference(self):
        if self._Circumference is None:
            self.calc_circumference()
        return self._Circumference

    @Circumference.setter
    def Circumference(self, value):
        self._default_set_handling('Circumference', value)

    @property
    def Opening(self):
        return self._Opening

    @Opening.setter
    def Opening(self, value):
        self._default_set_handling('Opening', value)

    @property
    def Zones(self):
        if self._Zones is None:
            return list()
        else:
            zones_list = list(x() for x in self._Zones)
            return zones_list

    @Zones.setter
    def Zones(self, value):
        zones_list = list(weakref.ref(x) for x in value)
        self._default_set_handling('Zones', zones_list)

    @property
    def Centroid(self):
        if self._Centroid is None:
            self.calc_centroid()
        return self._Centroid

    @Centroid.setter
    def Centroid(self, value):
        self._default_set_handling('Centroid', value)

    @property
    def PlaneEQ(self):
        if self._PlaneEQ is None:
            self.calc_plane_equation()
        return self._PlaneEQ

    @PlaneEQ.setter
    def PlaneEQ(self, value):
        self._default_set_handling('PlaneEQ', value)

    @property
    def Floor(self):
        if self._Floor is None:
            self.find_floor()
        return self._Floor

    @Floor.setter
    def Floor(self, value):
        self._default_set_handling('Floor', value)

    # --------------------------------------------------------
    # observed object change callbacks
    # --------------------------------------------------------

    def hole_updated(self, **kwargs):
        for key, value in kwargs.items():
            # self.print_status("{0} = {1}".format(key, value))
            if value == 'vertex_position_changed':
                if self._OverwriteCalcable:
                    self.recalculate_dependent_attributes()
                for callback in self._observers:
                    instance = callback.__self__
                    instance._UpdateHandler.add_notification(callback, 'vertex_position_changed')

    def boundary_updated(self, **kwargs):
        for key, value in kwargs.items():
            # self.print_status("{0} = {1}".format(key, value))
            if value == 'vertex_position_changed':
                if self._OverwriteCalcable:
                    self.recalculate_dependent_attributes()
                for callback in self._observers:
                    instance = callback.__self__
                    instance._UpdateHandler.add_notification(callback, 'vertex_position_changed')

    def part_updated(self):
        # print('Part updated')
        pass

    # --------------------------------------------------------
    # class methods
    # --------------------------------------------------------

    def create_poly_points(self):

        if self.Boundary:

            points = list()

            points.append(self.Boundary[0].Edges[0].Vertex1)
            points.append(self.Boundary[0].Edges[0].Vertex2)

            for i in range(1, self._Boundary[0].EdgeCount):
                if points[-1] == self.Boundary[0].Edges[i].Vertex1:
                    points.append(self.Boundary[0].Edges[i].Vertex2)
                elif points[-1] == self.Boundary[0].Edges[i].Vertex2:
                    points.append(self.Boundary[0].Edges[i].Vertex1)
                else:
                    self.print_status('start of the edge is not the end of the previous edge')

            # check if polygon is closed
            if points[-1] == points[0]:
                self.Closed = True
            else:
                self.Closed = False

            self.Points = points

    def calc_normal(self):

        if self.Points.__len__() > 2:
            # other method
            a = np.array(self._Points[0].Position)
            b = np.array(self._Points[1].Position)
            c = np.array(self._Points[2].Position)

            self.Normal = unit_normal(a, b, c)
        else:
            self.Normal = []

    def create_poly_coordinates(self):

        if self.Points is not None:
            self._Coords = np.zeros((self.Points.__len__()-1, 3))
            for i in range(self.Points.__len__() - 1):
                self._Coords[i, :] = self.Points[i].Position

            self.Coords = self._Coords

    def convert_to_local_coord(self, *args):

        try:
            self.LocalCoord, self.G2L_TransMat = convert_to_local(self.Coords)
        except Exception as e:
            throw_exception(e, message='Face: {Name} with ID: {ID}: \n Could not convert face to local coordinates. '
                                       '\nThe face seems to be not planar. \nError: '.format(Name=self.Name,
                                                                                                    ID=self.ID))
            self.LocalCoord = None
            self.G2L_TransMat = None
            return


        if args:
            points = args
            local_coords = np.zeros((len(points), 2))
            local_coords[:, 0] = np.dot((points - self.G2L_TransMat.loc0), self.G2L_TransMat.locx)
            local_coords[:, 1] = np.dot((points - self.G2L_TransMat.loc0), self.G2L_TransMat.locy)
            return local_coords
        else:
            return self.LocalCoord, self.G2L_TransMat

    def convert_to_global_coord(self, *args):
        if args:
            points = args[0]
            return convert_to_global(self.G2L_TransMat.transformation_mat, points)
        else:
            return convert_to_global(self.G2L_TransMat.transformation_mat, self.LocalCoord)

    def calculate_area(self):

        area = polygon_area_3d(self.Coords)

        # subtract holes area:
        hole_area = 0
        if any(self.Holes):
            for hole in self.Holes:
                hole_area += hole.Area
            self.Area = area - hole_area
        else:
            self.Area = area

    def triangulate(self):

        segments = []
        for i in range(len(self.Points) - 2):
            segments.append([int(i), int(i + 1)])
        segments.append([int(i + 1), int(0)])

        # handle holes
        if self.HoleCount > 0:
            local_coord = self.LocalCoord
            holes_point = np.empty(0)
            for hole in self.Holes:
                initial_number_of_nodes = local_coord.shape[0]
                hole_local_ccord = self._G2L_TransMat.transform(hole.Coords)
                local_coord = np.vstack((local_coord, hole_local_ccord))
                for i in range(len(hole.Points) - 2):
                    segments.append([int(i+initial_number_of_nodes), int(i + 1 + initial_number_of_nodes)])
                segments.append([int(i + 1 + initial_number_of_nodes), int(0 + initial_number_of_nodes)])

                # create points inside the hole; these points are the centre of gravity of the triangulated hole:
                # https://de.wikipedia.org/wiki/Geometrischer_Schwerpunkt#Dreieck

                for j in range(hole.Triangulation['triangles'].shape[0]):
                    s = np.array(
                        (1/3 * np.sum(hole_local_ccord[hole.Triangulation['triangles'][j, :], 0]),
                         1/3 * np.sum(hole_local_ccord[hole.Triangulation['triangles'][j, :], 1])
                         )
                    )
                    if holes_point.shape[0] == 0:
                        holes_point = s
                    else:
                        holes_point = np.vstack((holes_point, s))

            a = {'vertices': local_coord, 'segments': segments, 'holes': holes_point}

            # add a vertex, which lies inside the hole:

        else:
            a = {'vertices': self.LocalCoord, 'segments': segments}

        triangulation = triangle.triangulate(a, 'p')
        # triangle.compare(plt, dict(vertices=self._LocalCoord), triangulation)
        triangulation['vertices3D'] = convert_to_global(self.G2L_TransMat.transformation_mat, triangulation['vertices'])

        # plt.show()
        self.Triangulation = triangulation

    def calc_circumference(self):
        if type(self.Boundary) == list:
            self._Circumference = self.Boundary[0].Length
        else:
            self._Circumference = self.Boundary.Length

    def create_mesh(self):
        self.Mesh = trimesh.Trimesh(vertices=self.Triangulation['vertices3D'],
                                    faces=self.Triangulation['triangles']
                                    )

    def create_offset_face(self, offset, name=None):

        # from face import Face

        # https://github.com/fonttools/pyclipper
        if self.HoleCount > 0:
            raise ValueError('Polygon offsetting for polygons with hole not possible')

        # 1 check if offset is integer. If not calculate scaling factor so that it is an integer:
        # : see: https://pypi.org/project/pyclipper/: The Clipper library uses integers
        # instead of floating point values to preserve numerical robustness. If you need to scale coordinates of your
        # polygons, this library provides helper functions scale_to_clipper() and scale_from_clipper() to achieve that.

        # if offset.is_integer():
        #     scale_factor = 1
        # else:
            # scale_factor = 1
            # while not(offset.is_integer()):
            #     scale_factor = scale_factor * 10
            #     offset = offset * scale_factor
        scale_factor = 100000
        offset = offset * scale_factor

        # 2 take local coordinates and scale:
        # print('\n Coords: \n', np.round(self.Coords, 5))
        # print('\n Local Coords: \n', np.round(self.LocalCoord, 5))

        local_coord = tuple(map(tuple, self.LocalCoord * scale_factor))

        # 3 create pyclipper object:
        pco = pyclipper.PyclipperOffset()
        pco.AddPath(local_coord, pyclipper.JT_ROUND, pyclipper.ET_CLOSEDPOLYGON)

        # 3 create offset:
        solution = pco.Execute(offset)

        # 4 convert coordinates back to global coordinates and scale back
        offset_coords = self.convert_to_global_coord(np.asarray(solution).squeeze() / scale_factor)

        # print('\n Local Offset Coord: \n', np.round(np.asarray(solution).squeeze() / scale_factor, 5))
        # print('\n Offset Coord: \n', np.round(offset_coords, 5))

        # self.print_status(offset_coords)

        # create vertices
        vertices = list()
        for position in offset_coords:
            vertices.append(Vertex(layers=self.Layers,
                                   is_visible=True,
                                   position=position,
                                   color_from_parent=False))

        # create edges
        edges = list()
        for index in range(vertices.__len__() - 1):
            edges.append(Edge(vertex_1=vertices[index],
                              vertex_2=vertices[index+1])
                         )
        edges.append(Edge(vertex_1=vertices[-1],
                          vertex_2=vertices[0])
                     )

        # create edge loop:
        edge_loop = EdgeLoop(edges=edges)

        # create face:
        face = Face(boundary=edge_loop,
                    orientation=self.Orientation,
                    name=name)

        print('Face Area: {area} m²'.format(area=self.Area))
        print('Offset Area: {area} m²'.format(area=face.Area))

        return face

    def check_closed(self):

        edges = self.Boundary[0].Edges

        if (edges[0].Vertex1 == edges[-1].Vertex1) or \
           (edges[0].Vertex1 == edges[-1].Vertex2) or \
           (edges[0].Vertex2 == edges[-1].Vertex1) or \
           (edges[0].Vertex2 == edges[-1].Vertex2):
            self.Closed = True
        else:
            self.Closed = False

    def calc_centroid(self):
        # https://stackoverflow.com/questions/53502002/how-to-calculate-the-center-of-gravity-with-shapely-in-python
        SPolygon()
        local_centroid = list(SPolygon(self.LocalCoord).centroid.coords)
        self.Centroid = np.squeeze(self.convert_to_global_coord(np.array(local_centroid)))

    def reprJSON(self):
        return dict(ID=self._ID,
                    PID=self._PID,
                    Name=self._Name,
                    IsVisible=self._IsVisible,
                    Color=self._Color,
                    ColorFromParent=self.ColorFromParent,
                    Boundary=self._Boundary,
                    BoundaryID=self._BoundaryID,
                    Holes=self._Holes,
                    HoleIDs=self._HoleIDs,
                    HoleCount=self._HoleCount,
                    Orientation=self._Orientation,
                    Points=self._Points,
                    Area=self._Area,
                    Normal=self._Normal,
                    Coords=self._Coords,
                    Closed=self._Closed,
                    LocalCoord=self._LocalCoord,
                    Triangulation=self.Triangulation)

    def calc_plane_equation(self):

        indx = np.array((0, 1, 2))
        pts = self.Coords[indx, :]
        pts_collinear = collinear_check(p0=pts[0, :], p1=pts[1, :], p2=pts[2, :])

        if pts_collinear:
            i = 1

            while pts_collinear:
                indx = np.array((i, i+1, i+2))
                indx[indx > self.Coords.__len__()] = indx[indx > self.Coords.__len__()] - self.Coords.__len__()
                pts = self.Coords[indx, :]
                pts_collinear = collinear_check(p0=pts[0, :], p1=pts[1, :], p2=pts[2, :])

        self.PlaneEQ = calc_plane_equation(pts)

    def recalculate_dependent_attributes(self):

        if self.OverwriteCalcable:
            self._Normal = None
            self._Points = None
            self._Coords = None
            self._Triangulation = None
            self._BoundaryID = None
            self._LocalCoord = None
            self._G2L_TransMat = None
            self._Closed = None
            self._Mesh = []
            self._Circumference = None
            self._Centroid = None
            self._PlaneEQ = None

            self.calc_normal()
            self.create_poly_points()
            self.create_poly_coordinates()
            self.calc_circumference()
            self.calculate_area()
            self.convert_to_local_coord()
            self.calc_centroid()
            self.calc_plane_equation()
            self.triangulate()
            self.create_mesh()

    def find_floor(self):
        if not Floor.get_instances():
            self._Floor = [Floor(floor_height=0)]

        existing_floors = Floor.get_instances()
        floors = []
        min_z = min(self.Coords[:, 2])
        max_z = max(self.Coords[:, 2])

        for existing_floor in existing_floors:
            min_floor_height = existing_floor.FloorHeight
            max_floor_height = existing_floor.FloorHeight + existing_floor.StoreyHeight
            # if np.any((self.Coords[:, 2]) >= min_floor_height) and np.any(self.Coords[:, 2] <= (max_floor_height)):
            if (min_z <= min_floor_height + 1e-4) and (max_z >= max_floor_height - 1e-4):
                floors.append(existing_floor)
            elif np.any(self.Coords[:, 2] < min_floor_height) and np.any(self.Coords[:, 2] > max_floor_height):
                floors.append(existing_floor)
            elif np.any(self.Coords[:, 2] >= min_floor_height) and np.any(self.Coords[:, 2] <= max_floor_height):
                floors.append(existing_floor)
        if not floors:
            self._Floor = [Floor(floor_height=min(self.Coords[:, 2]))]

    def floor_changed(self):
        pass


if use_class_extension:
    class Face(ExtendedFace, BaseFace):
        pass
else:
    Face = BaseFace


if __name__ == '__main__':

    pass









