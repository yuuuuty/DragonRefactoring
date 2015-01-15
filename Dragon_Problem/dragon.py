#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import urllib

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

TRACE = True
DEBUG = False


class OpenGLProjection(object):

    """OpenGLプロジェクション。"""

    def __init__(self):
        """OpenGLプロジェクションのコンストラクタ。"""
        if TRACE: print __name__, self.__init__.__doc__

        self._eye_point = self._default_eye_point = None
        self._sight_point = self._default_sight_point = None
        self._up_vector = self._default_up_vector = None
        self._fovy = self._default_fovy = None
        self._near = self._default_near = None
        self._far = self._default_far = None

        return

    def eye_point(self):
        """視点を応答する。"""
        if TRACE: print __name__, self.eye_point.__doc__

        if self._eye_point == None: self.eye_point_([0.0, 0.0, 10.0])
        return self._eye_point

    def eye_point_(self, a_point):
        """視点を設定する。"""
        if TRACE: print __name__, self.eye_point_.__doc__

        self._eye_point = a_point
        if self._default_eye_point == None: self._default_eye_point = a_point

        return

    def sight_point(self):
        """注視点を応答する。"""
        if TRACE: print __name__, self.sight_point.__doc__

        if self._sight_point == None: self.sight_point_([0.0, 0.0, 0.0])
        return self._sight_point

    def sight_point_(self, a_point):
        """注視点を設定する。"""
        if TRACE: print __name__, self.sight_point_.__doc__

        self._sight_point = a_point
        if self._default_sight_point == None:
            self._default_sight_point = a_point

        return

    def up_vector(self):
        """上方向ベクトルを応答する。"""
        if TRACE: print __name__, self.up_vector.__doc__

        if self._up_vector == None: self.up_vector_([0.0, 1.0, 0.0])
        return self._up_vector

    def up_vector_(self, a_point):
        """上方向ベクトルを設定する。"""
        if TRACE: print __name__, self.up_vector_.__doc__

        self._up_vector = a_point
        if self._default_up_vector == None: self._default_up_vector = a_point

        return

    def fovy(self):
        """視界角を応答する。"""
        if TRACE: print __name__, self.fovy.__doc__

        if self._fovy == None: self.fovy_(30.0)
        return self._fovy

    def fovy_(self, a_float):
        """視界角を設定する。"""
        if TRACE: print __name__, self.fovy_.__doc__

        self._fovy = a_float
        if self._default_fovy == None: self._default_fovy = a_float

        return

    def near(self):
        """近を応答する。"""
        if TRACE: print __name__, self.near.__doc__

        if self._near == None: self.near_(0.01)
        return self._near

    def near_(self, a_float):
        """近を設定する。"""
        if TRACE: print __name__, self.near_.__doc__

        self._near = a_float
        if self._default_near == None: self._default_near = a_float

        return

    def far(self):
        """遠を応答する。"""
        if TRACE: print __name__, self.far.__doc__

        if self._far == None: self.far_(100)
        return self._far

    def far_(self, a_float):
        """遠を設定する。"""
        if TRACE: print __name__, self.far_.__doc__

        self._far = a_float
        if self._default_far == None: self._default_far = a_float

        return

    def reset(self):
        """プロジェクション情報をデフォルト(最初に設定されたパラメータ)に設定し直す。"""
        if TRACE: print __name__, self.reset.__doc__

        if self._default_eye_point != None:
            self._eye_point = self._default_eye_point

        if self._default_fovy != None:
            self._fovy = self._default_fovy

        return


