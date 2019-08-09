#!/usr/bin/env python
# coding: utf-8


from selenium import webdriver
from bs4 import BeautifulSoup
import time
import xlsxwriter 

class InstagramHandler():

    def __init__(self):
        self.driver = webdriver.Chrome('../chromedriver')
        #### Enter Your Insta Username  ####
        user = input("Enter Yopur Instagram user to scrape data")
        url = "https://www.instagram.com/{}/".format(user)
        self.driver.get(url)
        self.driver.maximize_window()
        for scroll in range(5):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
        

#### METHOD TO GET USER DETAILS ####

    def getUserDetails(self):
        page = BeautifulSoup(self.driver.page_source, 'lxml')
        username = page.find('h1', attrs = {'class':'fDxYl'}).text
        name = page.find('h1', attrs = {'class':'rhpdm'}).text
        basic_details = page.findAll('span', attrs = {'class':'g47SY'})
        ######### FOLLOWERS ########
        followers = basic_details[1].text
        if 'm' in followers:
            followers = int(float(followers.replace('m',''))*1000000)
        elif 'k' in followers:
            followers = int(float(followers.replace('k',''))*1000 )
        else:
            followers = int(followers)
        ######### FOLLOWING ##########   
        following = basic_details[2].text
        if 'm' in following:
            following = int(float(following.replace('m',''))*100000)
        elif 'k' in following:
            following = int(float(following.replace('k',''))*1000 )
        else:
            following = int(following)
        ######### NO OF POSTS ##########    
        posts_count = basic_details[0].text
        if 'm' in posts_count:
            posts_count = int(float(posts_count.replace('m',''))*100000)
        elif 'k' in posts_count:
            posts_count = int(float(posts_count.replace('k',''))*1000 )
        else:
            posts_count = int(posts_count)
        return(username,name,followers,following,posts_count)
        
    ######### METHOD TO GET POST DETAILS ########
    def postDetails(self):
        page = BeautifulSoup(self.driver.page_source, 'lxml')
        post_data = page.findAll('div', attrs ={'class':'_bz0w'})
        post_urls = []
        post_media = []
        post_pages = []
        for post_link in post_data:
            post_attchment = post_link.find('img', attrs = {'class':'FFVAD'})['src']
            post_media.append(post_attchment)
#             print("post_attchment : ",post_attchment)
            post_links = post_link.find('a')
            post_links = post_links['href']
            post_links = "https://www.instagram.com" + str(post_links)
            post_urls.append(post_links)
#             print("post_links : ",post_links)
    def writeData(self):
        userDetails = self.getUserDetails()
        postDetails = self.postDetails()
        
#         print(userDetails[0])
        workbook = xlsxwriter.Workbook('Instagram.xlsx')
        worksheet = workbook.add_worksheet() 
        bold = workbook.add_format({'bold': True})
        worksheet.write(0,1,'Instagram Details',bold)
        worksheet.write(2,0,'Username',bold)
        worksheet.write(3,0,'Name',bold)
        worksheet.write(4,0,'Followers',bold)
        worksheet.write(5,0,'Folowings',bold)
        worksheet.write(6,0,'No. of Posts',bold)
        worksheet.write(2,2,userDetails[0])
        worksheet.write(3,2,userDetails[1])
        worksheet.write(4,2,userDetails[2])
        worksheet.write(5,2,userDetails[3])
        worksheet.write(6,2,userDetails[4])
        
        worksheet.write(8,1,"POST DETAILS",bold)
        worksheet.write(10,0,"S.No.",bold)
        worksheet.write(10,1,"Post Link",bold)
        worksheet.write(10,2,"Post Attachment",bold)
        
#         for i in range(11,int(userDetails[4])):
#             worksheet.write(i,0, i-11) 
#             worksheet.write(i,1, post_links[i-11]) 
#             worksheet.write(i,2, post_attchment[i-11]) 
            
        workbook.close()
    
    def exitBrowser(self):
        self.driver.quit()
    def startExecution(self):
        self.getUserDetails()
        self.postDetails()
        self.writeData()
        self.exitBrowser()
        
        
if __name__ == "__main__":
    obj = InstagramHandler()
    obj.startExecution()






