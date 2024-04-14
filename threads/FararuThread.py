from bs4 import BeautifulSoup
import threading, requests, enum, json


# defining different types of thread
class TYPES (enum.Enum):
    NONE= 0
    URLS= 1
    IMAGE= 2


class FararuThread(threading.Thread):
    id = 0
    link = ""
    type = TYPES.NONE


    def __init__(self, id, link, type, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        super().__init__(group, target, name, args, kwargs, daemon=daemon)
        self.id = id
        self.link = link
        self.type = type


    # request to given url
    def request_to_page(self, link):
        response = requests.get(link)
        return response


    # create soup with the given response
    def create_soup(self, response):
        soup = BeautifulSoup(response.content, "html.parser")
        return soup


    # get all links related to images
    def get_all_image_urls(self, soup):
        image_soups = soup.find_all("img")
        all_image_urls = []

        for image in image_soups:
            try:
                all_image_urls.append(image["data-src"])
            except KeyError:
                pass
        return all_image_urls


    # get requiered image urls
    def get_image_urls(self, all_image_urls):
        extensions = ["jpg", "bmp", "png", "jpeg"]
        image_urls=[]
        for image_url in all_image_urls:
            url = image_url.split(".")
            if url[0]=="https://cdn" and url[-1] in extensions:
                image_urls.append(image_url)
        return image_urls
    

    # runs when we want to get Fararu image urls
    def get_urls(self):
        response = self.request_to_page(self.link)
        soup = self.create_soup(response)
        all_image_urls = self.get_all_image_urls(soup)
        image_urls = self.get_image_urls(all_image_urls)
        return image_urls
    

    # save urls into a file
    def save_urls(self, image_urls):
        with open("./links/fararu.json", "w") as f:
            image_urls = json.dumps(image_urls)
            f.write(image_urls)
            f.close()


    # save image in fararu image folder
    def save_image(self, content, ext, name):
        with open("./files/fararu/" + name + "." + ext, "wb") as f:
            f.write(content)
            f.close()
            return


    # runs when we want to download Fararu images
    def get_image(self):
        ext = self.link.strip().split(
            "/")[-1].strip().split("?")[0].strip().split(".")[-1]
        name = self.link.strip().split(
            "/")[-1].strip().split("?")[0].strip().split(".")[0]
        content = requests.get(self.link).content
        return content, ext, name
    

    # runs when thread is called
    def run(self):
        print('thread id :', self.id)
        if self.type == TYPES.IMAGE:
            image = self.get_image()
            self.save_image(image[0], image[1], image[2])
        elif self.type == TYPES.URLS:
            image_urls = self.get_urls()
            self.save_urls(image_urls)
            return

