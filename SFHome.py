from bs4 import BeautifulSoup
import requests
import re,random
import mysql.connector
from sklearn import tree
import time



#-------------------introduction and taking what user needs-------------------------
print("welcome\nwe are gonna predict the price of the hypothetical home\nthat you want to bye")
for i in range(10):
    print('*',end=' ')
    time.sleep(0.2)
print()
print("now please enter the count of pages that you want to dig in:",end='\t')
user_data_dig = int(input())
for i in range(10):
    print('*',end=' ')
    time.sleep(0.2)
print()
print("and now we want you to tell us how many rooms and how much\nsphere your hypothetical should have\nyou should enter 2 houses!!!")
user_data_home1_r = int(input("number of rooms of the first house:"))
user_data_home1_s = int(input(" sphere of the first house:"))
user_data_home2_r = int(input("number of rooms of the second house:"))
user_data_home2_s = int(input(" sphere of the second house:"))
#-------------------connecting to database------------------------------------------
cnx = mysql.connector.connect(user='root', password='141516',
                              host='127.0.0.1',
                              database='mysql-learning')
curs = cnx.cursor()


#-------------------gathering data of houses from ihome.ir-------------------------
city = "تهران"
g = open('test2.txt', encoding='utf-8', mode='a+')
for page in range(1,user_data_dig):
    bama_link = requests.get("https://www.ihome.ir/%D8%AE%D8%B1%DB%8C%D8%AF-%D9%81%D8%B1%D9%88%D8%B4/%D8%A2%D9%BE%D8%A7%D8%B1%D8%AA%D9%85%D8%A7%D9%86/%D8%A7%DB%8C%D8%B1%D8%A7%D9%86/{}/".format(page))
    soup = BeautifulSoup(bama_link.text,'html.parser')


#------------------peeling scrips and making what we need-------------------------------------
    sample = [] #for making record of a house contains location,price,room and sphere
    remover = 0
    convert = ''#for deleting ',' out of the numbers
    counter = 0
    car = soup.find_all('div',attrs={"class":"sh-content left"})
    for i in car :
        item = re.sub(r'\s+',' ',i.text).strip()
        item = item.split(' ')
        location = list(item[0])
        for bb in range(5):
            location.pop(-1)
        for bb in location:
            if bb==',':
                continue
            else:    
                convert +=bb
        if (re.search(r'^\d',convert))==None:
            sample.append(-1)
        else:
            sample.append(int(convert))
        convert = ''
        item.pop(0)

#------------------making numbers from string dataes-----------------------
        for j in item:
            ttt = re.match(r'^([\u06F0-\u06F90-9]+)$',j)#checking for persian numbers
            if ttt==None:
                convert += j + ' '
                counter += 1
                continue
            else:
                break
        sample.append(convert)
        convert = ''
        while remover<counter:
            item.pop(0)
            remover += 1
#------------------------------------------------------------------------------------
        for rec in item:
            ttt = re.match(r'^([\u06F0-\u06F90-9]+)$',rec)#checking for persian numbers
            if ttt==None:
                continue
            else:
                sample.append(int(rec))
                convert = ''
        tester = len(sample)
#---------------------for inserting in database--------------------------------------
        if tester==4:
            b = int(sample[0])//1000000   
            curs.execute("INSERT INTO building VALUES(\'{x}\',{x0},\'{x1}\',{x2},{x3})".format(x=city,x0=b,x1=sample[1],x2=sample[2],x3=sample[3]))
            cnx.commit()
        sample = []
    print('page ',end='\t')
    print(page,end=' ')
    print('is done.')


#----------------machine calculating stuff --------------------------------------

x = []
y = []

curs.execute("SELECT price,room,sphare FROM building2")

for prc,rm,sph in curs:#fetching dataes (price,room,sphere)
    item = [rm,sph]
    x.append(item)
    y.append(prc)

clf = tree.DecisionTreeClassifier()
guess = clf.fit(x,y)

my_record = [[user_data_home1_r,user_data_home1_s],[user_data_home2_r,user_data_home2_s]]
ans = guess.predict(my_record)
print("the hypothetical price of your first house is",end='\t')
print(ans[0],end='\t')
print("million Toomans")
print("the hypothetical price of your socond house is",end='\t')
print(ans[1],end='\t')
print("million Toomans")