# 1. 获取验证码
# 2. 分析验证码
# 3. 放入sessionId中
# 4. 请求接口
# 5. 判断返回值
import io
import random
import string
import time
from tkinter import Tk, Label

import ddddocr
import requests as requests
from PIL import ImageTk, Image
import second


def getCodeImg():
    url = "https://t66y.com/require/codeimg.php?0.8496717166104992"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"
    }
    kw = {'s': 'python 教程'}

    r = requests.get(url, params=kw, headers=headers)
    if r.status_code != 200:
        raise Exception("获取图片异常")
    return r


def getCode(codeImg):
    # # 创建窗口
    # window = Tk()
    #
    # # 设置窗口标题
    # window.title("展示图片")
    # # 创建窗口
    # bytes_io = io.BytesIO(codeImg)
    # image = Image.open(bytes_io)
    # photo = ImageTk.PhotoImage(image)
    #
    # # 创建标签并展示图片
    # label = Label(window, image=photo)
    # label.pack()
    # window.after(1000, window.destroy())
    # window.mainloop()

    # 识别图片
    ocr = ddddocr.DdddOcr()
    imgCode = ocr.classification(codeImg)
    print("识别出验证码是：" + imgCode)
    return imgCode





def isAvaliable(response):
    if response.text == "<script language=\"JavaScript1.2\">parent.retmsg_invcode('2');</script>":
        return "2"
    elif response.text == "<script language=\"JavaScript1.2\">parent.retmsg_invcode('1');</script>":
        return "1"
    elif response.text == "<script language=\"JavaScript1.2\">parent.retmsg_invcode('0');</script>":
        return "0"
    else:
        return "-1"


def processOneCode(invitedCode):
    imgRes = getCodeImg()
    imgCode = getCode(imgRes.content)
    sessionId = imgRes.headers.get("Set-Cookie")
    agent_list = [
        "Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; Nexus S Build/GRK39F) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        "Avant Browser/1.2.789rel1 (http://www.avantbrowser.com)",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.5 (KHTML, like Gecko) Chrome/4.0.249.0 Safari/532.5",
        "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.310.0 Safari/532.9",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.514.0 Safari/534.7",
        "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/9.0.601.0 Safari/534.14",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/10.0.601.0 Safari/534.14",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.27 (KHTML, like Gecko) Chrome/12.0.712.0 Safari/534.27",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.24 Safari/535.1",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.120 Safari/535.2",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7",
        "Mozilla/5.0 (Windows; U; Windows NT 6.0 x64; en-US; rv:1.9pre) Gecko/2008072421 Minefield/3.0.2pre",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.10) Gecko/2009042316 Firefox/3.0.10"
    ]
    url = "https://t66y.com/register.php"

    payload = {'reginvcode': invitedCode, 'validate': imgCode, 'action': 'reginvcodeck'}

    headers = {
        'Cookie': sessionId, 'User-Agent': random.choice(agent_list)

    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print("尝试" + invitedCode + "邀请码...")
    return response


if __name__ == '__main__':
    allPossible = string.ascii_lowercase + "0123456789"
    successCodes = []
    # 初始值
    alwaysFailedCodes = []
    originCodes = [
        "8*8c53fa6e4f*274"
    ]
    failedCodes = []

    for originCode in originCodes:
        print("===开始处理" + originCode + "邀请码===")
        possibleCodes = second.formatCombin(originCode)
        for invitedCode in possibleCodes:
            time.sleep(random.uniform(3, 5))
            result = ""
            i = 0
            # 只要结果不是0和1 就一直循环
            while result != "1" and result != "0":
                try:
                    response = processOneCode(invitedCode)
                except Exception as e:
                    print(e)
                    continue
                result = isAvaliable(response)
                i += 1
                if i > 10:
                    print("，跳过该邀请码")
                    break
            if result == "0":
                print("成功！！！")
                successCodes.append(invitedCode)
                break
            if result == "1":
                print("结果为已经被使用")
                continue
            elif result == "2":
                print("重试次数达到限制 跳过 目前错误的验证码为" + failedCodes.__str__())
                failedCodes.append(invitedCode)
                continue
        # 对失败的邀请码进行重试 如果识别
        print("===结束处理" + originCode + "邀请码===")
    print("程序运行结束,成功邀请码为：" + str(successCodes) + ",失败邀请码为：" + str(failedCodes))
