import random

teachers = [
    ["김진오", "아주대 미디어학과",       "/members/ajou/t1.jpg", "게으르지만 열심히 하고 싶은 꼬마 프로그래머"],
    ["박순영", "아주대 미디어학과",       "/members/ajou/t2.jpg", "전 서서도 잠을 잘 수 있습니다."],
    ["어수웅", "아주대 정보컴퓨터공학과", "/members/ajou/t3.jpg", "Null point exception"],
    ["최경철", "아주대 미디어학과",       "/members/ajou/t4.jpg", "자아정체성 혼란 디자이너"]
  ]


students = [
    ["오승현", "아주대 정보컴퓨터공학과",   "/members/ajou/s1.jpg"],
    ["이승용", "아주대 전자공학과",         "/members/ajou/s2.jpg"],
    ["주정용", "아주대 전자공학과",         "/members/ajou/s3.jpg"],
    ["박정석", "아주대 금융공학과",         "/members/ajou/s4.jpg"],
    ["문주성", "아주대 건설시스템공학과",   "/members/ajou/s5.jpg"],
    ["김민수", "아주대 경영학과",           "/members/ajou/s6.jpg"],
    ["박태준", "아주대 경영학과",           "/members/ajou/s7.jpg"],
    ["서성원", "아주대 경영학과",           "/members/ajou/s8.jpg"],
    ["김주영", "아주대 산업공학과",         "/members/ajou/s9.jpg"],
    ["박형민", "아주대 산업공학과",         "/members/ajou/s10.jpg"],
    ["최우인", "아주대 e-비지니스학과",     "/members/ajou/s11.jpg"],
    ["권민재", "아주대 소프트웨어융합학과", "/members/ajou/s12.jpg"],
    ["이하림", "아주대 SW특성화대학원",     "/members/ajou/s13.jpg"],
    ["심희승", "아주대 문화콘텐츠학과",     "/members/ajou/s14.jpg"],
    ["배꽃그리고솔", "아주대 미디어학과",   "/members/ajou/s15.jpg"],
    ["방성주", "아주대 미디어학과",         "/members/ajou/s16.jpg"],
    ["권순백", "아주대 미디어학과",         "/members/ajou/s17.jpg"],
    ["황원주", "아주대 미디어학과",         "/members/ajou/s18.jpg"],
    ["김재은", "아주대 미디어학과",         "/members/ajou/s19.jpg"],
    ["주정은", "아주대 심리학과",           "/members/ajou/s20.jpg"],
    ["김도아", "아주대 심리학과",           "/members/ajou/s21.jpg"]
  ]

random.shuffle(teachers)
random.shuffle(students)