

def uos
  teachers = [
    ["박재영", "서울시립대 컴퓨터과학부", "/members/uos/t1.jpg", "취직했으나, 입사 포기하고 멋사 진행중."],
    ["박건수", "서울시립대 컴퓨터과학부", "/members/uos/t2.jpg", "멘붕 장인"],
    ["조인행", "서울시립대 컴퓨터과학부", "/members/uos/t3.jpg", "전략적인 선택이군요, 멋쟁이사자님"]
  ].shuffle

  students = [
    ["곽재만", "서울시립대 도시행정학과", "/members/uos/s1.jpg"], 
    ["김광성", "서울시립대 물리학과", "/members/uos/s2.jpg"], 
    ["김교동", "서울시립대 스포츠과학과", "/members/uos/s3.jpg"], 
    ["김소현", "서울시립대 전자전기컴퓨터공학부", "/members/uos/s4.jpg"], 
    ["김용운", "서울시립대 컴퓨터과학부", "/members/uos/s5.jpg"],
    ["김준영", "서울시립대 경영학부", "/members/uos/s6.jpg"], 
    ["김지원", "서울시립대 컴퓨터과학부", "/members/uos/s7.jpg"],
    ["김찬민", "서울시립대 기계정보공학과", "/members/uos/s8.jpg"],
    ["백경", "서울시립대 산업디자인학과", "/members/uos/s9.jpg"],
    ["안민섭", "서울시립대 건축학과", "/members/uos/s10.jpg"],
    ["양다영", "서울시립대 공간정보공학과", "/members/uos/s11.jpg"],
    ["이용현", "서울시립대 건축학과", "/members/uos/s12.jpg"],
    ["이혜인", "서울시립대 산업디자인학과", "/members/uos/s13.jpg"],
    ["전성숙", "서울시립대 산업디자인학과", "/members/uos/s14.jpg"],
    ["조세연", "서울시립대 생명과학과", "/members/uos/s15.jpg"],
    ["진동하", "서울시립대 컴퓨터과학부", "/members/uos/s16.jpg"],
    ["최용현", "서울시립대 경영학부", "/members/uos/s17.jpg"],
    ["최철헌", "서울시립대 컴퓨터과학부", "/members/uos/s18.jpg"],
    ["최태림", "서울시립대 경영학부", "/members/uos/s19.jpg"]
  ].shuffle

#선생님 셔플(랜덤) 한번 하고, 학생 셔플 한번 해서 넣음.
  teachers + students

end
