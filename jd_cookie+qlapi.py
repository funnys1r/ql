from selenium import webdriver
import requests
import json

# 定义一个函数，用来获取访问令牌
def get_token():
    url = 'http://192.168.100.1:5700/open/auth/token?client_id=A__v62Lb9S3D&client_secret=COO_2elt4GtPq3wAOYPHauaP&'  #http://你的青龙后台:端口（默认5700）去应用里面设置中注册一个,client_id=你的CLIENT CLIENT_SECRET=你的CLIENT_SECRET
    response = requests.get(url)
    data = json.loads(response.content.decode()) 
    return data['data']['token']

# 获取访问令牌
token = get_token()

# 构造请求头，携带访问令牌
headers = {
    'Authorization': 'Bearer ' + token,
}

# 获取环境变量详情
url1 = 'http://192.168.100.1:5700/open/envs'#改为http://你的青龙后台:端口（默认5700）/open/envs
res = requests.get(url1, headers=headers) 
envs = json.load
print("所有的环境变量如下：")
for env in envs["data"]: #遍历所有的环境变量
    print("名称：", env["name"])
    print("值：", env["value"])
    print("备注：", env["remarks"])
    print("id：", env["id"])
    print("----------")

# 提示要更新的变量
remark = input("请输入要更新的变量的备注值：") #让用户输入一个备注值
for env in envs["data"]: #遍历所有的环境变量
    if env["remarks"] == remark: #如果找到了匹配的备注值
        print("找到了要更新的变量，它的详情如下：")
        print("名称：", env["name"])
        print("值：", env["value"])
        print("备注：", env["remarks"])
        print("id：", env["id"])
        print("----------")
        # 询问是否要更新
        confirm = input("是否要更新这个变量的值？按回车继续，输入其他内容取消：") #让用户确认是否要更新
        if confirm == "": #如果用户按回车继续
            # 使用selenium模块来模拟浏览器操作，登录京东网站，然后获取cookie
            print("使用说明：必须安装chrome浏览器否则不能使用本脚本")
            print("弹出浏览器窗口请登录您的账户，脚本会为您自动抓取cookie！")
            url = "https://plogin.m.jd.com/login/login"

            drive = webdriver.Chrome()
            drive.get(url)
            input("成功登录后请按回车继续:")
            drive.refresh()
            getcookie = drive.get_cookies()
            for cookie in getcookie:
                if cookie['name'] == 'pt_key':
                    pt_key = cookie['value']
                elif cookie['name'] == 'pt_pin':
                    pt_pin = cookie['value']

            pt_key = 'pt_key' + '=' + pt_key + ';'
            pt_pin = 'pt_pin' + '=' + pt_pin + ';'
            print("\n抓取成功！您的cookie:",pt_key, pt_pin)

            # 关闭浏览器窗口
            drive.close()

            # 更新请求头中的cookie，把最新的cookie放在请求头中
            headers['Cookie'] = pt_key + pt_pin

            # 更新指定的环境变量的值，把京东的cookie作为环境变量的值
            url2 = 'http://192.168.100.1:5700/open/envs/'#改为http://你的青龙后台:端口（默认5700）/open/envs
            data ={
            "value": pt_key + pt_pin, #把京东的cookie作为value的内容
            "name": env["name"], #保持其他属性不变
            "remarks": env["remarks"],
            "id": env["id"],}
            response = requests.put(url2, headers=headers, json=data) #发送put请求，更新服务器上的资源
            print("更新结果如下：")
            print("状态码：", response.status_code) #打印响应的状态码
            print("内容：", response.content.decode()) #打印响应的内容
            break #跳出循环
        else: #如果用户输入其他内容取消
            print("取消更新，程序结束。")
            break #跳出循环
else: #如果没有找到匹配的备注值
    print("没有找到要更新的变量，请检查你的输入是否正确。")
