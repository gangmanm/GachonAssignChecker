from django.shortcuts import render
from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup
from django import template
from datetime import datetime
from datetime import timedelta
user_id = ""
user_password = ""

# 과제 저장하는 dictionary
assign_final = {}
mooc_final = {}
# Array 생성
class_title = []
course_link = []
assign_link = {}
assign_list = {}
list_key = []


cols = 6
rows = 100

dt1 = datetime.now()


def home(request):
    if request.method == 'GET':
        assign_final = {}
        user_id = request.GET.get('username'),  # .POST['title'],
        user_password = request.GET.get('password'),
        assign_final = assign_hey(user_id, user_password)
        mooc_final = mooc_hey(user_id, user_password)
        return render(request, 'base/home.html', {'assign': assign_final[0], 'mooc': mooc_final[0], 'course_title': assign_final[1], 'course_range': len(assign_final[1])})
    else:
        assign_final = {}
        return render(request, 'base/home.html', {'assign': assign_final[0], 'mooc': mooc_final[0], 'course_title': assign_final[1], 'course_range': 0})


def assign_hey(user_id, user_password):
    list_key = []
    assign_final = {}
    # Array 생성
    class_title = []
    course_link = []
    assign_link = {}
    assign_list = {}
    # Create your views here. 로그인하는 url
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
    #class_title = ['메타버스 vr/ar', 'p실무', '컴퓨터 구조',
     #             '드론과 로봇틱스', '컴퓨터그래픽스', '폭력예방교육']
    # 링크 soup에서 link만 찾아서 집어넣기
    for link in links:
        # print(link['href']) 아직 전체 list
        course_link.append(link['href'])

   # course_link = ['https://cyber.gachon.ac.kr/course/view.php?id=82533', 'https://cyber.gachon.ac.kr/course/view.php?id=82636', 'https://cyber.gachon.ac.kr/course/view.php?id=83046',
    #              'https://cyber.gachon.ac.kr/course/view.php?id=83951', 'https://cyber.gachon.ac.kr/course/view.php?id=83200', 'https://cyber.gachon.ac.kr/course/view.php?id=73208']

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
                    assign_link[class_title[count]] = link['href']
            soup3 = soup.findAll('a', href=True, text='과제')
            for link in soup3:
                if len(link['href']) >= 0:
                    # print(class_title[count])
                    # print(link['href'])
                    assign_link[class_title[count]] = link['href']

            count += 1

        list_key = list(assign_link.keys())

        assign_final = {}
        count_course = 0
        for course in class_title:
            count1 = 0
            count2 = 0
            count3 = 0
            count4 = 0
            arr = [[0 for j in range(cols)] for i in range(rows)]

            if course in assign_link.keys():
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
                    result_txt = dt2
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

            else:
                assign_final[count_course] = []

            count_course += 1
        # print(assign_final)
        return assign_final, class_title

# mooc을 가져오는 코드


