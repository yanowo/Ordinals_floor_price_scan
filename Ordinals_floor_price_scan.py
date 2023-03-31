from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
import requests

# 設置 Chrome 瀏覽器的選項
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # 選項可以在背景運行 Chrome
options.add_experimental_option('excludeSwitches', ['enable-logging'])

# 指定 Chrome 瀏覽器驅動程式的路徑，下載位置可能與您的位置不同
driver_path = 'chromedriver.exe'

# 設定監控的項目名稱
ordinal_name = input("請輸入要監控的 ordinal 名稱：")

# 設定價格門檻
threshold_price = float(input("設定通知價格："))  # 設定門檻價格

# 設定網站 URL
OW_url = f"https://ordinalswallet.com/collection/{ordinal_name}"
OS_url = f"https://ordswap.io/collections/{ordinal_name}"
ME_url = f"https://magiceden.io/ordinals/marketplace/{ordinal_name}"

# 初始化最低價格
min_price = float("inf")

# 初始化網站名稱
OW_name = "Ordinalswallet"
OS_name = "Ordswap"
ME_name = "Magiceden"

# 初始化網頁標籤名稱
OW_tag_name = 'p'
OS_tag_name = 'span'
ME_tag_name = 'div'

# 初始化網頁元素定位路徑
OW_xpath = '/html/body/div[3]/div/div[2]/div/div[1]/div[2]/div'
OS_xpath = '//*[@id="root"]/div/div[4]/div/div/div/div[1]/div/div[1]/div[2]/div[2]/div/p'
ME_xpath = '//*[@id="content"]/div/div[1]/div/div[2]/div[2]/div[1]/div/div[1]/div[2]/div[2]/span'

# 初始化 Chrome 瀏覽器驅動程式
driver = webdriver.Chrome(executable_path=driver_path, options=options)
print("\n-----開始執行-----")
while True:
    
    # 初始化警告訊息列表
    warning_messages = []
    
    # 逐一查詢三個網站的最低價格
    for site_name, site_url, site_tag_name, site_xpath in zip(
        [OW_name, OS_name, ME_name],
        [OW_url, OS_url, ME_url],
        [OW_tag_name, OS_tag_name, ME_tag_name],
        [OW_xpath, OS_xpath, ME_xpath],
    ):
        driver.get(site_url)
        time.sleep(5)  # 等待 5 秒鐘，直到網頁加載完成
    
        # 找到包含價格的元素
        try:
            
            price_tag = driver.find_element_by_xpath(site_xpath)
            current_price = float(price_tag.text.replace(",", ""))
        except:
            print(f"{site_name} 沒有這個項目")
            continue
    
        # 列印出當下價格
        print(f"{site_name} price: {current_price}")
        if current_price < threshold_price:
            warning_messages.append(f"{site_name} 價格低於門檻價格 {threshold_price}！")
        
    if warning_messages:
        print("\n".join(warning_messages))
        
        # 休眠 1 分鐘
    print("\n\n一分鐘後繼續執行\n\n")
    time.sleep(60)
        
        # 關閉 Chrome 瀏覽器驅動程式
driver.quit()
