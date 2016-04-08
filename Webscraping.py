import tkinter as tk
import urllib
import urllib.request
import re
import validators
import random

startAddress = "http://petterssonsblogg.se/"
numberOfAddresses = 10
doneAddresses = 0
width = 1300
height = 800
pendelSize = 500
nextPos = 100

class Internet:
    def __init__(self):
        self.nodes = {}

    def isStored(self, address):
        return (address in self.nodes)

    def getNode(self, address):
        return self.nodes[address]

    def storeNode(self, address, node):
        self.nodes[address] = node

    def countNodes(self):
        return len(self.nodes)

class Node:
    def __init__(self):
        self.inputs = []
        self.outputs = []

def getContentFromSite(link):
    try:
        req = urllib.request.urlretrieve(link)
        try:
            html = open(req[0], encoding='UTF8')
        except:
            return ""
        content = html.read()
        html.close()
        return content
    except:
        return ""

def getLinksFromContent(content):
    return re.findall(r'<a href="(https?.+?)"', content)

def removeHost(list, address):
    links = []
    host = re.findall('https?:\/\/(www\.)?(\w+.\w+).*', address)[0][1]
    for item in list:
        if host not in item:
            links.append(item)
    return links

# Recursive. Collects data for node and put it in the internet
def collectData(address, internet, fromaddress = ""):
    global doneAddresses, numberOfAddresses
    if doneAddresses > numberOfAddresses:
        return
    else:
        doneAddresses+=1

    if not validators.url(address):
        return
    
    content = getContentFromSite(address)

    if content == "":
        return

    links = removeHost(getLinksFromContent(content), address)   

    if internet.isStored(address):
        n = internet.getNode(address)
    else:
        n = Node()
        internet.storeNode(address, n)
    
    if fromaddress != "":
        n.inputs.append(fromaddress)

    for link in links:
        if link not in n.outputs:
            if link not in n.inputs:
                n.outputs.append(link)
                collectData(link, internet, address)
    else:
        return

internet = Internet()
collectData(startAddress, internet)

root = tk.Tk()
root.geometry('{}x{}'.format(width, height))
canvas = tk.Canvas(root, width=width, height=height, borderwidth=0, highlightthickness=0, bg="white")
canvas.grid()

def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
tk.Canvas.create_circle = _create_circle

xNext = width / 2 - pendelSize
yNext = height / 2 - pendelSize
canvas.create_circle(width/2, height/2, 30, fill="black", outline="#DDD", width=3)
canvas.create_text(width/2+15,height/2-40,text=startAddress)
for (url, node) in internet.nodes.items():
    canvas.create_circle(xNext, yNext, 20, fill="blue", outline="#DDD", width=3)
    canvas.create_text(xNext+15,yNext-40,text=url)
    xNext += nextPos
    yNext += nextPos
    #for innerUrl in node.outputs:
    #    canvas.create_circle(xval, yval, 10, fill="gray", outline="#DDD", width=3)
    #    canvas.create_text(xval+5,yval-40,text=innerUrl)

#canvas.create_circle(100, 120, 50, fill="blue", outline="#DDD", width=4)
#canvas.create_circle(150, 40, 20, fill="#BBB", outline="")
#canvas.create_line(20, 20, 500, 500)

root.wm_title("Circles and Arcs")
root.mainloop()