class OpenGLModel(object):

    """OpenGLモデル。"""

    def __init__(self):
        """OpenGLモデルのコンストラクタ。"""
        if TRACE: print __name__, self.__init__.__doc__

        self._display_object = []
        self._projection = OpenGLProjection()
        self._display_list = None
        self._view = None
        self._axes_scale = 1.0

        return

    def default_controllerew_class(self):
        """OpenGLモデルを表示するデフォルトのビューのクラスを応答する。"""
        if TRACE: print __name__, self.default_controllerew_class.__doc__

        return OpenGLController

    def default_view_class(self):
        """OpenGLモデルを表示するデフォルトのビューのクラスを応答する。"""
        if TRACE: print __name__, self.default_view_class.__doc__

        return OpenGLView

    def default_window_title(self):
        """OpenGLウィンドウのタイトル(ラベル)を応答する。"""
        if TRACE: print __name__, self.default_window_title.__doc__

        return "Untitled"

    def display_list(self):
        """OpenGLモデルのディスプレイリスト(表示物をコンパイルしたOpenGLコマンド列)を応答する。"""
        if TRACE: print __name__, self.display_list.__doc__

        if self._display_list == None:
            self._display_list = glGenLists(1)
            glNewList(self._display_list, GL_COMPILE)
            glColor4d(0.5, 0.5, 1.0, 1.0)
            for index, each in enumerate(self._display_object):
                if DEBUG: print index,
                each.rendering()
            glEndList()

        return self._display_list

    def open(self):
        """OpenGLモデルを描画するためのOpenGLのウィンドウを開く。"""
        if TRACE: print __name__, self.open.__doc__

        view_class = self.default_view_class()
        self._view = view_class(self)

        return

    def rendering(self):
        """OpenGLモデルをレンダリングする。"""
        if TRACE: print __name__, self.rendering.__doc__

        glCallList(self.display_list())

        return


class OpenGLView(object):

    """OpenGLビュー。"""

    window_postion = [100, 100]

    @classmethod
    def get_window_postion(a_class):
        """ウィンドウを開くための位置を応答する。"""
        if TRACE: print __name__, a_class.get_window_postion.__doc__

        current_position = a_class.window_postion
        a_class.window_postion = map(
            (lambda value: value + 30), a_class.window_postion)

        return current_position

    def __init__(self, a_model):
        """OpenGLビューのコンストラクタ。"""
        if TRACE: print __name__, self.__init__.__doc__

        self._model = a_model
        controller_class = self._model.default_controllerew_class()
        self._controller = controller_class(self)
        self._angle_x = 0.0
        self._angle_y = 0.0
        self._angle_z = 0.0
        self._width = 400
        self._height = 400

        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
        glutInitWindowPosition(*OpenGLView.get_window_postion())
        glutInitWindowSize(self._width, self._height)
        glutCreateWindow(self._model.default_window_title())

        glutDisplayFunc(self.display)
        glutReshapeFunc(self.reshape)
        glutKeyboardFunc(self._controller.keyboard)
        glutMouseFunc(self._controller.mouse)
        glutMotionFunc(self._controller.motion)
        glutWMCloseFunc(self._controller.close)

        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_DEPTH_TEST)
        glDisable(GL_CULL_FACE)
        glEnable(GL_NORMALIZE)

        return

    def display(self):
        """OpenGLで描画する。"""
        if TRACE: print __name__, self.display.__doc__

        projection = self._model._projection
        eye_point = projection.eye_point()
        sight_point = projection.sight_point()
        up_vector = projection.up_vector()
        fovy = projection.fovy()
        near = projection.near()
        far = projection.far()

        aspect = float(self._width) / float(self._height)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(fovy, aspect, near, far)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(eye_point[0], eye_point[1], eye_point[2],
                  sight_point[0], sight_point[1], sight_point[2],
                  up_vector[0], up_vector[1], up_vector[2])

        glClearColor(1.0, 1.0, 1.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glEnable(GL_LIGHTING)
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.5, 0.5, 0.5, 1.0])
        glLightModelf(GL_LIGHT_MODEL_LOCAL_VIEWER, 0.0)
        glLightModelf(GL_LIGHT_MODEL_TWO_SIDE, 1.0)
        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_POSITION, [0.0, 0.0, 1.0, 0.0])
        glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, [0.0, 0.0, -1.0])
        glLightfv(GL_LIGHT0, GL_SPOT_CUTOFF, 90.0)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.5, 0.5, 0.5, 1.0])
        glLightfv(GL_LIGHT0, GL_SPECULAR, [0.5, 0.5, 0.5, 1.0])
        glLightfv(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.0)
        glLightfv(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, 0.0)
        glLightfv(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 1.0)

        self.display_axes()

        glRotated(self._angle_x, 1.0, 0.0, 0.0)
        glRotated(self._angle_y, 0.0, 1.0, 0.0)
        glRotated(self._angle_z, 0.0, 0.0, 1.0)

        self._model.rendering()

        glutSwapBuffers()

        return

    def display_axes(self):
        """世界座標系を描画する。"""
        if TRACE: print __name__, self.display_axes.__doc__

        axes_scale = self._model._axes_scale
        scaled_by_n = (
            lambda vertex: map((lambda value: value * axes_scale), vertex))
        glBegin(GL_LINES)
        glColor([1.0, 0.0, 0.0, 1.0])
        glVertex(scaled_by_n([-1.00, 0.0, 0.0]))
        glVertex(scaled_by_n([1.68, 0.0, 0.0]))
        glColor([0.0, 1.0, 0.0, 1.0])
        glVertex(scaled_by_n([0.0, -1.00, 0.0]))
        glVertex(scaled_by_n([0.0, 1.68, 0.0]))
        glColor([0.0, 0.0, 1.0, 1.0])
        glVertex(scaled_by_n([0.0, 0.0, -1.00]))
        glVertex(scaled_by_n([0.0, 0.0, 1.68]))
        glEnd()

        return

    def reshape(self, width, height):
        """OpenGLを再形成する。"""
        if TRACE: print __name__, self.reshape.__doc__

        self._width = width
        self._height = height

        glViewport(0, 0, width, height)

        return


