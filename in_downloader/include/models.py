# -*- coding: utf-8 -*-
from helpers import resolve_kwargs, safty_name, atom_fetch_info, compile_string
from json import load, dumps
from os import path, mkdir


class Singleton(type):
    """
    Singleton Model Class, ejemplo tomado desde:
    https://stackoverflow.com/questions/31875/is-there-a-simple-elegant-way-to-define-singletons
    """

    def __init__(cls, name, bases, dict):
        super(Singleton, cls).__init__(name, bases, dict)
        cls.instance = None

    def __call__(cls, *args, **kw):
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__call__(*args, **kw)
        return cls.instance


class Script(object):
    """
    TODO!
    """

    def __init__(self, config=None):
        if not isinstance(config, dict):
            raise TypeError('\'config\' invalido.')
        self.config = config
        self.template = self._load_template()
        self._json_script = {}
        self._targets = []

    @property
    def targets(self):
        return getattr(self, '_targets', [])

    @targets.setter
    def targets(self, target):
        if isinstance(target, dict):
            self._targets.append(target)
            script_fn = '{}_script.json'.format(self.config.get('project_name'))
            full_path_script = path.join(self.config.get('project_folder'), script_fn)
            with open(full_path_script, 'w') as script:
                script.write(dumps(self._targets))
                script.flush()
                script.close()

    @staticmethod
    def _load_template(template=None):
        """
        TODO!
        :return:
        """
        from os.path import join, exists, dirname, abspath
        here = join(dirname(abspath(__file__)))
        if not isinstance(template, (str, unicode)):
            template = 'default'
        template = join(here, 'required/{template}.template.json'.format(template=template))
        if not exists(template):
            template = join(here, 'required/{template}.template.json'.format(template='default'))
        return load(open(template, 'rb'))

    def _translate_data(self, data):
        """

        :return:
        """
        from os import path
        from arrow import now
        image_formats = {
            'image/jpeg': 'JPG',
            'image/png': 'PNG',
            'image/tiff': 'TIF',
        }
        if isinstance(data, dict) and isinstance(self.config, dict):
            if data.get('is_image', False) and data.get('status_code') == 200:
                translated_data = self.template
                img_dst_folder = path.join(self.config.get('project_folder'),
                                           self.config.get('image_destination', 'images'))
                img_crppd_folder = path.join(self.config.get('project_folder'),
                                             self.config.get('crop_image').get('destination_folder'))
                img_rsz_folder = path.join(self.config.get('project_folder'),
                                           '{}_{}x{}'.format(self.config.get('resize').get('destination_folder'),
                                                             self.config.get('resize').get('resize_x'),
                                                             self.config.get('resize').get('resize_y')))
                actual_date = ''
                if self.config.get('filename', {'date': False}).get('date'):
                    actual_date = now().format(self.config.get('filename', {'date_format': 'YYYY-MM-DD'}).get('date_format'))
                config_to_name = {
                    'project_name': self.config.get('project_name'),
                    'suffix': self.config.get('filename').get('suffix', ''),
                    'prefix': self.config.get('filename').get('prefix', ''),
                    'date': actual_date,
                    'index': str(len(self.targets)),
                    'format': image_formats.get(data.get('format')).lower(),
                }
                translated_data.update(
                    {
                        'format': image_formats.get(data.get('format')),
                        'name': self.config.get('project_name'),
                        'image_destination': img_dst_folder,
                        'resize_destination': img_rsz_folder,
                        'fn': compile_string(self.config.get('filename', {'fn': '$project_name.$format'}).get('fn'),
                                             config_to_name),
                        'cropped_destination': img_crppd_folder,
                        'url': data.get('url'),
                        'resize':
                            {
                                "enable": self.config.get('resize').get('enable'),
                                "resize_x": self.config.get('resize').get('resize_x'),
                                "resize_y": self.config.get('resize').get('resize_y'),
                                "fn_mark": self.config.get('resize').get('fn_mark')
                            },
                        'crop_image': {
                            'enable': self.config.get('crop_image').get('enable'),
                            'fn_mark': self.config.get('crop_image').get('fn_mark'),
                            'crop_x0': self.config.get('crop_image').get('crop_x0'),
                            'crop_x1': self.config.get('crop_image').get('crop_x1'),
                            'crop_y0': self.config.get('crop_image').get('crop_y0'),
                            'crop_y1': self.config.get('crop_image').get('crop_y1')
                        },
                        'enable_download': True if data.get('status_code') == 200 else False,
                    }
                )
                return translated_data
        elif isinstance(data, list):
            pass
        else:
            raise TypeError('\'data\' debes ser una instancia de LIST o DICT.')

    def generate(self, target, template='default'):
        """
        TODO!
        :return:
        """
        if isinstance(target, (str, unicode)):
            translated = self._translate_data(self.fetch_information(target))
            if translated:
                self.targets = translated.copy()
                return translated
        elif isinstance(target, list):
            for e in target:
                self.generate(target=e)
        else:
            raise TypeError('\'target\' debe ser: str | unicode | list.')

    @staticmethod
    def fetch_information(url, **kwargs):
        """
        Args:
            - url:
            - kwargs:

        Return:
            - dict
        """
        defaults = resolve_kwargs({
            'parallel_process': False,
            'schema': {}
        }, kwargs)
        return atom_fetch_info(url)

    def save(self):
        """
        TODO
        :return:
        """
        pass

    def __str__(self):
        return dumps(self._json_script)


