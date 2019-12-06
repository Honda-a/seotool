import kivy
kivy.require('1.10.0')
from kivy.config import Config
Config.set('graphics', 'resizable', 0)
Config.set('graphics', 'width', 600)
Config.set('graphics', 'height', 700)
from kivy.core.window import Window
Window.clearcolor = (0.66, 0.66, 0.66, 1)
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout
from app import App as SeoApp
from kivy.uix.label import Label
from filemanager import FileManager
import threading


class SeoGridLayout(GridLayout):

    # Function called when equals is pressed
    def seo_run(self):
        self.ids.url.disabled = True
        self.ids.auth_id.disabled = True
        self.ids.auth_pass.disabled = True
        self.ids.filename.disabled = True
        self.ids.depth.disabled = True
        self.ids.run.disabled = True
        url = self.ids.url.text
        if self.ids.auth_id.text or self.ids.auth_pass.text:
            basic_auth = f"{auth_id},{auth_pass}"
        else:
            basic_auth = ""
        depth = int(self.ids.depth.text) if self.ids.depth.text else 0
        self.ids.layout_content.clear_widgets()
        self.my_backend_app = SeoApp(url, depth=depth, basic_auth=basic_auth)
        self.my_app_thread = threading.Thread(target=self.my_backend_app.run)
        self.my_app_thread.start()
        self.my_task_schedule = Clock.schedule_interval(self.refresh_csv_file, 0.5)

    def refresh_csv_file(self, dt):
        fm = FileManager()
        if self.my_app_thread.is_alive():
            urls_to_show = self.my_backend_app.get_urls_to_show()
            for urls in urls_to_show:
                self.ids.layout_content.add_widget(Label(text=f"{urls}", outline_color=[1,0.75,0.75,1]))
                self.ids.layout_content.add_widget(Label(text=f"{urls_to_show[urls]}", outline_color=[0.75,0.75,0.75,1]))
            table, column = self.my_backend_app.get_csv_table()
            fm.save_to_csv(table, self.ids.filename.text, column)
        else:
            self.ids.url.disabled = False
            self.ids.auth_id.disabled = False
            self.ids.auth_pass.disabled = False
            self.ids.filename.disabled = False
            self.ids.depth.disabled = False
            self.ids.run.disabled = False

    def cancel_crawl(self):
        fm = FileManager()
        self.my_task_schedule.cancel()
        self.my_backend_app.stop()
        table, column = self.my_backend_app.get_csv_table()
        fm.save_to_csv(table, self.ids.filename.text, column)
        self.my_backend_app = False
        self.ids.url.disabled = False
        self.ids.auth_id.disabled = False
        self.ids.auth_pass.disabled = False
        self.ids.filename.disabled = False
        self.ids.depth.disabled = False
        self.ids.run.disabled = False

class SeoTool(App):

    def build(self):
        return SeoGridLayout()

calcApp = SeoTool()
calcApp.run()