class OpenGLController(object):

    """OpenGLコントローラ。"""

    def __init__(self, a_view):
        """OpenGLコントローラのコンストラクタ。"""
        if TRACE: print __name__, self.__init__.__doc__

        self._model = a_view._model
        self._view = a_view

        return

    def close(self):
        """ウィンドウを閉じる際の処理をする。"""
        if TRACE: print __name__, self.close.__doc__

        sys.exit(0)

        return

    def keyboard(self, key, x, y):
        """キーボードを処理する。"""
        if TRACE: print __name__, self.keyboard.__doc__

        view = self._view
        projection = self._model._projection

        if key in "qQ\33":
            sys.exit(0)
        if key == 'r' or key == 'R':
            view._angle_x = 0.0
            view._angle_y = 0.0
            view._angle_z = 0.0
            projection.reset()
        if key == 'x':
            view._angle_x += 1.0
        if key == 'y':
            view._angle_y += 1.0
        if key == 'z':
            view._angle_z += 1.0
        if key == 'X':
            view._angle_x -= 1.0
        if key == 'Y':
            view._angle_y -= 1.0
        if key == 'Z':
            view._angle_z -= 1.0
        if key == 's':
            projection.fovy_(projection.fovy() + 1.0)
        if key == 'S':
            projection.fovy_(projection.fovy() - 1.0)

        self._view.display()  # glutPostRedisplay()

        return

    def motion(self, x, y):
        """マウスボタンを押下しながらの移動を処理する。"""
        if TRACE: print __name__, self.motion.__doc__

        print "motion at (" + str(x) + ", " + str(y) + ")"

        return

    def mouse(self, button, state, x, y):
        """マウスボタンを処理する。"""
        if TRACE: print __name__, self.mouse.__doc__

        if button == GLUT_LEFT_BUTTON:
            print "left",
        elif button == GLUT_MIDDLE_BUTTON:
            print "middle"
        elif button == GLUT_RIGHT_BUTTON:
            print "right",
        else:
            pass

        print "button is",

        if state == GLUT_DOWN:
            print "down",
        elif state == GLUT_UP:
            print "up",
        else:
            pass

        print "at (" + str(x) + ", " + str(y) + ")"

        return


