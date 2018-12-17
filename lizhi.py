import urllib.request
import urllib.parse
import re
'''
获取图片是出现问题没有解决：
有的励志内容中出现两张图片，如果采用下边方式获取图片，
会使为最后一张图片在固定位置上出现两次

解决方法，并未附加代码
1.通过正则匹配，匹配出img标签的个数，通过个数1或2进行判断
一个则使用下边的方法
两个，第一个使用正则的非贪婪匹配，第二个使用正则的贪婪匹配，最后进行url的拼接
2.根据标签的内容进行匹配
'''

def handle_request(url, page=None):
    if page != None:
        url = url + str(page) + '.html'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; \
            x64) AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/70.0.3538.102 Safari/537.36'
    }
    request = urllib.request.Request(url=url, headers=headers)
    return request


def get_img(text):
    #获取图片
    pat = re.compile(r'src="(.*?)"')
    img = pat.findall(text)
    for img1 in img:
        img_url = 'src=' + '"' + 'http://www.yikexun.cn' + img1 + '"'
        text = pat.sub(img_url, text)
    return text


def get_text(a_href):
    # 调用函数构建请求对象
    request = handle_request(a_href)
    # 发送请求获取响应
    content = urllib.request.urlopen(request).read().decode()
    # 解析内容
    pattern = re.compile(r'<div class="neirong">(.*?)</div>', re.S)
    lt = pattern.findall(content)

    # print(lt)
    # exit()
    text = lt[0]
    # 将内容里面所有图片标签全部清空
    # pat = re.compile(r'<img .*?>')
    # print(text)
    # exit()  # 强制退出
    img_text = get_img(text)
    return img_text


def parse_content(content):
    pattern = re.compile(r'<h3><a href="(/lizhi/qianming/\d+\.html)">(.*?)</a></h3>')
    lt = pattern.findall(content)
    # print(lt)
    for href_title in lt:
        # 获取连接内容
        a_href = 'http://www.yikexun.cn' + href_title[0]
        # 获取标题
        title = href_title[-1]
        # 向a_href发送请求，获取响应内容
        text = get_text(a_href)
        string = '<h1>%s</h1>%s' % (title, text)
        # print(string)
        with open('lizhi.html', 'a', encoding='utf-8') as fp:
            fp.write(string)
        # exit()


def main():
    url = 'http://www.yikexun.cn/lizhi/qianming/list_50_'
    start_page = int(input("请输入起始页"))
    end_page = int(input("请输入结束页"))
    for page in range(start_page, end_page + 1):
        request = handle_request(url, page)
        content = urllib.request.urlopen(request).read().decode()
        # print(content)
        parse_content(content)


if __name__ == '__main__':
    main()
