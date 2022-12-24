# assignapp

가천대학교 과제 확인 웹사이트 
-> 과제 기한, 과제 점수, 제출 유무를 한눈에 확인 하여 과제를 놓치지 않겠다는 다짐

Django , Bootstrap, HTML, Beautifulsoup, 배포 Heroku 사용 


HTML 에서 유저에게 GET 메소드를 통해 
id 와 password 를 받은후 
Beautifulsoup를 통해 모든 과목들의 링크안의 과제 리스트를 돌면서 2차원 배열을 생성한다. 
후에 course 번호 , 과제 를 딕셔너리를 만든 후 
home.html에 넘겨준다. 

home.html에서
python template 코드를 이용하여 , for loop를 돌며 코스별로 tab을 생성
tab안에는 과제리스트를 생성하고, badge를 통해 색깔별로 중요 포인트를 준다. 
[결과창] 

<img width="567" alt="스크린샷 2022-12-25 오전 12 13 15" src="https://user-images.githubusercontent.com/97601109/209448356-fc76f6e9-e660-4bf5-a1a2-994f1e717264.png">