class OpenGLObject(object):

    """OpenGLオブジェクト。"""

    def __init__(self):
        """OpenGLオブジェクトのコンストラクタ。"""
        if DEBUG: print __name__, self.__init__.__doc__

        self._rgb = [1.0, 1.0, 1.0]

        return

    def rendering(self):
        """OpenGLオブジェクトをレンダリングする。"""
        if DEBUG: print __name__, self.rendering.__doc__

        glColor4d(self._rgb[0], self._rgb[1], self._rgb[2], 1.0)

        return

    def rgb(self, red, green, blue):
        """OpenGLオブジェクトの色を設定する。"""
        if DEBUG: print __name__, self.rgb.__doc__

        self._rgb = [red, green, blue]

        return


class OpenGLTriangle(OpenGLObject):

    """OpenGL三角形。"""

    def __init__(self, vertex1, vertex2, vertex3):
        """OpenGL三角形のコンストラクタ。"""
        if DEBUG: print __name__, self.__init__.__doc__

        super(OpenGLTriangle, self).__init__()
        self._vertex1 = vertex1
        self._vertex2 = vertex2
        self._vertex3 = vertex3

        ux, uy, uz = map(
            (lambda value1, value0: value1 - value0), vertex2, vertex1)
        vx, vy, vz = map(
            (lambda value1, value0: value1 - value0), vertex3, vertex1)
        normal_vector = [
            (uy * vz - uz * vy), (uz * vx - ux * vz), (ux * vy - uy * vx)]
        distance = sum(
            map((lambda value: value * value), normal_vector)) ** 0.5
        self._normal_unit_vector = map(
            (lambda vector: vector / distance), normal_vector)

        return

    def rendering(self):
        """OpenGL三角形をレンダリングする。"""
        if DEBUG: print __name__, self.rendering.__doc__

        super(OpenGLTriangle, self).rendering()
        glBegin(GL_TRIANGLES)
        glNormal3fv(self._normal_unit_vector)
        glVertex3fv(self._vertex1)
        glVertex3fv(self._vertex2)
        glVertex3fv(self._vertex3)
        glEnd()

        return


class OpenGLPolygon(OpenGLObject):

    """OpenGL多角形。"""

    def __init__(self, vertexes):
        """OpenGL多角形のコンストラクタ。"""
        if DEBUG: print __name__, self.__init__.__doc__

        super(OpenGLPolygon, self).__init__()
        self._vertexes = vertexes

        x = 0.0
        y = 0.0
        z = 0.0
        length = len(vertexes)
        for i in range(0, length):
            j = (i + 1) % length
            k = (i + 2) % length
            ux, uy, uz = map(
                (lambda each1, each2: each1 - each2), vertexes[j], vertexes[i])
            vx, vy, vz = map(
                (lambda each1, each2: each1 - each2), vertexes[k], vertexes[j])
            x = x + (uy * vz - uz * vy)
            y = y + (uz * vx - ux * vz)
            z = z + (ux * vy - uy * vx)
        normal_vector = [x, y, z]
        distance = sum(map((lambda each: each * each), normal_vector)) ** 0.5
        self._normal_unit_vector = map(
            (lambda vector: vector / distance), normal_vector)

        return

    def rendering(self):
        """OpenGL多角形をレンダリングする。"""
        if DEBUG: print __name__, self.rendering.__doc__

        super(OpenGLPolygon, self).rendering()
        glBegin(GL_POLYGON)
        glNormal3fv(self._normal_unit_vector)
        for vertex in self._vertexes:
            glVertex3fv(vertex)
        glEnd()

        return


