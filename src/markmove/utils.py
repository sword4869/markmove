import re
import requests
import os


def getUrl(img_content, filter_suffix):
    # 括号内部和去掉括号
    img_content = re.findall('\(.*\)', img_content)[0]
    img_content = img_content[1:-1]
    
    if filter_suffix == None:
        return img_content

    # 截取到图片后缀格式
    for suffix in filter_suffix:
        suffix_index = img_content.find(suffix)
        # 找到了
        if suffix_index != -1:
            return img_content[0:suffix_index] + suffix
    return None

def getUrlList(line, filter_suffix = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp']):
    '''
    获取一行中的图片链接
    :param line: 一行字符串
    :param filter_suffix: 过滤后缀
    :return: 图片链接列表

    例子：
    line = '   ![xxx](fdf)  '
    print(getUrlList(line, filter_suffix=None))     # ['fdf']
    line = '   ![xxx](fdf.png)  '
    print(getUrlList(line))                         # ['fdf.png']
    '''
    url_list = []

    # 判读是否包含`![]()`的格式，用正则表达式
    regex = '!\[.*\]\(.*\)'
    img_contents = re.findall(regex, line)
    # 有图片，但是不止一张
    if(len(img_contents) > 1):
        print('多张图片')
        for img_content in img_contents:
            url = getUrl(img_content, filter_suffix)
            if(url):
                url_list.append(url)
    # 只有一张图片
    elif(len(img_contents) == 1):
        url = getUrl(img_contents[0], filter_suffix)
        if(url):
            url_list.append(url)
    return url_list

def downloadImage(url, imageNameSave):
    '''
    下载图片，并存储在image文件夹下
    :param url: 图片链接
    :param imageNameSave: 图片保存路径
    :return: True/False

    例子：
    url = 'https://i0.hdslb.com/bfs/activity-plat/25830752a052f1c8861e26c8e96d46cdf7f53e02.jpg@640w_200h_!web-video-activity-cover.webp'
    imageNameSave = './images/xxx.png'
    print(downloadImage(url, imageNameSave))     # ![xxx.png](./images/xxx.png)
    '''
    print('download', url, imageNameSave)
  
    headers = { 
        'authority': 'api.bilibili.com',
        'method': 'GET',
        'path': '/x/note/image?image_id=410836',
        'scheme': 'https',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Cookie': "buvid3=0FC06167-36B3-EE32-0F39-C7642B64657C59734infoc; b_nut=1699194959; i-wanna-go-back=-1; b_ut=7; _uuid=1B7D3E43-110B9-5946-C3AB-23663A835CE360507infoc; enable_web_push=DISABLE; buvid4=F0CD99D4-A60D-69E7-7220-C20277EE5FA660545-023110522-Hf%2FkEx03jN3mw0lhNE2EUw%3D%3D; header_theme_version=CLOSE; DedeUserID=12619074; DedeUserID__ckMd5=710bce50cdb3d44e; rpdid=|(JYYu~kk|)l0J'uYmmklRu)Y; hit-dyn-v2=1; LIVE_BUVID=AUTO8017000524221749; buvid_fp_plain=undefined; CURRENT_FNVAL=4048; fingerprint=47ab71301101c7b8fc44f16c032aa008; is-2022-channel=1; home_feed_column=5; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDQ2ODA4NjgsImlhdCI6MTcwNDQyMTYwOCwicGx0IjotMX0.i55Okyos2CaRv2CEyJAU1RUyWRfBmyWs-_4JUA1DAns; bili_ticket_expires=1704680808; CURRENT_QUALITY=80; SESSDATA=473fa5ec%2C1720086183%2C2fe8c%2A12CjAWBSyUFaERp4fYAfeXU-BqlhR1nWWy4f9h-qlF8bnEDRw_YydSEwq9NPnJG5nIHB8SVmVDUGJDYjR0YmJsT1p6U2pQYWtab0xENm9obml1eFRTRWNITjRtM1kzMUw3ek13eEFYWVpJdmtvbndMVXFJMzFfVlc2LWF2MkVDY3A5Rlhsa0d2QUhnIIEC; bili_jct=2816abb5c7f9c8e29c047369182e8bb9; sid=6og4nl5u; buvid_fp=47ab71301101c7b8fc44f16c032aa008; browser_resolution=1656-883; bp_video_offset_12619074=883477586014896136; PVID=1; b_lsid=9103107242_18CDEEA66A7; bsource=search_bing",
        'Dnt': '1',
        'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Microsoft Edge";v="120"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'
    }
    r = requests.get(url, headers=headers)
    print(r)
    # 保存图片
    with open(imageNameSave, 'wb') as f:
        # 判断状态码
        if r.status_code == 404:
            print(f'{r.status_code}.status_code = {url}')
            return False
        # 写入数据
        else:
            f.write(r.content)
    # 返回markdown中图片路径
    return True