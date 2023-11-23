import csv
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import pickle


def readCSVFILE(temp_list,
                filename='SophonCodeInterpreterEvalVersion1_xingfuli_dianshangquanliang_paichuguiyin_wufazhaohui.csv'):
    # 打开CSV文件
    with open(filename,
              newline='', encoding='utf-8') as csvfile:
        # 创建CSV阅读器对象
        reader = csv.reader(csvfile)
        next(reader)

        # 遍历每一行数据
        for row in reader:
            temp_dict = {}
            # 打印每一行数据
            temp_dict["id"] = row[0]
            temp_dict["query"] = row[1]
            temp_dict["answer_url"] = row[3]
            temp_list.append(temp_dict)


def requestURL(url, cookies, driver):
    try:
        # load cookies for given websites
        driver.get(url)
        if cookies != None:
            for cookie in cookies:
                driver.add_cookie(cookie)
            driver.refresh()
    except Exception as e:
        # it'll fail for the first time, when cookie file is not present
        print(str(e))
        print("Error loading cookies")


def save_cookie(driver, path):
    with open(path, 'wb') as filehandler:
        pickle.dump(driver.get_cookies(), filehandler)


def load_cookie(driver, path):
    with open(path, 'rb') as cookiesfile:
        cookies = pickle.load(cookiesfile)
        for cookie in cookies:
            driver.add_cookie(cookie)


def close_all(driver):
    # close all open tabs
    if len(driver.window_handles) < 1:
        return
    for window_handle in driver.window_handles[:]:
        driver.switch_to.window(window_handle)
        driver.close()


def quit(driver, cookies_file_path):
    save_cookie(driver, cookies_file_path)
    close_all(driver)

def logRecord(driver):
    # extract requests from logs
    logs_raw = driver.get_log("performance")
    logs = [json.loads(lr["message"])["message"] for lr in logs_raw]

    def log_filter(log_):
        return (
            # is an actual response
                log_["method"] == "Network.responseReceived"
                # and json
                and "json" in log_["params"]["response"]["mimeType"]
        )

    for log in filter(log_filter, logs):
        request_id = log["params"]["requestId"]
        resp_url = log["params"]["response"]["url"]
        print(f"Caught {resp_url}")
        print(driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": request_id}))


## step1 table2json
# temp_list = []
# readCSVFILE(temp_list)
# with open('need.json', 'w') as json_file:
#     json.dump(temp_list, json_file)

## step2 cookie save
with open('need.json', 'r') as json_file:
    temp_list = json.load(json_file)

save_dir = r"./save/cookies.pkl"
# driver = webdriver.Chrome()
# driver.get(r"https://sso.bytedance.com")
# time.sleep(60)
# save_cookie(driver, save_dir)

## start task

driver = webdriver.Chrome()
cookies = pickle.load(open(save_dir, "rb"))
requestURL(r"https://sso.bytedance.com",
           cookies, driver)

for i, item in enumerate(temp_list):
    if "sophon-data" in item["answer_url"]:
        requestURL(
            item["answer_url"], None, driver)



        time.sleep(60)
        break
time.sleep(60)
