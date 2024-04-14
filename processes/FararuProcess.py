import multiprocessing, time, json, os
import threads.FararuThread as FararuTh


class FararuProcess(multiprocessing.Process):
    id = 0

    def __init__(self, id, group=None, target=None, name=None, args=(), kwargs={}, *, daemon=None):
        super().__init__(group, target, name, args, kwargs, daemon=daemon)
        self.id = id


    # open Fararu urls file
    def open_links_file(self):
        with open("./links/fararu.json", "r") as f:
            urls = f.read()
            urls = json.loads(urls)
            f.close()
        return urls


    def get_images(self):
        urls = self.open_links_file()
        # runs if Fararu urls file exist
        threads = []
        th_id = 1
        for url in urls:
            thread = FararuTh.FararuThread(th_id, url, FararuTh.TYPES.IMAGE)
            thread.start()
            threads.append(thread)
            th_id+=1
            time.sleep(1)
        for thread in threads:
            thread.join()

    def run(self):
        print('process id :', self.id)
        # checks if Fararu urls file exists
        if os.path.exists("./links/fararu.json"):
            self.get_images()
        # runs if Fararu urls file does not exists
        else:
            th1 = FararuTh.FararuThread(0, "https://fararu.com/", FararuTh.TYPES.URLS)
            th1.start()
            while th1.is_alive():
                time.sleep(5)
            else:
                self.get_images()
            return

