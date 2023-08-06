from .editor import Editor
from .config import Config

import os
import glob
import shutil
import zipfile

class Android(Config):

    editor = None

    def __init__(self, theme_name, base_theme, log):
        self.log = log
        self.theme_name = theme_name
        self.base_theme = base_theme

        self.comp_dir_path = f'comp_themefile/Android/{theme_name}'
        self.temp_dir_path = f'temp_{self.theme_name}'
        self.comp_file_path = f'{self.comp_dir_path}/themefile'
        self.base_file_path = f'base_themefile/Android/{base_theme}'
        self.json_file_path = f'{self.temp_dir_path}/theme.json'

        os.makedirs(self.comp_dir_path, exist_ok=True)

        if not os.path.exists(self.base_file_path):
            raise Exception('No exist base themefile')

        if os.path.exists(self.json_file_path):
            self.__set_editor()


    def __set_editor(self):
        if self.editor is None:
            self.editor = Editor(self.json_file_path, self.theme_name, self.log)


    def thaw(self):
        with zipfile.ZipFile(self.base_file_path) as zip_file:
            zip_file.extractall(self.temp_dir_path)
        self.__set_editor()


    def compression(self, delete_temp):
        if os.path.exists(self.temp_dir_path):
            if not os.path.exists(f'{self.temp_dir_path}/images/'):
                raise Exception('No exist images data')
            if not os.path.exists(self.json_file_path):
                raise Exception('No exist json data')
            shutil.make_archive(self.temp_dir_path, 'zip', self.temp_dir_path)
            os.rename(f'{self.temp_dir_path}.zip', self.comp_file_path)
            if delete_temp:
                shutil.rmtree(self.temp_dir_path)
        else:
            raise Exception('No exist temp directory.')


    def edit_json(self, args):
        self.editor.json_edit(args)


    def load_theme_log(self, file_name):
        self.editor.load_log_file(file_name)


    def edit_by_egg(self, place, key, status):
        args = self.egg_dict[place][key] + (status, )
        self.editor.json_edit(args)


    def add_image(self, file_name):
        shutil.copy(file_name, f'{self.temp_dir_path}/images/{file_name}')


    def line_apply(self, theme_id):
        if theme_id is None:
            theme_id = self.theme_id_dict.get(self.base_theme)
        file_list = glob.glob(f'{self.android_theme_dir_path}{theme_id}/themefile.*')
        if not file_list:
            raise Exception('Not found themefile.')
        shutil.copy(self.comp_file_path, file_list[0])
