import json
import datetime

class Editor:

    def __init__(self, json_path, theme_name, log):
        self.json_path = json_path
        self.log = log
        time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        self.log_file_name = f'log_{theme_name}_{time}'

        with open(self.json_path) as json_file:
            self.json_data = json.loads(json_file.read())

        self.save()
        self.save_log(f'*** [{theme_name}] THEME_LOG_FILE ***')


    def json_edit(self, args):
        if len(args) == 1:
            print(args[0])
            self.save_log('\n\n' + args[0])
            return
        if len(args) == 2:
            self.json_data[args[0]] = args[1]
        elif len(args) == 3:
            self.json_data[args[0]][args[1]] = args[2]
        elif len(args) == 4:
            self.json_data[args[0]][args[1]][args[2]] = args[3]
        self.save()
        self.save_log('\n' + str(args)[1:-1])


    def save(self):
        with open(self.json_path, 'w') as json_file:
            json.dump(self.json_data, json_file, indent=4)


    def save_log(self, log_msg):
        if self.log:
            with open(self.log_file_name, 'a') as log_file:
                log_file.write(log_msg)


    def load_log_file(self, file_name):
        with open(file_name) as log_file:
            log_data = log_file.read().replace('\'', '').split('\n')
        for i in [tuple(i.split(', ')) for i in log_data]:
            self.json_edit(i)
