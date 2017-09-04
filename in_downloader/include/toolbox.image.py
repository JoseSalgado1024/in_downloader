from helpers import resolve_kwargs, guid
from os import path, makedirs
import cv2
import numpy as np


def split_image():
    pass


def crop_image(image, **kwargs):
    defaults = resolve_kwargs({"enable": True,
                               "destination_folder": "cropped_images",
                               "fn_mark": "cropped",
                               "crop_x0": 0,
                               "crop_x1": 0,
                               "crop_y0": 0,
                               "crop_y1": 0}, kwargs)
    if isinstance(image, list):
        return filter(None, [crop_image(i, kwargs) for i in image])
    img = get_image(image)
    if img:
        img_x, img_y, img_channels = img.shape
        if img_x >= img_y:
            x_start = int((img_x - img_y) / 2)
            x_end = x_start + img_y
            y_start = 0
            y_end = img_y
        else:
            y_start = int((img_y - img_x) / 2)
            y_end = y_start + img_x
            x_start = 0
            x_end = img_x
        img = img[x_start:x_end, y_start:y_end]

        if defaults['enable']:
            crop_dest_folder = defaults.get('destination_folder')
            crop_fn = '{fn}{fn_mark}.{f}'.format(
                fn=defaults.get('fn', guid()),
                fn_mark=defaults.get('fn_mark'),
                f=defaults.get('format', 'png').lower()
            )
            if not path.exists(crop_dest_folder):
                makedirs(crop_dest_folder)
            crp_img_filename = path.join(crop_dest_folder, crop_fn)
            try:
                cv2.imwrite(crp_img_filename, img)
                return crp_img_filename
            except Exception as e:
                print e


def get_image(image):
    """
    Normalizar entra de imagenes.

    Args:
        - image:

    Return:
        - image.np.ndarray
    """
    if isinstance(image, np.ndarray):
        print 'Loading from np.array.'
        return image
    elif isinstance(image, (str, unicode)):
        print 'Loading from file.'
        if not path.exists():
            print 'No existe {}.'.format(image)
            return None
        try:
            return cv2.imread(image)
        except:
            print 'Fallo carga de imagen {}.'.format(image)
            return None
    elif isinstance(image, list):
        print 'Loading from list.'
        return filter(None, [get_image(img) for img in image])
    else:
        return None


def resize_image(_image_fn, **kwargs):
    if not isinstance(_image_fn, (str, unicode)):
        print 'Fallo: \'_image_fn\' debe ser una instancia de unicode o str. {}'.format(_image_fn)
    defaults = resolve_kwargs({"enable": False,
                               "resize_x": 50,
                               "resize_y": 50,
                               "square_image": True,
                               "destination_folder": "resided_images",
                               "fn_mark": "resided"}, kwargs)
    respose = {
        'status': False,
        'msg': ['No ejecutado.'],
        'input_img': _image_fn,
        'output_img': ''
    }
    if not isinstance(_image_fn, (str, unicode)):
        return respose
    if not path.exists(_image_fn):
        respose.update({'msg': ['No existe la imagen {}.'.format(_image_fn)]})
    print 'Croppenado: \'{}\'.'.format(_image_fn)
    try:
        img = cv2.imread(_image_fn)
    except Exception as load_image_error:
        respose.update({'msg': ['Fallo la carga de la imagen{}, error: {}.'.format(_image_fn, load_image_error)]})
        return respose
    if defaults['square_image']:
        img_x, img_y, img_channels = img.shape
        if img_x >= img_y:
            x_start = int((img_x - img_y) / 2)
            x_end = x_start + img_y
            y_start = 0
            y_end = img_y
        else:
            y_start = int((img_y - img_x) / 2)
            y_end = y_start + img_x
            x_start = 0
            x_end = img_x
        img = img[x_start:x_end, y_start:y_end]

        if defaults['enable']:
            crop_dest_folder = defaults.get('destination_folder')
            crop_img_format = _image_fn.split('.')[len(_image_fn.split('.')) - 1]
            crop_fn = '{fn}{fn_mark}.{f}'.format(
                fn=_image_fn[:-len(crop_img_format) - 1],
                fn_mark=defaults['fn_mark'],
                f=crop_img_format
            )
            if not path.exists(crop_dest_folder):
                makedirs(crop_dest_folder)
            crp_img_filename = path.join(crop_dest_folder, crop_fn)
            respose.update({'image_cropped': {
                'path': crp_img_filename,
                'fn': crop_fn
            },
                'msg': ['Imagen {} re-encuadrada a {}x{}'.format(crop_fn,
                                                                 x_end,
                                                                 y_end)]})
            _tmp_img = cv2.imwrite(crp_img_filename, img)
        else:
            _tmp_img = img
        cv2.imwrite('resize/image.png', cv2.resize(_tmp_img, (defaults['resize_w'], defaults['resize_h'])))
        respose.update({'msg': ['Realizado con exito.'],
                           'output_img': 'resize/image.png'})
        return respose

print get_image(['str'])