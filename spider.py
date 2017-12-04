import requests
import re
import json
from multiprocessing import Pool
from requests.exceptions import RequestException\

def get_one_page(url):
    try:
        headers={'User-Agent':'Mozilla/5.0'}
        r=requests.get(url,headers=headers)
        r.encoding=r.apparent_encoding
        r.raise_for_status()
        #print(r.text)
        return r.text

    except requests.exceptions.RequestException:
        print('requests.exceptions.RequestException')
        return None


def parse_one_page(html):
    pattern=re.compile('<dd>.*?<i class="board-index.*?">(\d+)</i>'
                       +'.*?title="(.*?)".*?'
                       +'<img data-src="(.*?)".*?'
                       + 'class="star">(.*?)</p>.*?'
                       + 'releasetime">(.*?)</p>'
                       + '.*?integer">(\d+.)</i>'
                       + '.*?fraction">(\d).*?</dd>'
                       ,re.S)
    items=pattern.findall(html)

    for item in items:
        yield {
            'sequence':item[0],
            'title':item[1],
            'picture':item[2],
            'actors':item[3].strip()[3:],
            'date':item[4][5:],
            'score':item[5]+item[6]}


def write_to_file(content):
    with open('movie.txt','a',encoding='utf-8') as f:
        jsondumps=json.dumps(content,ensure_ascii=False)
        #print(jsondumps)
        f.write(jsondumps+'\n')
    f.close()


def main(i):
    urlbasic='http://maoyan.com/board/4?offset='
    url=urlbasic+str(10*i)
    print(url)
    html=get_one_page(url)
    content=parse_one_page(html)
    #print(type(content))
    for i in [0,1,2,]:
        write_to_file(next(content))




if __name__ == '__main__':
    pool=Pool()
    pool.map(main, [i for i in range(0, 11)])
