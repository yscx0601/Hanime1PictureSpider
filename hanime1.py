import urllib.request, urllib.error, re, os, time
from lxml import etree

# 目标网址
base_url = 'https://hanime1.me/search?genre=%E8%A3%8F%E7%95%AA'

# 用正则替换掉不合法的字符
def sanitize_filename(filename):
    # 替换掉特殊字符，替换为下划线
    return re.sub(r'[\\/*?:"<>|]', "_", filename)

# 获取源码
def getContent(page):
    # 请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
    }

    url = base_url + '&page=' + str(page)

    request = urllib.request.Request(url = url, headers = headers)

    response = urllib.request.urlopen(request)

    content = response.read().decode('utf-8')

    return content



if __name__ == '__main__':
        # 获取1~10页的网页源码
        for page in range(1, 11):
            content = getContent(page)

            # 爬取标题和图片
            tree = etree.HTML(content)
            title_list = tree.xpath('//div//a/div/div/text()')
            img_list = tree.xpath('//div//a/div/img[@style="border-radius: 3px"]/@src')

            # 下载到本地
            # 创建目录
            save_dir = './hanime1'
            os.makedirs(save_dir, exist_ok=True)

            for i in range(len(title_list)):
                # 清理标题中的非法字符
                sanitized_title = sanitize_filename(title_list[i])
                # 拼接合法的文件路径
                filepath = os.path.join(save_dir, sanitized_title + '.jpg')

                try:
                    urllib.request.urlretrieve(url=img_list[i], filename=filepath)
                except urllib.error.URLError:
                    print("Error downloading " + sanitized_title)

                time.sleep(0.5)

