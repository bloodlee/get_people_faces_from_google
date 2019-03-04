from selenium import webdriver
import base64
import os.path
import requests
import time
import random

chrome_path = r"H:\\chromedriver.exe"
target_folder = 'H:\\people_images'
visited = set()
index = 1

if not os.path.exists(target_folder):
    os.mkdir(target_folder)

driver = webdriver.Chrome(chrome_path)

keywords = ['happy face', 'smiling', 'face', 'crying', 'beauty', 'fear face', 'worker', 'engineers', 'kid', 'boy', 'girl', 'man', 'model', 'women']

for keyword in keywords:
    print("Try keyword \"{}\"".format(keyword))

    url = r"https://www.google.com/search?q=[KEY_WORD]&source=lnms&tbm=isch&sa=X&ved=0ahUKEwic_bSp0rndAhWFB3wKHdv_A7sQ_AUICygC&biw=1249&bih=1248"

    driver.get(url.replace("[KEY_WORD]", keyword))

    has_new_data = True
    same_page_index = 0
    tried_already = False

    while has_new_data:
        num_of_imgs = 0
        has_new_data = False
        imgs = driver.find_elements_by_class_name("rg_ic")

        for img in imgs[same_page_index:]:
            src_link = img.get_property("src")

            if not src_link:
                continue

            has_new_data = True

            if src_link[:10] == 'data:image':
                img_base64 = src_link[len("data:image/jpeg;base64,"):]

                try:
                    img_data = base64.b64decode(img_base64)

                    with open(os.path.abspath(os.path.join(target_folder, "{}.jpg".format(index))), 'wb') as f:
                        f.write(img_data)
                except Exception:
                    print("Met errors, skip it!")
                    continue
            else:
                response = requests.get(src_link)

                with open(os.path.abspath(os.path.join(target_folder, "{}.jpg".format(index))), 'wb') as f:
                    f.write(response.content)

            index += 1
            num_of_imgs += 1

        same_page_index += num_of_imgs

        time.sleep(2)

        if has_new_data:
            print("scroll to the bottom...")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        else:
            element = driver.find_element_by_id("smb")
            if element and element.get_property("value") == 'Show more results':
                print("Show me more button is there, click it")

                try:
                    element.click()
                    tried_already = False
                    has_new_data = True
                except Exception:
                    if not tried_already:
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                        tried_already = True

                        # try one more time
                        has_new_data = True
                    else:
                        print("no more data, try the next keyword")
                        break
            else:
                print("no more data, try the next keyword")


driver.close()

