import cv2
import diplib as dip
import matplotlib.pyplot as plt
import numpy as np
import pydicom
from gstools import SRF, Gaussian
from matplotlib.backends.backend_agg import FigureCanvasAgg
from pydicom import dcmread
from scipy.special import binom
from sklearn.preprocessing import minmax_scale

from app.services import FileService

bernstein = lambda n, k, t: binom(n, k) * t**k * (1.0 - t) ** (n - k)


def bezier(points, num=200):
    N = len(points)
    t = np.linspace(0, 1, num=num)
    curve = np.zeros((num, 2))
    for i in range(N):
        curve += np.outer(bernstein(N - 1, i, t), points[i])
    return curve


class Segment:
    def __init__(self, p1, p2, angle1, angle2, **kw):
        self.p1 = p1
        self.p2 = p2
        self.angle1 = angle1
        self.angle2 = angle2
        self.numpoints = kw.get("numpoints", 100)
        r = kw.get("r", 0.3)
        d = np.sqrt(np.sum((self.p2 - self.p1) ** 2))
        self.r = r * d
        self.p = np.zeros((4, 2))
        self.p[0, :] = self.p1[:]
        self.p[3, :] = self.p2[:]
        self.calc_intermediate_points(self.r)

    def calc_intermediate_points(self, r):
        self.p[1, :] = self.p1 + np.array(
            [self.r * np.cos(self.angle1), self.r * np.sin(self.angle1)]
        )
        self.p[2, :] = self.p2 + np.array(
            [self.r * np.cos(self.angle2 + np.pi), self.r * np.sin(self.angle2 + np.pi)]
        )
        self.curve = bezier(self.p, self.numpoints)


def get_curve(points, **kw):
    segments = []
    for i in range(len(points) - 1):
        seg = Segment(
            points[i, :2], points[i + 1, :2], points[i, 2], points[i + 1, 2], **kw
        )
        segments.append(seg)
    curve = np.concatenate([s.curve for s in segments])
    return segments, curve


def ccw_sort(p):
    d = p - np.mean(p, axis=0)
    s = np.arctan2(d[:, 0], d[:, 1])
    return p[np.argsort(s), :]


def get_bezier_curve(a, rad=0.2, edgy=0):
    """given an array of points *a*, create a curve through
    those points.
    *rad* is a number between 0 and 1 to steer the distance of
          control points.
    *edgy* is a parameter which controls how "edgy" the curve is,
           edgy=0 is smoothest."""
    p = np.arctan(edgy) / np.pi + 0.5
    a = ccw_sort(a)
    a = np.append(a, np.atleast_2d(a[0, :]), axis=0)
    d = np.diff(a, axis=0)
    ang = np.arctan2(d[:, 1], d[:, 0])
    f = lambda ang: (ang >= 0) * ang + (ang < 0) * (ang + 2 * np.pi)
    ang = f(ang)
    ang1 = ang
    ang2 = np.roll(ang, 1)
    ang = p * ang1 + (1 - p) * ang2 + (np.abs(ang2 - ang1) > np.pi) * np.pi
    ang = np.append(ang, [ang[0]])
    a = np.append(a, np.atleast_2d(ang).T, axis=1)
    s, c = get_curve(a, r=rad, method="var")
    x, y = c.T
    return x, y, a


def get_random_points(n=5, scale=0.8, mindst=None, rec=0):
    """create n random points in the unit square, which are *mindst*
    apart, then scale them."""
    mindst = mindst or 0.7 / n
    a = np.random.rand(n, 2)
    d = np.sqrt(np.sum(np.diff(ccw_sort(a), axis=0), axis=1) ** 2)
    if np.all(d >= mindst) or rec >= 200:
        return a * scale
    else:
        return get_random_points(n=n, scale=scale, mindst=mindst, rec=rec + 1)


