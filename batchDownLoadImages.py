#batchDownloadImages
from requests_html import HTMLSession
import os
import sys
import re

#check username
def isPageError(page):
    if (page.status_code != 200):
        return True
    return False

#create output dir
outputDir = "qicai"
mainUrl = "https://book.yunzhan365.com/yqhw/tpee/files/mobile/"
minPage = 1
maxPage = 24
tail = ".jpg"
if not os.path.exists(outputDir):
    os.mkdir(outputDir)

print("---create session---")
session = HTMLSession()
mainPage = session.get(mainUrl + str(minPage) + tail)
if (isPageError(mainPage)):
    print("page is not exist!")
    sys.exit()

print("---start download---")
#default max get pages
for i in range(minPage, maxPage + 1):
    listPage = session.get(mainUrl + str(i) + tail)
    if (isPageError(listPage)):
        print("page is not exist!")
        continue

    with open(outputDir + "/" + str(i) + tail, 'wb') as file:
        file.write(listPage.content)
    print("download page: ", i)
