from django.shortcuts import render
from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup
from django import template
from datetime import datetime
from datetime import timedelta
user_id = ""
user_password = ""


# Array 생성
class_title = []
course_link = []
assign_link = {}
assign_list = {}


cols = 5
rows = 100

dt1 = datetime.now()


def home(request):
    if request.method == 'GET':
        user_id = request.GET.get('username'),  # .POST['title'],
        user_password = request.GET.get('password'),
        assign_final = assign_hey(user_id, user_password)
        return render(request, 'base/home.html', {'assign': assign_final[0], 'course_title': assign_final[1], 'course_range': len(assign_final[1])})

    return render(request, 'base/home.html', {'assign': {}, 'course_title': [], 'course_range': 0})


def assign_hey(user_id, user_password):
    # Create your views here.
    loginurl = ('https://cyber.gachon.ac.kr/login/index.php')
    secureurl = ('https://cyber.gachon.ac.kr/')

    userid = user_id
    userpass = user_password
    payload = {
        'username': userid,
        'password': userpass,
    }

    # 아이디 패스워드 POST 하기
    req = requests.post(loginurl, data=payload)
    soup = BeautifulSoup(req.text, 'html.parser')

    # course_linkf라는 클래스를 가진 모든 링크 찾기
    links = soup.find_all("a", {"class": "course_link"})

    # cousre- title 클래스에 있는 모든 div 찾기
    mydivs = soup.find_all("div", {"class": "course-title"})

    # Class title h3 로 시작하는 텍스트만 strip해서 집어넣기
    for classes in mydivs:
        class_title_text = classes.h3.text.strip()
        class_title.append(class_title_text)

    # 링크 soup에서 link만 찾아서 집어넣기
    for link in links:
        # print(link['href'])
        course_link.append(link['href'])
    count = 0
    arr = [[0 for j in range(cols)] for i in range(rows)]
    with requests.session() as s:
        s.post(loginurl, data=payload)

        for course in course_link:

            r = s.get(course)
            soup = BeautifulSoup(r.text, 'html.parser')
            soup2 = soup.findAll('a', href=True, text='Assignment')
            for link in soup2:

                if len(link['href']) > 0:
                    print(class_title[count])
                    print(link['href'])
                    assign_link[class_title[count]] = link['href']

            count += 1

        list_key = list(assign_link.keys())

        assign_final = {}
        count_course = 0
        for course in list_key:
            count1 = 0
            count2 = 0
            count3 = 0
            count4 = 0
            arr = [[0 for j in range(cols)] for i in range(rows)]
            r = s.get(assign_link[course])

            soup = BeautifulSoup(r.text, 'html.parser')
            cell_c1 = soup.findAll('td', {"class": "cell c1"})

            for value in cell_c1:

                arr[count1][0] = value.text
                count1 += 1
            cell_c2 = soup.findAll('td', {"class": "cell c2"})
            for value in cell_c2:
                time = value.text.split(" ")
                ymd = time[0].split("-")
                dt = time[1].split(":")
                dt2 = datetime(int(ymd[0]), int(
                    ymd[1]), int(ymd[2]), int(dt[0]), int(dt[1]))
                result = dt1 - dt2
                result_txt = ""
                if result.days >= 0:
                    result_txt = "overdue +" + \
                        str(result.days)+" day " + \
                        str(int(result.seconds/3600))+" hour"
                else:
                    result_txt = str(-result.days)+" day " + \
                        str(int(result.seconds/3600))+" hour left"
                arr[count2][1] = result_txt
                count2 += 1
            cell_c3 = soup.findAll('td', {"class": "cell c3"})
            for value in cell_c3:
                arr[count3][2] = value.text
                count3 += 1
            cell_c4 = soup.findAll('td', {"class": "cell c4 lastcol"})
            for value in cell_c4:
                arr[count4][3] = value.text
                arr[count4][4] = course
                count4 += 1
            assign_final[count_course] = arr[:count1]
            count_course += 1
        print(assign_final)
        return assign_final, list_key
