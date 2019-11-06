import subprocess
# from scrapy import cmdline
import time
subprocess.run("echo 开始爬取qq", shell=True)
subprocess.run("scrapy crawl qq", shell=True)
subprocess.run("echo 开始爬取163", shell=True)
subprocess.run("scrapy crawl 163", shell=True)
subprocess.run("echo 开始爬取sohu", shell=True)
subprocess.run("scrapy crawl sohu", shell=True)
subprocess.run("echo 开始爬取sina", shell=True)
subprocess.run("scrapy crawl sina", shell=True)
# print("开始爬取qq")  # 没用，好像只能执行第一个，接下去不能继续执行，而且print还是最后输出
# cmdline.execute(['scrapy', 'crawl', 'qq'])
# print("开始爬取163")
# cmdline.execute(['scrapy', 'crawl', '163'])
# print("开始爬取sohu")
# cmdline.execute(['scrapy', 'crawl', 'sohu'])
# print("开始爬取sina")
# cmdline.execute(['scrapy', 'crawl', 'sina'])
print(time.strftime("%Y%m%d %H:%M:%S", time.localtime()) + " 执行了爬取")  # crontab有自动发邮件的功能，但MAILTO只适用于/etc/crontab中执行的脚本或命令
# 会一条接一条执行，不会并行
# 数据存在MongoDB和存储组API
