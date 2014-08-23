__author__ = 'jeong-yonghan'

from bs4 import BeautifulSoup
import mechanize
import urllib

def main():
    def download_html():
        url = "http://www.likelion.net"
        htmlread = mechanize.urlopen(url)
        htmltext = htmlread.read()
        soupsoup = BeautifulSoup(htmltext)
        return soupsoup

    soup = download_html()
    for soup


if __name__ == "__main__":
    main()