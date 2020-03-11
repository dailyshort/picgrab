#!/usr/bin/python3
from urllib.request import urlopen
from urllib.request import urlretrieve
from urllib import parse
from bs4 import BeautifulSoup
import sys
import os


class HtmlImageParser:
    def __init__(self, url):
        self._target_url = url
        self._soup = BeautifulSoup(urlopen(url), "html.parser")
        self._image_urls = self.__parse_image_links()

    def get_image_urls(self):
        return self._image_urls

    def download_images_to(self, target_path):
        for url in self._image_urls:
            try:
                urlretrieve(url, target_path + url.rsplit('/', 1)[-1])
            except Exception as e:
                print("The image {0} could not be fetched and stored to {1}\n{2}".format(url, target_path, e))

    def __parse_image_links(self):
        full_paths = []
        for src in self._soup.findAll("img"):
            full_paths.append(parse.urljoin(self._target_url, src["src"]))
        return full_paths


def create_parser(url):
    parser = None
    try:
        parser = HtmlImageParser(url)
    except Exception as e:
        print("Error fetching and parsing the page({0})! :\n{1}".format(url, e))
    return parser


def write_file(path, lines):
    try:
        file = open(path, "w")
        for line in lines:
            file.write(line + "\n")
        file.close()
    except IOError as e:
        print("File io error!\n{0}".format(e))


def test_cmd_line_args():
    is_test_ok = True
    if len(sys.argv) != 4:
        is_test_ok = False
    return is_test_ok


def main():
    if test_cmd_line_args():
        parser = create_parser(sys.argv[1])
        if parser is not None:
            write_file(sys.argv[2], parser.get_image_urls())
            parser.download_images_to(sys.argv[3])
    else:
        print("\nUsage python3 {0} URL P1 P2.\nWhere URL is target site, P1 is path where to store links"
              " and P2 path where to store images.".format(os.path.basename(__file__)))

if __name__ == "__main__":
    main()
