#crawMyCsdnBlog.py
from requests_html import HTMLSession
import os
import sys
import re

#get input username
userName = input("Please inpu csdn username:")
if (userName == ""):
    print("Input name is empty!")
    sys.exit()

#check username
def isPageError(page):
    if (page.status_code != 200):
        return True
    return False

#create output dir
outputDir = userName
if not os.path.exists(outputDir):
    os.mkdir(outputDir)

#write content to html file
def writeHtmlContent(fileName, titleElement, contentElement):
    file = open(fileName, "w", encoding="utf-8")
    file.write('<html lang="zh-CN">\r\n')
    file.write('  <head>\r\n')
    file.write('    <meta http-equiv="content-type" content="text/html; charset=utf-8">\r\n')
    file.write('    <title>{}</title>\r\n'.format(titleElement.text))
    file.write('  </head>\r\n')
    file.write('  <body>\r\n')
    file.write('    <div class="article-title-box">{}</div>\r\n'.format(titleElement.html))
    file.write(contentElement.html)
    file.write('\r\n  </body>\r\n')
    file.write('</html>\r\n')
    file.close()

#repalce specail charactor
def getValidFileName(fileName):
    fileName = re.sub(r'[ <>/:*?"|\\-]', "_", fileName) #replace special charactor to '_'
    fileName = re.sub('__+', "_", fileName)              #replace duplicate '_'
    return fileName

session = HTMLSession()
mainUrl = "https://blog.csdn.net/{}/".format(userName)
mainPage = session.get(mainUrl)
if (isPageError(mainPage)):
    print("User name is not exist!")
    sys.exit()
    
#default max get 100 pages
checkUrlUserName= "/" + userName + "/"
for i in range(1, 101):
    listPage = session.get(mainUrl + "article/list/" + str(i))
    articleUrlList = listPage.html.find("#mainBox > main > div.article-list", first=True)
    if (articleUrlList is None):
        break;
    
    print("process page {}".format(i).center(50, "-"))
    uid = listPage.html.find("body > header > div > div.title-box > h1", first=True).text
    #print(articleUrlList.links)

    for url in articleUrlList.links:
        #ignore error url, like /yoyo_liyy/article/details/82762601
        if (checkUrlUserName.upper() not in url.upper()):
            continue
        page = session.get(url)
        if (isPageError(page)):
            print("warn: " + url + " open failed!")
            continue;
        
        titleElement = page.html.find("#mainBox > main > div.blog-content-box > div > div > div.article-title-box > h1", first = True)
        title = titleElement.text
        title = getValidFileName(title)
        print("article: {}".format(title))
        htmlFileName = "{}\\Page{}_{}.html".format(outputDir, i, title);
        contentElement = page.html.find("#content_views", first=True)
        writeHtmlContent(htmlFileName, titleElement, contentElement)
 



