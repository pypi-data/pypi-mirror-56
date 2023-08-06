from .android import Android
from .ios import IOS

class Theme:

    def __init__(self, theme_name, os_type='Android', base_theme='black', log=True):
        if os_type == 'iOS':
            self.platform = IOS(theme_name, base_theme, log)
        elif os_type == 'Android':
            self.platform = Android(theme_name, base_theme, log)
        else:
            raise Exception('Not found platform')


    def thaw_file(self):
        self.platform.thaw()


    def compression_file(self, delete_temp=True):
        self.platform.compression(delete_temp)


    def edit_theme(self, *args):
        self.platform.edit_json(args)


    def edit_by_egg(self, place, key, status):
        self.platform.edit_by_egg(place, key, status)


    def add_image(self, file_name):
        self.platform.add_image(file_name)


    def load_log(self, file_name):
        self.platform.load_theme_log(file_name)


    def apply(self, theme_id=None):
        self.platform.line_apply(theme_id)