def filled_random_contour(n, scale=1, rad=0.2, edgy=0.05):
    """
    Создание случайного замкнутого заполненного контура
    Возвращает бинарный массив - маску

    Args:
        n - кол-во точек
        scale - масштаб
        rad - см. https://stackoverflow.com/a/50751932/12691808
        edgy - см. https://stackoverflow.com/a/50751932/12691808
    """
    a = get_random_points(n=n, scale=scale)
    x, y, _ = get_bezier_curve(a, rad=rad, edgy=edgy)
    fig = plt.figure()
    plt.gca().set_aspect("equal")
    plt.fill(x, y, color="black")
    plt.xlim([0, 1])
    plt.ylim([0, 1])
    # plt.tight_layout()
    plt.box(False)
    plt.tick_params(
        which="both",  # both major and minor ticks are affected
        bottom=False,  # ticks along the bottom edge are off
        left=False,
        top=False,  # ticks along the top edge are off
        labelbottom=False,  # labels along the bottom edge are off
        labelleft=False,
    )
    # plt.show()
    # plt.grid()
    canvas = plt.gcf().canvas
    agg = canvas.switch_backends(FigureCanvasAgg)
    agg.draw()
    result_array = np.asarray(agg.buffer_rgba())
    result_array = result_array[:, :, 1]
    return result_array


def create_GRF_mask(shape, rng=(0.2, 3.0), scale=20, seed=20170519):
    """

    Args:
        shape: кортеж (ширина, высота) изображения/карты
        rng: кортеж (мин, макс) значение карты
        scale - масштаб
    """
    # x = img.Sizes()[0]
    # y = img.Sizes()[1]
    x = shape[0]
    y = shape[1]
    shape = (range(x), range(y))
    model = Gaussian(dim=2, var=1.0, len_scale=scale)
    srf = SRF(model, seed=seed)
    blur_map = srf.structured(shape)
    blur_map = minmax_scale(blur_map.flatten().astype(float), feature_range=rng)
    blur_map = blur_map.reshape([x, y])  # .astype(dtype=np.uint8)
    # blur_map = blur_map * 2 + 1
    return blur_map


def add_nodule(src, coord=(150, 250), size=(100, 100)):
    """
    Args:
        src - исходное изображение (numpy array)
        coord - координаты (x, y) центра узла, пиксели, от левого верхнего угла
        size - размеры узла, пиксели, (ширина, высота)
    """


def add_nodule(src, coord=(150, 250), size=(100, 100)):
    """
    Args:
        src - исходное изображение (numpy array)
        coord - координаты (x, y) центра узла, пиксели, от левого верхнего угла
        size - размеры узла, пиксели, (ширина, высота)
    """
    wc = 0  # центр окна яркости опухоли
    ww = 1500  # ширина окна яркости опухоли
    image_shift = src.min()
    # print("image_shift = ", image_shift)
    image_begin = wc - ww / 2
    image_end = wc + ww / 2

    random_contour_nparray = filled_random_contour(n=7, scale=1, rad=0.2, edgy=0.05)
    orig_shape = random_contour_nparray.shape
    # plt.figure()
    # plt.imshow(random_contour_nparray, cmap=plt.cm.gray)
    GRF_mask_nparray = create_GRF_mask(
        random_contour_nparray.shape, rng=(0.1, 10.0), scale=50
    )
    random_contour_blurred_diplib = dip.AdaptiveGauss(
        random_contour_nparray, [0, GRF_mask_nparray], sigmas=[11]
    )
    random_contour_blurred_array = np.asarray(
        random_contour_blurred_diplib, dtype=np.int16
    )
    # print("blurred = ", random_contour_blurred_array.min(), random_contour_blurred_array.max())
    random_contour_blurred_array = random_contour_blurred_array.flatten()
    # print("flatten = ", random_contour_blurred_array.min(), random_contour_blurred_array.max())
    random_contour_blurred_array = minmax_scale(
        random_contour_blurred_array, feature_range=(0, ww)
    )
    # print("minmax_scale = ", random_contour_blurred_array.min(), random_contour_blurred_array.max())
    random_contour_blurred_array = random_contour_blurred_array.reshape(
        orig_shape
    ).astype(dtype=np.int16)
    # print("reshape = ", random_contour_blurred_array)
    # TODO вписать сгенерированный контур в size
    # random_contour_blurred_array = np.invert(random_contour_blurred_array)
    random_contour_blurred_array = (
        random_contour_blurred_array.max() - random_contour_blurred_array
    )
    # print("2 = ", random_contour_blurred_array)
    # ret,alpha_mask = cv2.threshold(random_contour_blurred_array,1,255,cv2.THRESH_BINARY)
    random_contour_resized = cv2.resize(
        random_contour_blurred_array, size, interpolation=cv2.INTER_AREA
    )
    # print("3 = ", random_contour_resized)
    random_contour_resized = np.array(0.9 * random_contour_resized, dtype=np.int16)
    # print("4 = ", random_contour_resized)
    # alpha_mask_resized = cv2.threshold(cv2.resize(alpha_mask, size, interpolation = cv2.INTER_AREA),1,255,cv2.THRESH_BINARY)
    src = src + np.abs(image_shift)
    roi = src[coord[1] : coord[1] + size[1], coord[0] : coord[0] + size[0]]
    dst = cv2.add(roi, random_contour_resized)
    src[coord[1] : coord[1] + size[1], coord[0] : coord[0] + size[0]] = dst
    # cv.bitwise_and(src[],random_contour_resized,mask = alpha_mask_resized)
    result = None
    return src - np.abs(image_shift)


