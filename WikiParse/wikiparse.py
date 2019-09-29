from bs4 import BeautifulSoup
import re
import os
import collections


# Function that return list of links to other pages in wiki;
def page_get(page, path):
    html = open(path + "\\" + page, encoding="utf8").read()
    soup = BeautifulSoup(html, "lxml")
    # we found all links and made them unique;
    links_wiki = list(set(a['href'] for a in soup.select('p a[href]') if a['href'].startswith('/wiki/')))
    # we need just names of articles;
    links = []
    for i in links_wiki:
        links.append(i[6:])
    return links


# Function that deletes pages that are not in our folder;
def del_diff(lis_to_del, path):
    # make a dictionary of articles that we have;
    files = dict.fromkeys(os.listdir(path))
    # return only that articled that we have;
    list_to_return = []
    for i in lis_to_del:
        if i in files:
            list_to_return.append(i)
    return list_to_return


# Function that finds the shortest path from start to end;
def find_way(start, end, path):
    way = {}
    way[start] = [start]
    Q = collections.deque([start])

    while len(Q) != 0:
        # look at next page in queue of pages to visit, get links on that page;
        page = Q.popleft()
        links = page_get(page, path)
        links = del_diff(links, path)

        # look at each link on the page;
        for link in links:

            # if link is our destination, we're done!;
            if link == end:
                return way[page] + [link]

            # if not, check if we already have a record of the don't, we need to reach of pages to explore;
            if (link not in way) and (link != page):
                way[link] = way[page] + [link]
                Q.append(link)

    # if we've exhausted all possible pages to explore in our queue without getting to the destination;
    return None


# Function find the maximum length of references tag in one sequence;
def find_max_ref_len(soup):

    # create list of tags;
    ref_list = [a for a in soup.find_all('a')]
    list_of_len = []
    count = 0
    # calculate, using BS method, length of tags in one sequence;
    for a in ref_list:
        if type(a.find_next_sibling()).__name__ != 'NoneType':
            if a.find_next_sibling().name == 'a':
                count += 1
            else:
                list_of_len.append(count)
                count = 0
    return max(list_of_len)


# The main function that returns the results;
def parse(start, end, path):
    # make the shortest way through start and end pages;
    bridge = find_way(start, end, path)

    out = {}
    # make that pages the BS objects;
    for file in bridge:
        html = open(path + "\\" + file, encoding="utf8").read()
        soup = BeautifulSoup(html, "lxml")
        # we will parsing only body element;
        body = soup.find(id="bodyContent")

        # calculate the quantity of images that width is greater than 200;
        imgs = len(body.select('img[width>=200]'))
        # headers that start with capital letters ("E","T","C");
        headers = len([i.string for i in body.find_all(name=re.compile('^h\d'), string=re.compile('^[ETC]'))])
        # max length of references in one sequence;
        links_len = find_max_ref_len(body)
        # quantity of lists not insert in another list;
        lists = len([a for a in body.find_all('ul') if (a.parent.name != 'li') or (a.parent.parent.name != 'li')])
        # write the results;
        out[file] = [imgs, headers, links_len, lists]

    return print(out)


path = input("Write the path to files: ")
start = input("Write the start article: ")
end = input("Write the end article: ")
# Call main function;
parse(start, end, path)
