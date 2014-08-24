
def sejong
  teachers = [
    ["김범준", "세종대 컴퓨터공학과", "/members/sejong/t1.jpg", "나이 / 피곤 담당"],
    ["김은영", "세종대 컴퓨터공학과", "/members/sejong/t2.jpg", "무서움 / 지각비 담당"],
    ["오성진", "건국대 인터넷미디어공학부", "/members/sejong/t3.jpg", "비쥬얼 / 야망 담당"],
    ["장지영", "세종대 컴퓨터공학과", "/members/sejong/t4.jpg", "잔소리 / 비타민 담당"]
  ].shuffle

  students = [
    ["강지혜", "세종대 전자공학과", "/members/sejong/s1.jpg"], 
    ["김명주", "건국대 축산식품공학", "/members/sejong/s2.jpg"], 
    ["김상범", "중앙대 전자전기공학부", "/members/sejong/s3.jpg"], 
    ["김수현", "건국대 기술경영", "/members/sejong/s4.jpg"], 
    ["김승근", "세종대 건축공학과", "/members/sejong/s5.jpg"],
    ["김재희", "건국대 음악교육과", "/members/sejong/s6.jpg"], 
    ["김준호", "건국대 컴퓨터공학부", "/members/sejong/s7.jpg"],
    ["박준모", "건국대 컴퓨터공학부", "/members/sejong/s8.jpg"],
    ["성정화", "건국대 커뮤니케이션디자인학과", "/members/sejong/s9.jpg"],
    ["신동훈", "건국대 경영학과 ", "/members/sejong/s10.jpg"],
    ["이석재", "서울과기대 MSDE", "/members/sejong/s11.jpg"],
    ["이정훈", "한성대 경제학과", "/members/sejong/s12.jpg"],
    ["최지환", "건국대 경제학과", "/members/sejong/s13.jpg"]
  ].shuffle

  teachers + students
end