def image_from_dicom(filename, wc=0, ww=1500, dtype=np.uint8):
    dicom_file = dcmread(filename)
    image_matrix = dicom_file.pixel_array

    orig_shape = image_matrix.shape
    print("min = ", image_matrix.min())
    print("max = ", image_matrix.max())

    # выделение к окна wc/ww (засветка и затемнение прочих частей матрицы)

    lung_brightness_lower = wc - ww / 2
    lung_brightness_upper = wc + ww / 2

    image_matrix[image_matrix < lung_brightness_lower] = lung_brightness_lower
    image_matrix[image_matrix > lung_brightness_upper] = lung_brightness_upper

    # нормализация под диапазон обычного изображения (0,255)
    # normalized_matrix = minmax_scale(image_matrix.flatten(), feature_range=(0,65535))
    normalized_matrix = minmax_scale(image_matrix.flatten(), feature_range=(0, 255))
    displayed_matrix_8bit = normalized_matrix.reshape(orig_shape).astype(dtype=dtype)
    # print("min = ", displayed_matrix_8bit.min())
    # print("max = ", displayed_matrix_8bit.max())
    return displayed_matrix_8bit


def generate_simple_dcm_file(filename: str) -> str:
    dicom_file = dcmread(filename)

    # наложение новообразования
    # параметры coord=(150, 250), size=(100, 100) - из параметров API-запроса
    result = add_nodule(dicom_file.pixel_array, coord=(150, 250), size=(100, 100))
    # сохранение в new_file_name
    new_file_name = FileService.generate_file_path()
    newfileMeta = pydicom.Dataset()

    newfileMeta = dicom_file.file_meta

    newds = pydicom.Dataset()
    newds.file_meta = newfileMeta

    newds.Rows = result.shape[0]
    newds.Columns = result.shape[1]
    newds.NumberOfFrames = 1

    newds.PixelSpacing = dicom_file.PixelSpacing  # in mm
    newds.SliceThickness = dicom_file.SliceThickness  # in mm

    newds.BitsAllocated = dicom_file.BitsAllocated
    newds.PixelRepresentation = dicom_file.PixelRepresentation
    newds.SamplesPerPixel = dicom_file.SamplesPerPixel
    newds.PhotometricInterpretation = dicom_file.PhotometricInterpretation
    newds.BitsStored = dicom_file.BitsStored
    newds.PixelData = result.tobytes()
    newds.save_as(new_file_name, write_like_original=False)
    return new_file_name


if __name__ == "__main__":
    filename = "1-18.dcm"
    dicom_file = dcmread(filename)

    # наложение новообразования
    # параметры coord=(150, 250), size=(100, 100) - из параметров API-запроса
    result = add_nodule(dicom_file.pixel_array, coord=(150, 250), size=(100, 100))
    # сохранение в new_file_name
    new_file_name = "newimage.dcm"
    newfileMeta = pydicom.Dataset()

    newfileMeta = dicom_file.file_meta

    newds = pydicom.Dataset()
    newds.file_meta = newfileMeta

    newds.Rows = result.shape[0]
    newds.Columns = result.shape[1]
    newds.NumberOfFrames = 1

    newds.PixelSpacing = dicom_file.PixelSpacing  # in mm
    newds.SliceThickness = dicom_file.SliceThickness  # in mm

    newds.BitsAllocated = dicom_file.BitsAllocated
    newds.PixelRepresentation = dicom_file.PixelRepresentation
    newds.SamplesPerPixel = dicom_file.SamplesPerPixel
    newds.PhotometricInterpretation = dicom_file.PhotometricInterpretation
    newds.BitsStored = dicom_file.BitsStored
    newds.PixelData = result.tobytes()
    newds.save_as(new_file_name, write_like_original=False)