class DragonModel(OpenGLModel):

    """ドラゴンのモデル。"""

    def __init__(self):
        """ドラゴンのモデルのコンストラクタ。"""
        if TRACE: print __name__, self.__init__.__doc__

        super(DragonModel, self).__init__()
        self._projection.eye_point_(
            [-5.5852450791872, 3.07847342734, 15.794105252496])
        self._projection.sight_point_(
            [0.27455347776413, 0.20096999406815, -0.11261999607086])
        self._projection.up_vector_(
            [0.1018574904194, 0.98480906061847, -0.14062775604137])
        self._projection.fovy_(12.642721790235)

        filename = os.path.join(os.getcwd(), 'textdragon.txt')
        if os.path.exists(filename) and os.path.isfile(filename):
            pass
        else:
            url = 'http://www.cc.kyoto-su.ac.jp/~atsushi/Programs/Dragon/dragon.txt'
            urllib.urlretrieve(url, filename)

        with open(filename, "rU") as a_file:
            while True:
                a_string = a_file.readline()
                if len(a_string) == 0: break
                a_list = a_string.split()
                if len(a_list) == 0: continue
                first_string = a_list[0]
                if first_string == "number_of_vertexes":
                    number_of_vertexes = int(a_list[1])
                if first_string == "number_of_triangles":
                    number_of_triangles = int(a_list[1])
                if first_string == "end_header":
                    get_tokens = (lambda file: file.readline().split())
                    collection_of_vertexes = []
                    for n_th in range(number_of_vertexes):
                        a_list = get_tokens(a_file)
                        a_vertex = map(float, a_list[0:3])
                        collection_of_vertexes.append(a_vertex)
                    index_to_vertex = (
                        lambda index: collection_of_vertexes[index - 1])
                    for n_th in range(number_of_triangles):
                        a_list = get_tokens(a_file)
                        indexes = map(int, a_list[0:3])
                        vertexes = map(index_to_vertex, indexes)
                        a_tringle = OpenGLTriangle(*vertexes)
                        a_tringle.rgb(0.5, 0.5, 1.0)
                        self._display_object.append(a_tringle)

        return

    def default_window_title(self):
        """ドラゴンのウィンドウのタイトル(ラベル)を応答する。"""
        if TRACE: print __name__, self.default_window_title.__doc__

        return "Dragon"


class WaspModel(OpenGLModel):

    """スズメバチのモデル。"""

    def __init__(self):
        """スズメバチのモデルのコンストラクタ。"""
        if TRACE: print __name__, self.__init__.__doc__

        super(WaspModel, self).__init__()
        self._projection.eye_point_(
            [-5.5852450791872, 3.07847342734, 15.794105252496])
        self._projection.sight_point_(
            [0.19825005531311, 1.8530999422073, -0.63795006275177])
        self._projection.up_vector_(
            [0.070077999093727, 0.99630606032682, -0.049631725731267])
        self._projection.fovy_(41.480099231656)
        self._axes_scale = 4.0

        filename = os.path.join(os.getcwd(), 'text/wasp.txt')
        if os.path.exists(filename) and os.path.isfile(filename):
            pass
        else:
            url = 'http://www.cc.kyoto-su.ac.jp/~atsushi/Programs/Wasp/wasp.txt'
            urllib.urlretrieve(url, filename)

        with open(filename, "rU") as a_file:
            while True:
                a_string = a_file.readline()
                if len(a_string) == 0: break
                a_list = a_string.split()
                if len(a_list) == 0: continue
                first_string = a_list[0]
                if first_string == "number_of_vertexes":
                    number_of_vertexes = int(a_list[1])
                if first_string == "number_of_polygons":
                    number_of_polygons = int(a_list[1])
                if first_string == "end_header":
                    get_tokens = (lambda file: file.readline().split())
                    collection_of_vertexes = []
                    for n_th in range(number_of_vertexes):
                        a_list = get_tokens(a_file)
                        a_vertex = map(float, a_list[0:3])
                        collection_of_vertexes.append(a_vertex)
                    index_to_vertex = (
                        lambda index: collection_of_vertexes[index - 1])
                    for n_th in range(number_of_polygons):
                        a_list = get_tokens(a_file)
                        number_of_indexes = int(a_list[0])
                        index = number_of_indexes + 1
                        indexes = map(int, a_list[1:index])
                        vertexes = map(index_to_vertex, indexes)
                        rgb_color = map(float, a_list[index:index + 3])
                        a_polygon = OpenGLPolygon(vertexes)
                        a_polygon.rgb(*rgb_color)
                        self._display_object.append(a_polygon)

        return

    def default_window_title(self):
        """スズメバチのウィンドウのタイトル(ラベル)を応答する。"""
        if TRACE: print __name__, self.default_window_title.__doc__

        return "Wasp"


