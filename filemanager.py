import sys
import os
import codecs
import pandas as pd
import json


class FileManager:
    def __init__(self):
        self.full_path = self.find_path()

    def find_path(self):
        if hasattr(sys, "frozen"):
            full_real_path = os.path.dirname(sys.executable)
        else:
            script_dir = os.path.dirname(__file__)
            full_real_path = os.path.dirname(os.path.realpath(sys.argv[0]))

        full_real_path = full_real_path.split("\\")
        full_real_path = "/".join(full_real_path)
        if not full_real_path.endswith("/"):
            full_real_path = full_real_path + "/"
        return full_real_path

    def finished(self, main, extra_funcs={}):
        message = "if you want to restart type \"reset\" \nelse if you want to exit type \"exit\"\n"
        if extra_funcs:
            for key in extra_funcs:
                message += f"if you want to {key} type \"{key}\"\n"
        cm_input = input(message)
        if cm_input == "reset":
            main()
        elif cm_input == "exit":
            return
        elif extra_funcs:
            for key, value in extra_funcs.items():
                if cm_input == key:
                    function = value[0]
                    args = value[1]
                    function(*args)
        else:
            self.finished(main)

    def save_to_csv(self, table, file_name, columns):
        df = pd.DataFrame(table, columns=columns)
        saving_path = os.path.join(self.full_path, 'csv_files')
        if not os.path.exists(saving_path):
            os.makedirs(saving_path)
        path = f"{saving_path}/{file_name}.csv"
        df.to_csv(path, encoding='utf-8')

    def save_to_log(self, e):
        log_path = os.path.join(self.full_path, 'log')
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        with open(f"{log_path}/log.txt", "a") as f:
            f.write(f"error ={e} \n")

    def save_to_file(self, object, texts, file_name):
        log_path = os.path.join(self.full_path, 'log')
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        with open(f"{log_path}/{file_name}.txt", "a") as f:
            for text in texts:
                f.write(f"{object} = {text} \n")

    def save_to_json(self, data):
        data_path = os.path.join(self.full_path, 'data')
        if not os.path.exists(data_path):
            os.makedirs(data_path)
        print(f"{data_path}/data.txt")
        with codecs.open(f"{data_path}/data.txt", 'w', encoding='utf8') as outfile:
            json.dump(data, outfile ,ensure_ascii=False)
