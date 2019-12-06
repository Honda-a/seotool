from spider import Spider
from command import CommandUi
from app import App
from filemanager import FileManager
import threading
from time import sleep


def listen(app, app_thread, name_of_file, file_manager, fetching_message="fetching"):
    while app_thread.is_alive():
        sleep(10)
        table, column = app.get_csv_table()
        file_manager.save_to_csv(table, name_of_file, column)
        app.remaining()
        print(f"{fetching_message}...")
    table, column = app.get_csv_table()
    file_manager.save_to_csv(table, name_of_file, column)


def retrive_lost_urls(app, file_manager):
    app.retrive_lost_urls()
    app_thread = threading.Thread(target=app.run)
    app_thread.start()
    name_of_file = "lost-urls"
    event = listen(app, app_thread, name_of_file, file_manager, fetching_message="fetching lost urls")
    table, column = app.get_csv_table()
    file_manager.save_to_csv(table, name_of_file, column)


def show_lost_urls(app):
    print(app.show_lost_urls())


def main():
    commandui = CommandUi()
    url, depth, basic_auth = commandui.start_page("crawl")
    name_of_file = input("file name :")
    file_manager = FileManager()
    full_path = file_manager.full_path
    app = App(url, full_path, depth=depth, basic_auth=basic_auth)
    app_thread = threading.Thread(target=app.run)
    app_thread.start()
    table, column = app.get_csv_table()
    file_manager.save_to_csv(table, name_of_file, column)
    event = listen(app, app_thread, name_of_file, file_manager)
    if not event:
        if app.has_lost_url():
            extra_option = {"retrive lost urls": [retrive_lost_urls, (app, file_manager)], "show lost urls": [show_lost_urls, (app, )], }
            file_manager.finished(main, extra_option)
        else:
            file_manager.finished(main)
        return app.stop()

if __name__ == "__main__":
    main()