class BunnyModel(OpenGLModel):

    """うさぎのモデル。"""

    def __init__(self):
        """うさぎのモデルのコンストラクタ。"""
        if TRACE: print __name__, self.__init__.__doc__

        super(BunnyModel, self).__init__()
        self._axes_scale = 0.1

        filename = os.path.join(os.getcwd(), 'text/bunny.ply')
        if os.path.exists(filename) and os.path.isfile(filename):
            pass
        else:
            url = 'http://www.cc.kyoto-su.ac.jp/~atsushi/Programs/Bunny/bunny.ply'
            urllib.urlretrieve(url, filename)

        with open(filename, "rU") as a_file:
            while True:
                a_string = a_file.readline()
                if len(a_string) == 0: break
                a_list = a_string.split()
                if len(a_list) == 0: continue
                first_string = a_list[0]
                if first_string == "element":
                    second_string = a_list[1]
                    if second_string == "vertex":
                        number_of_vertexes = int(a_list[2])
                    if second_string == "face":
                        number_of_faces = int(a_list[2])
                if first_string == "end_header":
                    get_tokens = (lambda file: file.readline().split())
                    collection_of_vertexes = []
                    for n_th in range(number_of_vertexes):
                        a_list = get_tokens(a_file)
                        a_vertex = map(float, a_list[0:3])
                        collection_of_vertexes.append(a_vertex)
                    index_to_vertex = (
                        lambda index: collection_of_vertexes[index])
                    for n_th in range(number_of_faces):
                        a_list = get_tokens(a_file)
                        indexes = map(int, a_list[1:4])
                        vertexes = map(index_to_vertex, indexes)
                        a_tringle = OpenGLTriangle(*vertexes)
                        a_tringle.rgb(1.0, 1.0, 1.0)
                        self._display_object.append(a_tringle)
                if first_string == "comment":
                    second_string = a_list[1]
                    if second_string == "eye_point_xyz":
                        self._projection.eye_point_(map(float, a_list[2:5]))
                    if second_string == "sight_point_xyz":
                        self._projection.sight_point_(map(float, a_list[2:5]))
                    if second_string == "up_vector_xyz":
                        self._projection.up_vector_(map(float, a_list[2:5]))
                    if second_string == "zoom_height" and a_list[3] == "fovy":
                        self._projection.fovy_(float(a_list[4]))

        return

    def default_window_title(self):
        """うさぎのウィンドウのタイトル(ラベル)を応答する。"""
        if TRACE: print __name__, self.default_window_title.__doc__

        return "Stanford Bunny"


