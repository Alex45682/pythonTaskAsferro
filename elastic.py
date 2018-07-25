# -- coding: utf-8 --
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from elasticsearch import Elasticsearch
from datetime import datetime

driver = webdriver.Chrome()
driver.get("https://media.netflix.com/en/")  # openNetflix


def putElastic(title, txt1, txt2):
    es = Elasticsearch()

    create = es.index(index="netflix", doc_type="any", id="1",

                      body={
                          "Text1": txt1,
                          "Title": title,
                          "Text2": txt2,
                          "DataTime": datetime.now()})

    get_art = es.get(index="netflix", doc_type="any", id="1")

    print ("ADDED:", create)
    print ("YOUR ARTICLE:", get_art)

    delete_art = es.delete(index="netflix", doc_type="any", id="1")
    print ("DELETED:", delete_art)


articles = [0, 1, 2]

for item in articles:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='preview-text']//h3//a"))
    )
    elem = driver.find_elements_by_xpath("//div[@class='preview-text']//h3//a")
    elem[item].click()  # openArticle
    article1 = driver.find_element_by_xpath("//div[@class='post-intro']/h2[@class='post-title']")
    title1 = article1.text  # getTitle

    text1 = driver.find_element_by_xpath("//div[@class='post-text']//p[1]")
    p1 = text1.text  # getText<p1>

    text2 = driver.find_element_by_xpath("//div[@class='post-text']//p[2]")
    p2 = text2.text  # getText<p2>

    putElastic(title1, p1, p2)

    driver.back()


driver.close()
