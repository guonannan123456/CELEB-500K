import os
import multiprocessing
from PIL import Image

def ExtractUrls(rootDir,txt):
    pos1=0
    pos2=-6
    txt_path = os.path.join(rootDir, txt) 
    data = open(txt_path, 'rb')
    for line in data:
        line = line.decode('utf-8')
    urls = []
    while(pos1 != -1 and line!=[]):
        line = line[pos2+6:]
        try:
            pos1 = line.index("\"ou\"")
        except ValueError:
            break
        pos2 = line.index("\"ow\"")
        urls.append(line[pos1+6:pos2-2])
    return urls
def Download(name, url):
    url_no = os.system('wget --no-check-certificate -O %s -T 30 -t 3 %s ' % (name, url))
    if url_no != 0:
	url1 = url.replace('https','http')
	os.system('wget --no-check-certificate -O %s -T 30 -t 3 %s ' % (name, url1))

    try:
        im = Image.open(name)
	im=im.convert('RGB')
        im.save(name)
    except:
	os.remove(name)
	

def MultiRunWrapper(args):
    return Download(*args) 

if __name__ == '__main__':
    rootDir = 'urls-357488-40w/'
    saveDir = 'imgs-357488-40w/'
    url_files = os.listdir(rootDir)
    #print(len(url_files))
    countExist=0
    countNotDownload=0
    for name in url_files:
	nameList = []
        folder_path = os.path.join(saveDir, name[:-6])
        cnt = int(name[-5])*100
        if not os.path.isdir(folder_path):
            os.mkdir(folder_path)
        urls = ExtractUrls(rootDir,name)
	
        for j in range(len(urls)):
            nameList.append(os.path.join(folder_path, ('%d.jpg' % (cnt+j))))
	print len(nameList)
        inputList = [(nameList[i], urls[i]) for i in range(len(nameList))]
	print inputList	
        pool = multiprocessing.Pool(12)
        pool.map(MultiRunWrapper, inputList)
        pool.close()
        pool.join()