class PenguinModel(OpenGLModel):

    """ペンギンのモデル。"""

    def __init__(self):
        """ペンギンのモデルのコンストラクタ。"""
        if TRACE: print __name__, self.__init__.__doc__

        super(PenguinModel, self).__init__()
        self._projection.eye_point_(
            [-6.6153435525924, 3.5413918991617, 27.440373330962])
        self._projection.sight_point_([0.070155, 0.108575, 0.056235])
        self._projection.up_vector_(
            [0.03950581341181, 0.99260439594225, -0.11478590446043])
        self._projection.fovy_(13.527497808711)
        self._axes_scale = 2.0

        filename = os.path.join(os.getcwd(), 'text/penguin.txt')
        if os.path.exists(filename) and os.path.isfile(filename):
            pass
        else:
            url = 'http://www.cc.kyoto-su.ac.jp/~atsushi/Programs/Penguin/penguin.txt'
            urllib.urlretrieve(url, filename)

        with open(filename, "rU") as a_file:
            while True:
                a_string = a_file.readline()
                if len(a_string) == 0: break
                a_list = a_string.split()
                if len(a_list) == 0: continue
                first_string = a_list[0]
                if first_string == "number_of_vertexes":
                    number_of_vertexes = int(a_list[1])
                if first_string == "number_of_polygons":
                    number_of_polygons = int(a_list[1])
                if first_string == "end_header":
                    get_tokens = (lambda file: file.readline().split())
                    collection_of_vertexes = []
                    for n_th in range(number_of_vertexes):
                        a_list = get_tokens(a_file)
                        a_vertex = map(float, a_list[0:3])
                        collection_of_vertexes.append(a_vertex)
                    index_to_vertex = (
                        lambda index: collection_of_vertexes[index - 1])
                    for n_th in range(number_of_polygons):
                        a_list = get_tokens(a_file)
                        number_of_indexes = int(a_list[0])
                        index = number_of_indexes + 1
                        indexes = map(int, a_list[1:index])
                        vertexes = map(index_to_vertex, indexes)
                        a_polygon = OpenGLPolygon(vertexes)
                        self._display_object.append(a_polygon)
                    for n_th in range(number_of_polygons):
                        a_list = get_tokens(a_file)
                        rgb_color = map(float, a_list[0:3])
                        a_polygon = self._display_object[n_th]
                        a_polygon.rgb(*rgb_color)

        return

    def default_window_title(self):
        """ペンギンのウィンドウのタイトル(ラベル)を応答する。"""
        if TRACE: print __name__, self.default_window_title.__doc__

        return "Penguin"


class OniModel(OpenGLModel):

    """鬼のモデル。"""

    def __init__(self):
        """鬼のモデルのコンストラクタ。"""
        if TRACE: print __name__, self.__init__.__doc__

        super(OniModel, self).__init__()
        self._projection.eye_point_(
            [-6.6153435525924, 3.5413918991617, 27.440373330962])
        self._projection.sight_point_(
            [-0.056150078773499, 0.022249937057495, -2.1525999903679])
        self._projection.up_vector_(
            [0.03835909829153, 0.99323407243554, -0.10961139051838])
        self._projection.fovy_(19.221287002173)
        self._axes_scale = 2.7

        filename = os.path.join(os.getcwd(), 'text/oni.txt')
        if os.path.exists(filename) and os.path.isfile(filename):
            pass
        else:
            url = 'http://www.cc.kyoto-su.ac.jp/~atsushi/Programs/Oni/oni.txt'
            urllib.urlretrieve(url, filename)

        with open(filename, "rU") as a_file:
            while True:
                a_string = a_file.readline()
                if len(a_string) == 0: break
                a_list = a_string.split()
                if len(a_list) == 0: continue
                first_string = a_list[0]
                if first_string == "number_of_vertexes":
                    number_of_vertexes = int(a_list[1])
                if first_string == "number_of_polygons":
                    number_of_polygons = int(a_list[1])
                if first_string == "number_of_colors":
                    number_of_colors = int(a_list[1])
                if first_string == "end_header":
                    get_tokens = (lambda file: file.readline().split())
                    collection_of_vertexes = []
                    for n_th in range(number_of_vertexes):
                        a_list = get_tokens(a_file)
                        a_vertex = map(float, a_list[0:3])
                        collection_of_vertexes.append(a_vertex)
                    index_to_vertex = (
                        lambda index: collection_of_vertexes[index - 1])
                    collection_of_indexes = []
                    for n_th in range(number_of_polygons):
                        a_list = get_tokens(a_file)
                        number_of_indexes = int(a_list[0])
                        index = number_of_indexes + 1
                        indexes = map(int, a_list[1:index])
                        vertexes = map(index_to_vertex, indexes)
                        index = int(a_list[index])
                        collection_of_indexes.append(index)
                        a_polygon = OpenGLPolygon(vertexes)
                        self._display_object.append(a_polygon)
                    collection_of_colors = []
                    for n_th in range(number_of_colors):
                        a_list = get_tokens(a_file)
                        rgb_color = map(float, a_list[0:3])
                        collection_of_colors.append(rgb_color)
                    for n_th in range(number_of_polygons):
                        index = collection_of_indexes[n_th]
                        rgb_color = collection_of_colors[index - 1]
                        a_polygon = self._display_object[n_th]
                        a_polygon.rgb(*rgb_color)

        return

    def default_window_title(self):
        """鬼のウィンドウのタイトル(ラベル)を応答する。"""
        if TRACE: print __name__, self.default_window_title.__doc__

        return "Oni"


