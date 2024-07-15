import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import os

def load_and_play_video(driver, url, wait):
    """加载并播放视频，然后在随机时间后暂停。"""
    input_box = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "form-control")))
    input_box.clear()
    input_box.send_keys(url)
    print(f"URL {url} loaded into input box.")

    # 点击加载并播放视频
    load_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.container > div:nth-child(2) > div.input-group > span > button.btn.btn-primary")))
    load_button.click()
    print("Load button clicked.")

    # 手动播放
    # time.sleep(1) # TODO 这里需要考虑修改等待逻辑
    time.sleep(1) # for windows
    # haohao 7.11 测试发现不加timesleep也是可以正常触发播放？还是加1s比较稳定
    play_button = wait.until(EC.element_to_be_clickable((By.ID, "iconPlayPause")))
    play_button.click()
    print("Play button clicked.")

    # 播放时间，设置为5min
    playtime = 8 * 60
    print("Load button clicked and play video for {} min.".format(playtime / 60))
    time.sleep(playtime)

def save_logs_to_file(driver, folder_name="original_logs", filename="browser_logs.txt"):
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
    # 'http://39.102.209.114/BV1P44y1F72Z.mpd'
    'http://182.92.189.72/BV1P44y1F72Z.mpd'
]

wait = WebDriverWait(driver, 10)
try:
    # test: 一次测试多个视频
    # for i in range(1, 3):   # TODO
    for video in video_urls:
        load_and_play_video(driver, video, wait)
        # time.sleep(2)  # 如果需要在视频间有特定的间隔

    folder_name = "original_logs"
    filename = "log_" + time.strftime("%Y%m%d-%H%M") + f"_1mbit.txt"
    save_logs_to_file(driver, folder_name, filename)

except Exception as e:
    print("An error occurred:")
    traceback.print_exc()

driver.quit()