class ScriptRow(object):
    """
    TODO!
    """

    def __init__(self):
        pass

    def __str__(self):
        pass


class NetImage(object):
    """
    TODO!
    """

    def __init__(self):
        pass


class Config(object):
    """

    """

    def __init__(self, _new_config=None):
        """

        """
        from os.path import exists
        if isinstance(_new_config, (unicode, str)):
            if not exists(_new_config):
                print 'RUNMODE: NON_CUSTOM_CONFIG_SELECTED'
                _new_config = None
            else:
                try:
                    print 'RUNMODE: JSON_CUSTOM_CONFIG_SELECTED'
                    _new_config = load(open(_new_config, 'rb'))
                except Exception as e:
                    print e
                    print 'RUNMODE: NON_CUSTOM_CONFIG_SELECTED'
                    _new_config = None
        elif isinstance(_new_config, dict):
            print 'RUNMODE: CONFIG_DICT_SELECTED'
        else:
            print 'RUNMODE: NON_CUSTOM_CONFIG_SELECTED'
        self.config = self.__load(_new_config)

    def __load(self, amend_config=None):
        default_config = self.__load_defaults()
        if not isinstance(amend_config, default_config.__class__):
            amend_config = {}
        return self.__build_scenario(resolve_kwargs(default_config, amend_config))

    def __load_defaults(self):
        json_config = 'required/defaults.config.json'
        return self.___prepare_config(load(open(json_config, 'rb')))

    @staticmethod
    def ___prepare_config(config):
        """

        Args:
            - config:
        Return:
             TODO
        """
        if config.get('project_folder', 'project') == 'project':
            from os import path
            here = path.dirname(path.abspath(__file__))[:-len('/in_downloader/in_downloader/include')]
            p_folder = path.join(here, config.get('project_folder'))
        else:
            p_folder = config.get('project_folder')
        config.update({'project_folder': safty_name(p_folder, config.get('project_name', 'project'))})
        return config

    @staticmethod
    def __build_scenario(_config):
        """
        TODO!
        Return:
             - TODO
        """
        # Creamos las path absolutas de guardado.
        here = path.dirname(path.abspath(__file__))[:-len('/in_downloader/in_downloader/include')]
        project_folder = path.join(here, _config['project_folder'])
        image_folder = path.join(project_folder, 'images',  _config['image_destination'])
        image_cropped_folder = path.join(project_folder, 'images', _config.get('crop_image').get('destination_folder'))
        image_resised_folder = path.join(project_folder, 'images',  _config.get('resize').get('destination_folder'))

        # Aplicamos los path completos:
        _config['project_folder'] = project_folder
        _config['image_destination'] = image_folder
        _config['crop_image']['destination_folder'] = image_cropped_folder
        _config['resize']['destination_folder'] = image_resised_folder

        # Generamos los directorios si los mismo no existen:
        for folder in [project_folder, image_folder, image_cropped_folder, image_resised_folder]:
            if not path.exists(folder):
                try:
                    mkdir(folder)
                except OSError:
                    pass
        return _config

    def __str__(self):
        return dumps(self.config)


# # Test Implementation:
# from pprint import pprint
# import json
#
# con = Config(json.load(open('samples/custom.config.json', 'rb')))
# script = Script(json.loads(con.__str__()))
# script.generate([
#     'http://haira.halfmoon.jp/photo/plant/kiku/aster-siro-hikari.jpg',
#     'http://www.carlpabst.de/images/3140.jpg',
#     'http://www.nordlommerse.com/site-afbeeldingen/zinnia_klein.jpg',
#     'http://pics.davesgarden.com/pics/zest_1188386607_362_tn.jpg',
#     'http://www.s-ip.net/seeds/datazukan/callistephus/aster1.jpg',
#     'http://margaritta.dir.bg/2003/sept/astra02.jpg'])
# pprint(script.targets)