class BabyModel(OpenGLModel):

    """赤ちゃんのモデル。"""

    def __init__(self):
        """赤ちゃんのモデルのコンストラクタ。"""
        if TRACE: print __name__, self.__init__.__doc__

        super(BabyModel, self).__init__()
        self._projection.eye_point_(
            [-6.6153435525924, 3.5413918991617, 27.440373330962])
        self._projection.sight_point_(
            [0.0, 0.14168989658356, 0.18842494487762])
        self._projection.up_vector_(
            [0.039485481935453, 0.99266691863474, -0.11425097533293])
        self._projection.fovy_(13.079457895221)
        self._axes_scale = 1.8

        filename = os.path.join(os.getcwd(), 'text/baby.txt')
        if os.path.exists(filename) and os.path.isfile(filename):
            pass
        else:
            url = 'http://www.cc.kyoto-su.ac.jp/~atsushi/Programs/Baby/baby.txt'
            urllib.urlretrieve(url, filename)

        with open(filename, "rU") as a_file:
            while True:
                a_string = a_file.readline()
                if len(a_string) == 0: break
                a_list = a_string.split()
                if len(a_list) == 0: continue
                first_string = a_list[0]
                if first_string == "number_of_vertexes":
                    number_of_vertexes = int(a_list[1])
                if first_string == "number_of_polygons":
                    number_of_polygons = int(a_list[1])
                if first_string == "number_of_colors":
                    number_of_colors = int(a_list[1])
                if first_string == "end_header":
                    get_tokens = (lambda file: file.readline().split())
                    collection_of_vertexes = []
                    for n_th in range(number_of_vertexes):
                        a_list = get_tokens(a_file)
                        a_vertex = map(float, a_list[0:3])
                        collection_of_vertexes.append(a_vertex)
                    index_to_vertex = (
                        lambda index: collection_of_vertexes[index - 1])
                    for n_th in range(number_of_polygons):
                        a_list = get_tokens(a_file)
                        number_of_indexes = int(a_list[0])
                        index = number_of_indexes + 1
                        indexes = map(int, a_list[1:index])
                        vertexes = map(index_to_vertex, indexes)
                        a_polygon = OpenGLPolygon(vertexes)
                        self._display_object.append(a_polygon)
                    collection_of_colors = []
                    for n_th in range(number_of_colors):
                        a_list = get_tokens(a_file)
                        rgb_color = map(float, a_list[0:3])
                        collection_of_colors.append(rgb_color)
                    for n_th in range(number_of_polygons):
                        a_list = get_tokens(a_file)
                        index = int(a_list[0])
                        rgb_color = collection_of_colors[index - 1]
                        a_polygon = self._display_object[n_th]
                        a_polygon.rgb(*rgb_color)

        return

    def default_window_title(self):
        """赤ちゃんのウィンドウのタイトル(ラベル)を応答する。"""
        if TRACE: print __name__, self.default_window_title.__doc__

        return "Baby"


def main():
    """OpenGL立体データを読み込んで描画する。"""
    if TRACE: print __name__, main.__doc__

    a_model = DragonModel()
    a_model.open()

    a_model = WaspModel()
    a_model.open()

    a_model = BunnyModel()
    a_model.open()

    a_model = PenguinModel()
    a_model.open()

    a_model = OniModel()
    a_model.open()

    a_model = BabyModel()
    a_model.open()

    glutMainLoop()

    return 0

if __name__ == '__main__':
    sys.exit(main())
