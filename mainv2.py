import requests,math,time
import pandas as pd

topic=str(input('enter the topic you would like to find: '))

url="https://api.nytimes.com/svc/search/v2/articlesearch.json"
API_KEY = "tcn7ErBggObioRwi4Z7KlUG9Adnsa2Rs"

#setting parameters
parameters={'q':topic, 'fq':'document_type:("article")','api key':API_KEY}
response=requests.get(url,params=parameters)
content=response.json()
total_hits=content['response']['meta']['hits']
total_page_count = math.ceil(total_hits/10)

print("there are currently a total of",total_hits,"articles")
page_request=""
page_count=0
ans_yes=['yes','Yes','y','Y','Yes']
ans_no=['no','NO','n','N','No']


#function to check if user function is int
def check_user_input(input):
  try:
    vl=int(input)
    return True
  except ValueError:
    return False


#determine if input is yes or no and if he wants to go through all the articles
while page_request not in ans_yes and page_request not in ans_no:
  page_request= str(input("\n do u still want to get all the articles?\n(yes or no): "))
if page_request in ans_no:
  print("How many pages do you want to scan?\nenter any interger value between 0 and",total_page_count)
  user_req=input("enter the integer")

  while check_user_input(user_req)!=True:
    user_req=input("please input int:")
    check_user_input(user_req)

    page_count=int(user_req)
    print("okay, please wait")

elif page_request in ans_yes:
  page_count=math.ceil(total_hits/10)
  print("okay, please wait")

year_published=[]
real_year_pub=[]
article_year=[]

#list for popularity has an element in it because this is the first creation of articles on the users topic
increase_decrease=["Increase"]

#variable for popularity csv
a_str = ""
year_pub=0

#list for raw data csv
date_published=[]
section=[]
article_name=[]
article_url=[]
article_num=[]
a_num=1
page_number=[]
#loop that goes through each page and collects data in 2 sec intervals
for i in content['respose']['docs']:
  #find article num
  article_num.append(a_num)
  #find publication date
  date_published.append(i['pub_date'])
  #finds article title
  article_name.append(i['headline']['main'])
  #find article section
  section.append(i['section_name'])
  #find article url
  article_url(i['web_url'])
  #find article page num
  page_number.append(i)
  #counter for article num
  a_num=a_num+1

  #gets the year from publication date
  #turns the first for char from pub_date
  a_str=str(i['pub_date'])
  year_pub=int(a_str[0:4])
  year_published.append(year_pub)
#lets api rest for 5 sec per page
time.sleep(5)
for i in year_published:
      if i not in real_year_pub:
        real_year_pub.append(i)

real_year_pub.sort()

article_count={i:year_published.count(i) for i in year_published}

for x in real_year_pub:
  if x in article_count.keys():
    article_year.append(article_count[x])

for i in (range(len(article_year)-1)):
  j=i+1

  if(article_year[j]-article_year[i])>0:
    increase_decrease.append("Increase")

  elif (article_year[j]-article_year[i])==0:
    increase_decrease.append("No Increase or Decrease")

  elif (article_year[j]-article_year[i])==0:
    increase_decrease.append("Decrease")
  
popularity_data = {'year Published':real_year_pub,"Article Published During this year":article_year,'popularity':increase_decrease}
raw_article_data={'article number':article_num,'page number':page_number,'date published':date_published,'article name':article_name,'section':section,'article url':article_url}

#turn dictonary into dataframe
dfPOP=pd.DataFrame(popularity_data,columns=['year Published','Article Published during this year','popularity'])
dfRAW=pd.DataFrame(raw_article_data,columns=['article number','pagenumber','date published','article name','section','article url'])

#turns dataframe into csv
dfPOP.to_csv(r'C:\Users\nikhi\OneDrive\Desktop\Newspaper-Sentiment-Analysis-master\Newspaper-Sentiment-Analysis-master\popularity_data.csv',index=False,header=True)
dfRAW.to_csv(r'C:\Users\nikhi\OneDrive\Desktop\Newspaper-Sentiment-Analysis-master\Newspaper-Sentiment-Analysis-master\raw_data.csv',index=False,header=True)

print("done")







#from main import *

#def startMenu():
#  mainCategories = ['https://api.nytimes.com/svc/search/v2/articlesearch.json?q=election&api-key=nik142']


 # print('\nHello! Welcome to the News Reader and Analysis App!\nSelect from the following Categories.\n 1. World News. \n 2. Business News. \n 3. Technology News. \n 4. Science News. \n')

#  checkCategory = input()
#
#  if checkCategory == '1':
#   mainUrl = mainCategories[0]
#  elif checkCategory == '2':
#    mainUrl = mainCategories[1]
#  elif checkCategory == '3':
#    mainUrl = mainCategories[2]
#  elif checkCategory == '4':
#    mainUrl = mainCategories[3]
#  else:
#    print("Try Again!!\n You selected wrong input")
#
#  return mainUrl
#
#if __name__=='__main__':
#	lists=[]
#	mainUrl = startMenu()
#	print("\n HELLO!!! What do you wanna do know? : \n 1. See News \n 2. See Sentiment Value for National News \n 3. See overall Sentiment for now. \n")
#	check = input("Enter the number: ")
#	sentValue=[]
#	for x in range(1,3):
#		newsPaper={}
#		url = urlMaker(mainUrl, x)
#		soup = soupee(url)
#		titles, links = parser(soup)
#
#		if check=='1':
#			seeNews(titles,links)
#		elif check=='2':
#			sentimentAnalysis(newsPaper, titles, links)
#		else:
#			avgSentVal = avgSentiment(newsPaper, titles, links)
#	if check== '3':
#		avgSentiment = find_Sentiment(sum(sentValue))
#		print("Average Sentiment now is : "+ avgSentiment+'. ('+str(sum(sentValue))+')')