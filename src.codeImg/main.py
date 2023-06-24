# 1. 获取验证码
# 2. 分析验证码
# 3. 放入sessionId中
# 4. 请求接口
# 5. 判断返回值
import io
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
        print("获取图片异常")
    return r


def getCode(codeImg):
    # 创建窗口
    window = Tk()

    # 设置窗口标题
    window.title("展示图片")
    # 创建窗口
    bytes_io = io.BytesIO(codeImg)
    image = Image.open(bytes_io)
    photo = ImageTk.PhotoImage(image)

    # 创建标签并展示图片
    label = Label(window, image=photo)
    label.pack()
    window.after(1000, window.destroy())
    window.mainloop()

    # 识别图片
    ocr = ddddocr.DdddOcr()
    imgCode = ocr.classification(codeImg)
    print("识别出验证码是：" + imgCode)
    return imgCode


def generateReqHeader(code, invitedCode, sessionId):
    import requests

    url = "https://t66y.com/register.php"

    payload = {'reginvcode': invitedCode, 'validate': code, 'action': 'reginvcodeck'}

    headers = {
        'Cookie': "PHPSESSID = " + sessionId,
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print("尝试" + invitedCode + "邀请码...")
    return response


def isAvaliable(response):
    if response.content == "<script language=\"JavaScript1.2\">parent.retmsg_invcode('2');</script>":
        return "2"
    elif response.content == "<script language=\"JavaScript1.2\">parent.retmsg_invcode('1');</script>":
        return "1"
    elif response.content == "<script language=\"JavaScript1.2\">parent.retmsg_invcode('0');</script>":
        return "0"
    else:
        return "-1"


def processOneCode(invitedCode):
    imgRes = getCodeImg()
    imgCode = getCode(imgRes.content)
    sessionId = imgRes.headers.get("Set-Cookie")
    return generateReqHeader(imgCode, invitedCode, sessionId)


if __name__ == '__main__':
    allPossible = string.ascii_lowercase + "0123456789"
    successCodes = []
    # 初始值
    alwaysFailedCodes = []
    originCodes = [
        "8*8c53fa6e4f*274"
    ]
    for originCode in originCodes:
        print("===开始处理" + originCode + "邀请码===")
        possibleCodes = second.formatCombin(originCode)
        failedCodes = []
        for invitedCode in possibleCodes:
            time.sleep(1)
            response = processOneCode(invitedCode)
            # 如果返回值不是200 那么就是验证码识别错误 退出程序
            if response.status_code != 200:
                print("请求错误")
                exit()
            result = isAvaliable(response)
            if result == "0":
                print("尝试" + invitedCode + "邀请码，结果为成功！！！")
                successCodes.append(invitedCode)
                break
            elif result == "2":
                print("尝试" + invitedCode + "邀请码,识别验证码 不正确")
                failedCodes.append(invitedCode)
                continue
            else:
                print("尝试" + invitedCode + "邀请码，结果为：" + result)
                continue
        # 对失败的邀请码进行重试 如果识别结果依然不可以 那么记录
        for failedCode in failedCodes:
            response = processOneCode(invitedCode)
            result = isAvaliable(response)
            if result == "0":
                print("尝试" + invitedCode + "邀请码，结果为成功！！！")
                successCodes.append(invitedCode)
                break
            elif result == "2":
                print("尝试" + invitedCode + "邀请码,识别验证码 依然！不正确")
                failedCodes.append(invitedCode)
                continue
            else:
                print("尝试" + invitedCode + "邀请码，结果为：" + result)
                continue
        # 对失败的邀请码进行重试 如果识别
        print("===结束处理" + originCode + "邀请码===")
    print("程序运行结束,成功邀请码为：" + str(successCodes))
