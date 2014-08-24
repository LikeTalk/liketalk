
def gachon
  teachers = [
  ["송제인", "가천대 소프트웨어설계경영", "/members/gachon/t1.jpg", "내안에 무한한 힘이 넘친다!"], 
  ["이현아", "가천대 소프트웨어설계경영", "/members/gachon/t2.jpg", "제가 당신을 인도하겠어요."],
  ["안준형", "가천대 소프트웨어설계경영", "/members/gachon/t3.jpg", "내가 캐리한다. 나만 믿어."] 
  ].shuffle

  students = [
  ["이다빈", "가천대 경영", "/members/gachon/s6.jpg"],
  ["이승현", "가천대 산업디자인", "/members/gachon/s8.jpg"],
  ["김초지", "가천대 시각디자인", "/members/gachon/s3.jpg"],
  ["김진영", "가천대 컴퓨터미디어융합", "/members/gachon/s2.jpg"],
  ["채민규", "가천대 컴퓨터공학", "/members/gachon/s11.jpg"],
  ["심세용", "가천대 소프트웨어설계경영", "/members/gachon/s5.jpg"],
  ["이상아", "가천대 소프트웨어설계경영", "/members/gachon/s7.jpg"],
  ["이혜빈", "가천대 컴퓨터공학", "/members/gachon/s9.jpg"]
  ].shuffle

  teachers + students
end
