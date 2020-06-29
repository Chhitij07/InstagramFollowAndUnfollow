from selenium import webdriver
from bs4 import BeautifulSoup
import re
from time import sleep
import json

insta_handle = '' # Type Instagram Username Here
insta_password = '' # Type Password for your Instagram account here

def getDriver(background=False):
    options = webdriver.ChromeOptions()
    if background == True:
        options.add_argument('--no-sandbox')
        options.add_argument('headless')
    driver = webdriver.Chrome(options=options,executable_path='C:\Program Files\ChromeDriver\chromedriver.exe')
    # driver = webdriver.Chrome(options=options)
    driver.get('https://www.instagram.com/accounts/login')
    sleep(5)
    inputElement = driver.find_elements_by_class_name("_2hvTZ")[0]
    inputElement.send_keys(insta_handle)
    inputElement = driver.find_elements_by_class_name("_2hvTZ")[1]
    inputElement.send_keys(insta_password)
    inputElement.submit()
    sleep(10)
    return driver

def getSoup(driver, link, click = False, n_scrolls = 0):
    source=getSource(driver,link, click ,n_scrolls)
    soup=BeautifulSoup(source,'lxml')
    return source, soup

def getSource(driver, link, click = False, n_scrolls=0):
    driver.get(link)
    sleep(2)
    try:
        if click == True:
            driver.execute_script('document.getElementsByClassName("-nal3")[1].click(); ')
            sleep(10)
    except:
        pass
    title = driver.title
    if title.find('Login') > -1:
        sleep(7200)
        return
    for i in range(n_scrolls):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(1)
    source=driver.page_source
    if source.find("Please wait a few minutes before you try again.") > -1:
        sleep(7200)
        return
    return source

blocked = False

def follow(user_id):
    driver = getDriver()
    user_id=user_id.replace(' ','')
    user_id=user_id.replace('/','')
    source, soup=getSoup(driver,'https://www.instagram.com/'+user_id)
    if soup.find('button', class_='_5f5mN') is not None:
        try:
            driver.execute_script('document.getElementsByClassName("_5f5mN")[0].click(); ')
        except Exception as e:
            print(str(e))
            print(user_id)
            driver.close()
    elif soup.find('button', class_='BY3EC') is not None:
        try:
            driver.execute_script('document.getElementsByClassName("BY3EC")[0].click(); ')
        except Exception as e:
            print(str(e))
            print(user_id)
            driver.close()
    print('Following '+user_id)
    sleep(10)

def follow_users(driver,user_id,clicks_count):
    sleep(10)
    user_id=user_id.replace(' ','')
    user_id=user_id.replace('/','')
    source, soup=getSoup(driver,'https://www.instagram.com/'+user_id, click=True)
    followers = soup.find_all('button',class_ = "sqdOP")
    for i in range(len(followers)):
        driver.execute_script('document.getElementsByClassName("sqdOP")['+str(i)+'].click(); ')
        clicks_count = clicks_count + 1
        if clicks_count > 80:
            sleep(3600)
            clicks_count = 0
        sleep(2)
    print(clicks_count)
    # for follower in followers:
    #     id = follower.get('href')
    #     follow(id)
    return clicks_count

def unfollow_users():
    # background = input('Run in background? (y|n) \n')
    # if background[0] == 'y' or background[0] == 'Y':
    #     background = True
    # else:
    #     background = False
    driver = getDriver()
    try:
        for i in range(4):
            driver.get("https://www.instagram.com/" + insta_handle)
            sleep(5)
            driver.execute_script('document.getElementsByClassName("-nal3")[2].click(); ')
            sleep(5)
            for i in range(12):
                try:
                    driver.execute_script('document.getElementsByClassName("_8A5w5")[1].click(); ')
                    sleep(2)
                    driver.execute_script('document.getElementsByClassName("-Cab_")[0].click(); ')
                    sleep(5)
                    print("Unfollowed " +str((i+1)) + " users")
                except Exception as e:
                    print("Failed to unfollow_user because "+ str(e))
        sleep(3600)
    except:
        driver.close()
    return

def getUsers(tag, clicks_count):
    background = input('Run in background? (y|n) \n')
    if background[0] == 'y' or background[0] == 'Y':
        background = True
    else:
        background = False
    driver = getDriver()
    users=[]
    count = 0
    scroll_count = 0
    dup_count=0
    u_posts=[]
    sleep(10)
    source, soup=getSoup(driver,'https://www.instagram.com/explore/tags/'+tag)
    try:
        while(len(u_posts) < 5):
            n_count=0
            u_count=0
            ps=soup.findAll('div',class_='kIKUG')
            for post in ps:
                if post.a.get('href') in u_posts:
                    n_count=n_count+1
                    continue
                dup_count=0
                u_count=u_count+1
                count = count + 1
                u_posts.append(post.a.get('href'))
                print("No of unique posts : ",len(u_posts))
            if count > 500:
                break
            if u_count==0:
                dup_count=dup_count+1
                if dup_count>=10:
                    print('breaking')
                    break
                driver.execute_script("window.scrollTo(0, -250);")
                sleep(2)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sleep(5)
                flag=1
                continue
            for i in range(2):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sleep(2)
                scroll_count=scroll_count+3
                source=driver.page_source
                soup=BeautifulSoup(source,'lxml')
    except Exception as e:
        driver.close()
        print(str(e))
        pass
    try:
        for i,post in enumerate(u_posts):
            p_source, p_soup=getSoup(driver,'https://www.instagram.com'+post)
            if(p_soup.find_all('a',class_='ZIAjV')==None):
                continue
            user=p_soup.find_all('a',class_='ZIAjV')[0].get('href')
            if user not in users:
                try:
                    clicks_count=follow_users(driver,user,clicks_count)
                    users.append(user)
                except Exception as e:
                    driver.close()
                    print(str(e))
                    pass
    except Exception as e:
        driver.close()
        print(str(e))
        pass
