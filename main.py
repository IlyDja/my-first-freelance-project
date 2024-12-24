import undetected_chromedriver as uc
import time
from selenium.webdriver.common.by import By
from datetime import date, timedelta
from selenium.webdriver.common.action_chains import ActionChains
import os
import requests
import pandas as pd


# Перед ПЕРВЫМ запуском кода необходимо авторизоваться в личном кабинете через браузер Chrome.
# Перед КАЖДЫМ запуском кода закройте браузер Chrome, если он открыт
def main(url):
    options_chrome = uc.ChromeOptions()
    # укажите имя ВАШЕЙ папки на ВАШЕМ компьютере вместо mak13
    options_chrome.add_argument('user-data-dir=C:\\Users\\mak13\\AppData\\Local\\Google\\Chrome\\User Data')
    reports_folder_path = f"{os.getcwd()}\\reports_"  # В директории со скриптом создастся папка reports_ - в неё
    #  будут складываться скачанные отчёты, и, после отправки на сервер, автоматически удаляться
    prefs = {
        "download.default_directory": reports_folder_path
    }
    options_chrome.add_experimental_option("prefs", prefs)
    driver = uc.Chrome(options=options_chrome)
    driver.implicitly_wait(30)
    yesterday = date.today() - timedelta(1)
    yesterday_formatted_date = yesterday.strftime('%d.%m.%Y')

    try:
        driver.get(url)

        def find_el_by_xpath(xpath):
            return driver.find_element(By.XPATH, xpath)

        try:
            find_el_by_xpath("//div[text()='Продвижение']").click()
            find_el_by_xpath("//div[text()='Трафареты']").click()
            find_el_by_xpath("//div[text()='Аналитика продвижения']").click()
            find_el_by_xpath("//span[text()='Скачать в excel']").click()
            find_el_by_xpath("//label[text()='Выберите период']").click()
            find_el_by_xpath("//button[text()='Вчера']").click()
            find_el_by_xpath("//span[text()='Скачать']").click()
            print('first download completed')
            # first download completed
        except Exception as e:
            print(f'Не удалось загрузить первый файл. Ошибка: {e}')

        try:
            action = ActionChains(driver).move_to_element(find_el_by_xpath("//div[text()='FBO']"))
            action.perform()
            find_el_by_xpath("//div[text()='Стоимость размещения']").click()
            find_el_by_xpath("//span[text()='Скачать отчет']").click()
            time.sleep(1)
            find_el_by_xpath("//*[@value='ByProducts']").click()
            driver.find_elements(By.XPATH, "//span[contains(text(), 'Дата:')]")[1].click()
            find_el_by_xpath(f'//*[@aria-label="{yesterday_formatted_date}"]').click()
            find_el_by_xpath("//*[@value='ByProducts']").click()
            find_el_by_xpath("//span[text()='Скачать']").click()
            print('second download completed')
            # second download completed
        except Exception as e:
            print(f'Не удалось загрузить второй файл. Ошибка: {e}')

        try:
            action = ActionChains(driver).move_to_element(find_el_by_xpath("//div[text()='Товары']"))
            action.perform()
            find_el_by_xpath("//div[text()='Закрепление отзыва']").click()
            find_el_by_xpath("//span[text()='Дополнительно']").click()
            find_el_by_xpath("//div[text()='Скачать аналитику в Excel']").click()
            time.sleep(1)
            print('third download completed')
            # third download completed
        except Exception as e:
            print(f'Не удалось загрузить третий файл. Ошибка: {e}')

        try:
            action = ActionChains(driver).move_to_element(find_el_by_xpath("//div[text()='Товары']"))
            action.perform()
            find_el_by_xpath("//div[text()='Отзывы за баллы']").click()
            find_el_by_xpath("//span[text()='Перейти к отчетам']").click()
            time.sleep(1)
            find_el_by_xpath("//span[text()='Сформировать']").click()
            driver.refresh()
            find_el_by_xpath("//span[text()='Перейти к отчетам']").click()
            time.sleep(1)
            find_el_by_xpath("//span[contains(text(), 'Баллы за отзывы за период')]").click()
            time.sleep(1)
            print('fourth download completed')
            # fourth download completed
        except Exception as e:
            print(f'Не удалось загрузить четвёртый файл. Ошибка: {e}')

    except Exception as ex:
        print(f'Ошибка: {ex}')

    finally:
        driver.close()
        driver.quit()

        # URL конечной точки API
        url = 'http://example.com/v1/uploadReport'
        # Данные для авторизации (если требуется)
        auth = ('username', 'password')  # Замените на реальные данные

        for filename in os.listdir(reports_folder_path):
            file_path = os.path.join(reports_folder_path, filename)
            if 'баллы_за_отзывы_за_период' in filename:
                filename = filename[:26] + yesterday_formatted_date + '-' + yesterday_formatted_date + filename[47:]
                df = pd.read_excel(file_path)
                os.remove(file_path)
                file_path = os.path.join(reports_folder_path, filename)
                df = df[df['Дата публикации отзыва'] == yesterday_formatted_date]
                df.to_excel(file_path, index=False)

            with open(file_path, 'rb') as find_el_by_xpath:
                files = {'report': find_el_by_xpath}
                try:
                    response = requests.post(url, auth=auth, files=files)
                    if response.status_code == 200:
                        print("Отчет успешно загружен.")
                    else:
                        print(f"Произошла ошибка при загрузке отчета. Код статуса: {response.status_code}")
                except Exception as e:
                    print(f"Произошла ошибка при загрузке файла {filename}: {e}")
            os.remove(file_path)


if __name__ == "__main__":
    main('https://seller.ozon.ru/app/dashboard/main')