def mooc_hey(user_id, user_password):

  
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
    # Array 생성
    class_title = []
    course_link = []

    # Class title h3 로 시작하는 텍스트만 strip해서 집어넣기
    for classes in mydivs:
        class_title_text = classes.h3.text.strip()
        class_title.append(class_title_text)
    #class_title = ['메타버스 vr/ar', 'p실무', '컴퓨터 구조',
     #              '드론과 로봇틱스', '컴퓨터그래픽스', '폭력예방교육']
    # 링크 soup에서 link만 찾아서 집어넣기
    for link in links:
        # print(link['href'])
        course_link.append(link['href'])

    #course_link = ['https://cyber.gachon.ac.kr/course/view.php?id=82533', 'https://cyber.gachon.ac.kr/course/view.php?id=82636', 'https://cyber.gachon.ac.kr/course/view.php?id=83046',
              #  'https://cyber.gachon.ac.kr/course/view.php?id=83951', 'https://cyber.gachon.ac.kr/course/view.php?id=83200', 'https://cyber.gachon.ac.kr/course/view.php?id=73208']

    count = 0
    assign_link = {}
    assign_list = {}

    cols = 5
    rows = 100

    arr = [[0 for j in range(cols)] for i in range(rows)]

    with requests.session() as s:
        s.post(loginurl, data=payload)

        for course in course_link:

            r = s.get(course)
            soup = BeautifulSoup(r.text, 'html.parser')
            soup2 = soup.findAll('a', href=True, text='Progress status')
            for link in soup2:

                if len(link['href']) >= 0:
                    assign_link[class_title[count]] = link['href']

            soup3 = soup.findAll('a', href=True, text='학습진도현황')
            for link in soup3:
                if len(link['href']) >= 0:
                    assign_link[class_title[count]] = link['href']

            count += 1

        list_key = list(assign_link.keys())

        mooc_final = {}
        count_course = 0
        mooc_count1 = 0
        mooc_count2 = 0
        mooc_count3 = 0
        mooc_count4 = 0
        mooc_title = []
        mooc_tt = []
        mooc_pt = []
        mooc_dt = []
        mooc_left_dt = []
        mooc_due_time = []

        for course in list_key:
            count1 = 0
            mooc = [[0 for j in range(cols)] for i in range(rows)]

            if course in assign_link.keys():
                r = s.get(assign_link[course])

                soup = BeautifulSoup(r.text, 'html.parser')
                # 강의 제목 찾기
                for row in soup.findAll('table', {"class": "table table-bordered user_progress"}):
                    for x in row.find_all('td', {"class": "text-left"}):
                        mooc[mooc_count1][0] = x.text[1:]
                        mooc_count1 += 1
                # 강의 최소 들어야하는 시간
                for row in soup.findAll('table', {"class": "table table-bordered user_progress"}):
                    for x in row.find_all('td', {"class": "text-center hidden-xs hidden-sm"}):
                        mooc[mooc_count2][1] = x.text
                        mooc_count2 += 1
                        dt = x.text.split(":")
                        if len(dt) < 3:
                            mooc_due_time.append(int(dt[0])*60+int(dt[1]))
                        else:
                            mooc_due_time.append(
                                int(dt[0])*3600+int(dt[1])*60+int(dt[2]))
                # 내가 지금까지 들은 시간
                for row in soup.findAll('table', {"class": "table table-bordered user_progress"}):
                    for x in row.find_all('td', {"class": "text-center"}):
                        if x.button:
                            if "상" in x.text:
                                time = x.text.split("상")
                                mooc_pt.append(time[0])
                            if "D" in x.text:
                                time = x.text.split("D")
                                mooc_pt.append(time[0])
                # 버튼이 존재하는 것의 타이틀을 모두가져오면 , 제목과 기한을 가져올 수 있다.
                for row in soup.find_all('button', title=True, class_="btn btn-default btn-xs track_detail"):
                    if (row['title']):
                        value = row['title'][-20:-1]
                        time = value.split(" ")
                        ymd = time[0].split("-")
                        dt = time[1].split(":")
                        # 기한을 date time으로 변경
                        dt2 = datetime(int(ymd[0]), int(
                            ymd[1]), int(ymd[2]), int(dt[0]), int(dt[1]))
                        result = dt1 - dt2
                        result_txt = dt2
                        mooc_dt.append(row['title'])
                        mooc_left_dt.append(result_txt)
                        mooc_count3 += 1

                # 이제 기한과 , 들은 시간을 매칭 시킨다. 우선 위에서 찾은 강의 제목과 일치하는 기한을 찾았으면 mooc 2차원 배열에 집어넣기
                for i in range(mooc_count1):
                    for j in range(mooc_count3):
                        # 제목을 비교하기 위해 뒤에 기한 부분은 없앤다.
                        if mooc[i][0] == mooc_dt[j][0:-44]:
                            mooc[i][3] = mooc_left_dt[j]
                            mooc[i][2] = mooc_pt[j][:]
                            # 진행 사항 퍼센트를 구하기 위한 부분이다.
                            if ":" in mooc[i][2]:
                                time = mooc[i][2].split(":")
                                # 1시간 이내의 강의
                                if len(time) < 3:
                                    progress_time = float(
                                        time[0])*60 + float(time[1])
                                    total_percent = int(
                                        (progress_time / mooc_due_time[i]) * 100)
                                    if total_percent >= 100:
                                        total_percent = 100
                                    mooc[i][4] = total_percent
                                else:
                                    progress_time = float(
                                        time[0])*3600 + float(time[1])*60+float(time[2])

                                    total_percent = int(
                                        (progress_time / mooc_due_time[i]) * 100)
                                    if total_percent >= 100:
                                        total_percent = 100
                                    mooc[i][4] = total_percent

                mooc_final[count_course] = mooc[:mooc_count1]

            else:
                mooc_final[count_course] = []

            mooc_count1 = 0
            mooc_count2 = 0
            mooc_count3 = 0
            mooc_count4 = 0
            mooc_title = []
            mooc_tt = []
            mooc_pt = []
            mooc_dt = []
            mooc_left_dt = []
            mooc_due_time = []
            count_course += 1
        return mooc_final, class_title


def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]
 