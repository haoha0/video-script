import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import re
import subprocess

def load_and_play_video(driver, url, playtime, wait):
    """加载并播放视频，然后在随机时间后暂停。"""
    input_box = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "form-control")))
    input_box.clear()
    input_box.send_keys(url)
    print(f"URL {url} loaded into input box.")

    # 点击加载并播放视频（自动播放）
    load_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.container > div:nth-child(2) > div.input-group > span > button.btn.btn-primary")))
    load_button.click()
    print("Load button clicked.")

    # 手动播放
    # time.sleep(1)
    time.sleep(1) # for windows
    # haohao 7.11 测试发现不加timesleep也是可以正常触发播放？还是加1s比较稳定
    # play_button = wait.until(EC.element_to_be_clickable((By.ID, "iconPlayPause")))
    # play_button.click()
    # print("Play button clicked.")

    # 播放时间，设置为3min
    # playtime = 1 * 60
    print("Play video for {} min.".format(playtime / 60))
    time.sleep(playtime)

def save_logs_to_file(driver, folder_name, filename):
    """获取浏览器日志并保存到文件。"""
    logs = driver.get_log('browser')
    # 创建文件夹
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    filepath = os.path.join(folder_name, filename)
    with open(filepath, "a") as file:
        for log in logs:
            # file.write(f"{log['timestamp']} - {log['level']} - {log['message']}\n")
            file.write(f"{log['timestamp']} - {log['message']}\n")
    print(f"Logs saved to {filepath}.")

# 主程序
options = webdriver.EdgeOptions()
# options.use_chromium = True
options.set_capability('ms:loggingPrefs', {'browser': 'ALL'})
options.add_experimental_option("detach", True)
options.add_argument('--ignore-certificate-errors') # for windows error
options.add_experimental_option('excludeSwitches', ['enable-logging']) # for windows error
driver = webdriver.Edge(options=options)
# TODO:使用指定路径的driver
# driver_path = '/Users/liuwenhao/Downloads/edgedriver_mac64_m1/msedgedriver'
# driver = webdriver.Edge(service=webdriver.EdgeService(driver_path), options=options)

driver.get('http://localhost:3000/samples/dash-if-reference-player/index.html')

# for windows 消除个性化推荐弹窗
# time.sleep(10)
# driver.refresh()

# 视频URL列表
video_urls = [
    'http://123.57.76.186/BV1JP411D76R.mpd',
    'http://123.57.76.186/BV1Wf4y1n7Pc.mpd',
    'http://123.57.76.186/BV1CM4m1k7bs.mpd',
    'http://123.57.76.186/BV1tc411M7JF.mpd',
    'http://123.57.76.186/BV1pn4y197hv.mpd',
    'http://123.57.76.186/BV16b421e7L1.mpd',
    'http://123.57.76.186/BV1UB4y1N7zB.mpd',
    'http://123.57.76.186/BV1At421t7z4.mpd',
    'http://123.57.76.186/BV1te4y1E7K5.mpd',
    'http://123.57.76.186/BV1VG411B7RP.mpd'
]

# test
video_urls = [
    # 'https://dash.akamaized.net/akamai/bbb_30fps/bbb_30fps.mpd',
    # 'https://dash.akamaized.net/digitalprimates/fraunhofer/480p_video/heaac_2_0_with_video/Sintel/sintel_480p_heaac2_0.mpd',
    # 'https://dash.akamaized.net/akamai/bbb_30fps/bbb_30fps.mpd',
    # 'http://39.102.209.114/BV1P44y1F72Z.mpd',
    'http://123.56.126.80/BV1P44y1F72Z.mpd',
    # 'http://123.56.126.80/BV1jE411k76o.mpd'
]

# bandwidths = ['100kbit', '300kbit', '500kbit', '1mbit', '2mbit', '3mbit', '4mbit', '5mbit', 'xmbit']
# 其实在这里设置bandwidths没啥用，除非能通过这里控制远程服务器进行带宽切换 TODO

wait = WebDriverWait(driver, 10)
try:
    # 下面三个变量需要根据实际情况设置
    logs_folder_name = "0721_original_logs" # 输出logs文件夹
    pcaps_folder_name = "0721_pcaps"    # 输出pcaps文件夹
    playtime = 30  # 播放时间
    bandwidth = '300kbit'  # 带宽

    # 不存在则创建
    if not os.path.exists(logs_folder_name):
        os.makedirs(logs_folder_name)

    if not os.path.exists(pcaps_folder_name):
        os.makedirs(pcaps_folder_name)

    # 顺序播放视频
    pattern = r'\/(BV.*?)\.mpd' 
    for video in video_urls:
        # 获取video号
        match = re.search(pattern, video)
        video_number = match.group(1)
        print("Video number: ", video_number)

        # 启动wireshark
        # pcap_file_name = "pcap_" + video_number + f"_{playtime}s.pcap"
        pcap_file_name = "pcap_" + video_number + f"_{bandwidth}_{playtime}s.pcap"
        pcap_file_path = os.path.join(pcaps_folder_name, pcap_file_name)
        tshark_command = [  
            'E:/Wireshark/tshark.exe',  # E:\\Wireshark\\tshark.exe
            '-i', '以太网',  # 以太网接口名称或编号  
            # '-w', video_number + '.pcap',
            '-w', pcap_file_path,
            '-f', 'host 123.56.126.80',
            # '-a', 'duration:60'  # 捕获持续时间
        ]
        process = subprocess.Popen(tshark_command)
        print("Wireshark started.")

        # 播放视频
        load_and_play_video(driver, video, playtime, wait)

        # 关闭wireshark
        process.terminate()
        print("Pcaps saved to {}.".format(pcap_file_path))
        print("Wireshark terminated.")

        # 7.21 实现多视频自动播放并记录logs
        # filename = "log_" + video_number + f"_{playtime}s.txt"
        filename = "log_" + video_number + f"_{bandwidth}_{playtime}s.txt"

        save_logs_to_file(driver, logs_folder_name, filename)
        print("Video {} finished.".format(video_number))

        # 刷新页面
        driver.refresh()
        time.sleep(2)

    # folder_name = "original_logs"
    # folder_name = "0721_original_logs"
    # filename = "log_" + time.strftime("%Y%m%d-%H%M") + f"_300bit.txt"
    # save_logs_to_file(driver, folder_name, filename)

except Exception as e:
    print("An error occurred:")
    traceback.print_exc()

driver.quit()
