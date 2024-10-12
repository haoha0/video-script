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
    # time.sleep(1) # 等待加载出播放按钮
    # haohao 7.11 测试发现不加timesleep也是可以正常触发播放？还是加1s比较稳定
    # play_button = wait.until(EC.element_to_be_clickable((By.ID, "iconPlayPause")))
    # play_button.click()
    # print("Play button clicked.")

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

# 打开视频播放器页面
# TODO:使用指定路径的driver
# driver_path = '/Users/liuwenhao/Downloads/edgedriver_mac64_m1/msedgedriver'
# driver = webdriver.Edge(service=webdriver.EdgeService(driver_path), options=options)
# driver = webdriver.Edge(options=options)
# driver.get('http://localhost:3000/samples/dash-if-reference-player/index.html')
# wait = WebDriverWait(driver, 10)

####################### 播放参数配置 #######################
# 根据实际情况设置
# logs_folder_name = "../../pcap_data/0801_ground_logs/videos_100kbit/"    # 输出logs文件夹
# pcaps_folder_name = "../../pcap_data/0801_ground_pcaps/videos_100kbit/"    # 输出pcaps文件夹
logs_folder_name = "../../output_data/plotinus_logs/1005_logs_startup/videos_100kbit/"    # 输出logs文件夹
pcaps_folder_name = "../../output_data/plotinus_pcaps/1005_pcaps_startup/videos_100kbit/"    # 输出pcaps文件夹
# videos_500kbit

server_ip = "10.18.155.4"  # 服务器IP
bandwidth = '100kbit'   # 服务器设置的带宽限制（需要去服务器使用tc进行限制）
playtime = 30   # 播放时间
# bandwidths = ['100kbit', '200kbit', '300kbit', '400kbit', '500kbit', 'xbit']
# TODO
# 考虑是否可以控制远程服务器进行带宽动态切换，从而可以撰写嵌套循环实现多个带宽自动播放 TODO

# 视频URL列表
video_urls = [
    # videos1
    f'http://{server_ip}/BV1zi421S7QJ.mpd',
    f'http://{server_ip}/BV1Tx411W7eg.mpd',
    f'http://{server_ip}/BV1pz421a7oC.mpd',
    f'http://{server_ip}/BV14m421N7Q5.mpd',
    f'http://{server_ip}/BV12A4y1o7Gg.mpd',
    f'http://{server_ip}/BV1fT421v7m6.mpd',
    f'http://{server_ip}/BV16Y4y13724.mpd',
    f'http://{server_ip}/BV1Gx411y749.mpd',
    f'http://{server_ip}/BV1Xi4y187MR.mpd',
    f'http://{server_ip}/BV1P44y1F72Z.mpd',

    f'http://{server_ip}/BV1j7421o7wd.mpd',
    f'http://{server_ip}/BV1Br421w7Pz.mpd',
    f'http://{server_ip}/BV1eU4y1Y7Vz.mpd',
    f'http://{server_ip}/BV1ai421D7yu.mpd',
    f'http://{server_ip}/BV1ks411W7r5.mpd',
    f'http://{server_ip}/BV1Ss421g75Y.mpd',
    f'http://{server_ip}/BV1At421t7z4.mpd',
    f'http://{server_ip}/BV16W4y1E7ou.mpd',
    f'http://{server_ip}/BV1nF411Z7Lp.mpd',
    f'http://{server_ip}/BV1sm421W7Yw.mpd',

    f'http://{server_ip}/BV1nm421K78H.mpd',
    f'http://{server_ip}/BV12w4m19781.mpd',
    f'http://{server_ip}/BV1xJ4m1g71P.mpd',
    f'http://{server_ip}/BV1fx41137RR.mpd',
    f'http://{server_ip}/BV1tX4y1q7nT.mpd',
    f'http://{server_ip}/BV1GT4y1e7VM.mpd',
    f'http://{server_ip}/BV1Cn4y1R7GB.mpd',
    f'http://{server_ip}/BV1bM411o7bx.mpd',
    f'http://{server_ip}/BV1Df4y1s7rG.mpd',
    f'http://{server_ip}/BV16b421e7L1.mpd',

    f'http://{server_ip}/BV12k4y1X7XL.mpd',
    f'http://{server_ip}/BV1EY411d77Z.mpd',
    f'http://{server_ip}/BV1jJ4m1G73a.mpd',
    f'http://{server_ip}/BV1Mr421p7W4.mpd',
    f'http://{server_ip}/BV1tc411M7JF.mpd',
    f'http://{server_ip}/BV17x4y177kS.mpd',
    f'http://{server_ip}/BV1mW421A7nM.mpd',
    f'http://{server_ip}/BV1qv4y1p7YN.mpd',
    f'http://{server_ip}/BV1Wf4y1n7Pc.mpd',
    f'http://{server_ip}/BV1Am421K7LM.mpd',

    f'http://{server_ip}/BV1rj411J7sN.mpd',
    f'http://{server_ip}/BV1Xw4m1Q7p2.mpd',
    f'http://{server_ip}/BV1uD421g7Qk.mpd',
    f'http://{server_ip}/BV1bT4y1871D.mpd',
    f'http://{server_ip}/BV1Vm421T7zL.mpd',
    f'http://{server_ip}/BV1a24y1j74Z.mpd',
    f'http://{server_ip}/BV1EL4y187ZP.mpd',
    f'http://{server_ip}/BV1ED421A7Ue.mpd',
    f'http://{server_ip}/BV1Dr421u7fQ.mpd',
    f'http://{server_ip}/BV1kV4y1r7j5.mpd',

    # f'http://{server_ip}/BV1oZ4y1X7tP.mpd',
    # f'http://{server_ip}/BV1jE411k76o.mpd',
    # f'http://{server_ip}/BV1ur421E7sn.mpd',
    # f'http://{server_ip}/BV1sR4y1e7SG.mpd',
    # f'http://{server_ip}/BV1jb421B7jP.mpd',
    # f'http://{server_ip}/BV1vi4y1N7f5.mpd',
    # f'http://{server_ip}/BV1Fu411o7o1.mpd',
    # f'http://{server_ip}/BV1mm421N7b1.mpd',
    # f'http://{server_ip}/BV1BV4y1T769.mpd',
    # f'http://{server_ip}/BV1Kt421M7Yz.mpd',
]

