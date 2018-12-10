#crawMyCsdnBlog.py
from requests_html import HTMLSession
import os
import sys
import re
import mypub

session = HTMLSession()

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

imgDir = outputDir + "/" + "img"
if not os.path.exists(imgDir):
    os.mkdir(imgDir)


#save img file to local directory and return the replace html text
def getExchangedText(contentElement):
    htmlText = contentElement.html
    for img in contentElement.find("img"):
        #mypub.printVar(img.attrs["src"])
        try:
            url = img.attrs["src"]
            imgName = url[url.rindex("/") + 1:]
            page = session.get(url)
            page.raise_for_status()
            localAddr = imgDir + "/" + imgName
            mypub.writeBinFile(localAddr, page.content)
            #mypub.printVar(localAddr)
            htmlText = htmlText.replace(url, "img/" + imgName)
        except:
            continue
    return htmlText
#write content to html file
def writeHtmlContent(fileName, titleElement, contentElement):
    c  = '<html lang="zh-CN">\r\n'
    c += '  <head>\r\n'
    c += '    <meta http-equiv="content-type" content="text/html; charset=utf-8">\r\n'
    c += '    <title>{}</title>\r\n'.format(titleElement.text)
    c += '  </head>\r\n'
    c += '  <body>\r\n'
    c += ('    <div class="article-title-box">{}</div>\r\n'.format(titleElement.html))
    c += getExchangedText(contentElement)
    c += '\r\n  </body>\r\n'
    c += '</html>\r\n'
    mypub.writeTextFile(fileName, c)

#repalce specail charactor
def getValidFileName(fileName):
    fileName = re.sub(r'[ <>/:*?"|\\-]', "_", fileName) #replace special charactor to '_'
    fileName = re.sub('__+', "_", fileName)              #replace duplicate '_'
    return fileName

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
        break
    
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
        htmlFileName = os.path.abspath("{}/Page{}_{}.html".format(outputDir, i, title));
        #mypub.outputVar(htmlFileName)
        contentElement = page.html.find("#content_views", first=True)
        writeHtmlContent(htmlFileName, titleElement, contentElement)
 



