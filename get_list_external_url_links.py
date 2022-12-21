import requests
import json
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import lxml

from slugify import slugify
# slugify("cra#5y ST*&^%ING") will output "cra-5y-st-ing" which is computer friendly.

# List of User Agents: https://developers.whatismybrowser.com/useragents/explore/
user_agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}

sitemap_url = "https://progips.com.ua/sitemap.xml"

def get_list_external_urls_from_url(url):
    request = requests.get(sitemap_url, headers=user_agent)
    content = request.content
    soup = BeautifulSoup(content, 'lxml')
    #print(soup)

    list_of_locs = soup.find_all("loc")
    list_of_xml_links = []

    for loc in list_of_locs:
        list_of_xml_links.append(loc.text)

    print(list_of_xml_links)
############# async def get_links_from_sitemap(url)->list:

    list_of_urls = []

    for xml_link in list_of_xml_links:
        #print(f"xml_link = {xml_link}")

        request = requests.get(xml_link, headers=user_agent)
        content = request.content
        soup = BeautifulSoup(content, 'lxml')

        list_of_locs = soup.find_all("loc")

        for loc in list_of_locs:
            print(f"{loc.text=}")
            list_of_urls.append(loc.text)
######### asinc def get_all_external_links()
    print("XML Retrieval complete")

    # Loop through every URL now and looks for external links:
    for url in list_of_urls:
        print(url)

    print("External Links Retrieval Starting")

    csv_row_list = []
    count = 0
    length_list = len(list_of_urls)

    for url in list_of_urls:

        count = count + 1

        request = requests.get(url, headers=user_agent)
        content = request.content
        soup = BeautifulSoup(content, 'lxml')

        list_of_links = soup.find_all("a")

        list_of_href_values = []

        for link in list_of_links:
            try:
                if "progips.com.ua" in link["href"] or "http" not in link["href"]:
                    pass
                else:
                    csv_row_list.append([url, link["href"]])
            except:
                pass

        print(count, " out of ", length_list, " done.")

    import csv

    with open(f'external_links_{sitemap_url}.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Page URL", "External Link"])
        writer.writerows(csv_row_list)



get_list_external_urls_from_url(sitemap_url)
