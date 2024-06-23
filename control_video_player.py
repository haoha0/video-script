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
    # time.sleep(1) # TODO 这里需要考虑修改等待逻辑
    time.sleep(2) # for windows

    play_button = wait.until(EC.element_to_be_clickable((By.ID, "iconPlayPause")))
    play_button.click()
    print("Play button clicked.")

    # 随机等待时间，播放视频
    wait_time = random.randint(5, 11)
    print(f"Playing video for {wait_time - 1} seconds.")
    time.sleep(wait_time)

    # 暂停视频
    play_button.click()
    print("Video paused.")

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
time.sleep(10)
driver.refresh()

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
    'https://dash.akamaized.net/akamai/bbb_30fps/bbb_30fps.mpd',
    'https://dash.akamaized.net/digitalprimates/fraunhofer/480p_video/heaac_2_0_with_video/Sintel/sintel_480p_heaac2_0.mpd'
]

wait = WebDriverWait(driver, 10)
try:
    # test: 一次测试多个视频
    for i in range(1, 3):   # TODO
        # 选择前i个视频进行测试
        selected_videos = video_urls[:i]
        # selected_videos = random.sample(video_urls, min(i, len(video_urls)))  # 选择min(i, len(video_urls))个视频，防止超出列表长度
        print(f"Test {i}: Testing with {len(selected_videos)} videos.")
        for url in selected_videos:
            load_and_play_video(driver, url, wait)
            # time.sleep(2)  # 如果需要在视频间有特定的间隔

        folder_name = "original_logs"
        filename = "log_" + time.strftime("%Y%m%d-%H%M") + f"_test_{i}.txt"
        save_logs_to_file(driver, folder_name, filename)
        time.sleep(5)  # 等待一段时间开始下一轮测试

except Exception as e:
    print("An error occurred:")
    traceback.print_exc()

driver.quit()
