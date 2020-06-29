from apis import *

def getTag():
    tag = None
    while tag is None:
        tag = input("Enter the hashtag to scrape \n")
        if ' ' in tag:
            print("No spaces allowed")
            tag = None
        if '#' in tag:
            tag = tag.replace('#','')
    return tag

tag = getTag()
getUsers(tag,0)