# test
# video_urls = [
#     # 'https://dash.akamaized.net/akamai/bbb_30fps/bbb_30fps.mpd',
#     # 'https://dash.akamaized.net/digitalprimates/fraunhofer/480p_video/heaac_2_0_with_video/Sintel/sintel_480p_heaac2_0.mpd',
#     f'http://{server_ip}/BV1P44y1F72Z.mpd',
#     f'http://{server_ip}/BV1jE411k76o.mpd'
# ]

try:
    # 检查输出文件夹
    if not os.path.exists(logs_folder_name):
        os.makedirs(logs_folder_name)
        print("Logs folder created.")
    if not os.path.exists(pcaps_folder_name):
        os.makedirs(pcaps_folder_name)
        print("Pcaps folder created.")

    # 顺序播放视频
    pattern = r'\/(BV.*?)\.mpd'
    for video in video_urls:
        # 获取video号
        match = re.search(pattern, video)
        video_number = match.group(1)
        print("Video number: ", video_number)

        # 打开浏览器
        driver = webdriver.Edge(options=options)
        driver.get('http://localhost:3000/samples/dash-if-reference-player/index.html')
        wait = WebDriverWait(driver, 10)

        # 启动wireshark
        offset_time = 3
        pcap_file_name = "pcap_" + video_number + f"_{bandwidth}_{playtime}s.pcap"
        pcap_file_path = os.path.join(pcaps_folder_name, pcap_file_name)
        tshark_command = [
            'E:/Wireshark/tshark.exe',  # E:\\Wireshark\\tshark.exe
            '-i', '以太网',  # 以太网接口名称或编号
            # '-w', video_number + '.pcap',
            '-w', pcap_file_path,
            '-f', f'host {server_ip}',
            '-a', f'duration:{playtime + offset_time}'  # 捕获持续时间
        ]
        print("Wireshark starting...")
        process = subprocess.Popen(tshark_command)
        time.sleep(offset_time)
        print("Wireshark started.\n")

        # 播放视频
        print("Playing video {}...".format(video_number))
        load_and_play_video(driver, video, playtime, wait)
        print("Playback finished.\n")

        # 关闭wireshark
        process.terminate()
        print("Wireshark terminated.")
        print("Pcaps saved to {}.".format(pcap_file_path))

        # 记录logs
        filename = "log_" + video_number + f"_{bandwidth}_{playtime}s.txt"

        save_logs_to_file(driver, logs_folder_name, filename)
        print("Video {} finished.\n".format(video_number))

        # # 刷新页面
        # print("Refreshing page...\n")
        # driver.refresh()
        # time.sleep(2)

        # 关闭浏览器
        driver.quit()
        time.sleep(2)

    # folder_name = "original_logs"
    # folder_name = "0721_original_logs"
    # filename = "log_" + time.strftime("%Y%m%d-%H%M") + f"_300bit.txt"
    # save_logs_to_file(driver, folder_name, filename)

except Exception as e:
    print("An error occurred:")
    traceback.print_exc()

# driver.quit()
print("All videos finished.")
