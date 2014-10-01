# -*- coding: utf-8 -*-
import random

from apps import app, db
from apps.models import Match, Candidate
from person_info import uos, ajou, gachon, hanyang, kaist, khu, korea, mju, sejong, snu_yonsei, ssu

import admin, candidate, comment, debug, test, tournament, user_account, view_page, what_match

# [1,2,3,4] ---> [[1,2],[3,4]]
def chunk(mylist):
    temp = zip(*[iter(mylist)] * 2)
    return [list(x) for x in temp]


@app.route('/init_cand_vote')
def init_cand_vote():
    '''
    기능
    : URL/init_cand_vote 이라고 치면, Match 의 vote 기록이 모두 0 으로 초기화된다.

    주의
    : Return 값이 없으니, 서버 에러가 날텐데 당황하지 말고 DB를 확인하면 된다.
    '''
    match = Match.query.all()
    for each_match in match:
        each_match.candidate_A_count = 0
        each_match.candidate_B_count = 0
    db.session.commit()
    
    

# Candidate DB에 선수들을 다 집어넣는 함수
@app.route('/total_allinone')
def all_in(gachon=None):
    '''
    기능
    : URL/total_allinone 이라고 치면, Candidate DB가 채워진다.

    주의
    : Return 값이 없으니, 서버 에러가 날텐데 당황하지 말고 DB를 확인하면 된다.
    '''


    ''' 선샌님 + 학생 (옛날모델 ㅠㅠ )
    ajou_info = [st for st in ajou.students] + [tc for tc in ajou.teachers]
    gachon_info = [st for st in gachon.students] + [tc for tc in gachon.teachers]
    hanyang_info = [st for st in hanyang.students] + [tc for tc in hanyang.teachers]
    kaist_info = [st for st in kaist.students] + [tc for tc in kaist.teachers]
    korea_info = [st for st in korea.students] + [tc for tc in korea.teachers]
    khu_info = [st for st in khu.students] + [tc for tc in khu.teachers]
    mju_info = [st for st in mju.students] + [tc for tc in mju.teachers]
    sejong_info = [st for st in sejong.students] + [tc for tc in sejong.teachers]
    snu_yonseig_info = [st for st in snu_yonsei.students] + [tc for tc in snu_yonsei.teachers]
    ssu_info = [st for st in ssu.students] + [tc for tc in ssu.teachers]
    uos_info = [st for st in uos.students] + [tc for tc in uos.teachers]
    master_info = [tc for tc in teacher.master]

    seed_num = [1,3,5,6,9]
    developer_seed = []
    for seed in seed_num:
        developer_seed.append(kaist.students[seed])

    all_info = ajou_info + gachon_info + hanyang_info + kaist_info + khu_info + mju_info + sejong_info + snu_yonseig_info + ssu_info + uos_info + master_info + developer_seed + korea_info

    for each_member in all_info:
        name = each_member[0]
        school = each_member[1]
        photo_link = each_member[2]

        member = Candidate(
            name=name,
            photolink=photo_link,
            school=school
        )

        db.session.add(member)
        db.session.commit()
    '''

    # 선생님들만 가보자! (5명 자름)
    ajou_info = [tc for tc in ajou.teachers]
    gachon_info = [tc for tc in gachon.teachers]
    hanyang_info = [tc for tc in hanyang.teachers]
    kaist_info = [tc for tc in kaist.teachers]
    khu_info = [tc for tc in khu.teachers]
    korea_info = [tc for tc in korea.teachers]
    mju_info =  [tc for tc in mju.teachers]
    sejong_info = [tc for tc in sejong.teachers]
    snu_yonseig_info =  [tc for tc in snu_yonsei.teachers]
    ssu_info = [tc for tc in ssu.teachers]
    uos_info = [tc for tc in uos.teachers]

    all_teacher = [tc for tc in ajou.teachers] + [tc for tc in gachon.teachers] + [tc for tc in hanyang.teachers] + [tc for tc in kaist.teachers] + [tc for tc in khu.teachers] + [tc for tc in korea.teachers] + [tc for tc in mju.teachers] + [tc for tc in sejong.teachers] + [tc for tc in snu_yonsei.teachers] + [tc for tc in ssu.teachers] + [tc for tc in uos.teachers]

    # 선생님들의 이름, 학교, 사진경로를 Candidate Table에 각각 column에 채워넣는다.
    for each_member in all_teacher:
        name = each_member[0]
        school = each_member[1]
        photo_link = each_member[2]

        member = Candidate(
            name=name,
            photolink=photo_link,
            school=school
        )

        db.session.add(member)
        db.session.commit()



# Candidate DB에서 꺼내와서 선수들을 그룹별로 집어넣는 함수
@app.route('/group_likelion')
def grouping():
    '''
    기능
    : URL/group_likelion 이라고 치면, MATCH Table에 각각의 Column이 업데이트 된다.
    : Candidate Table 의 row를 2개씩 Chunking 하여 붙여주는 것이기 때문에, Candidate DB가 채워져 있어야 한다.
    : 32강 대진표만 채워주고, 16강 - 8강 - 4강 은 유저의 선택에 따라 각각 개별화된다.

    주의
    : Return 값이 없으니, 서버 에러가 날텐데 당황하지 말고 DB를 확인하면 된다.

    '''


    ''' 선생님 + 학생 (옛날 모델)
    ajou_info = [st for st in ajou.students] + [tc for tc in ajou.teachers]
    gachon_info = [st for st in gachon.students] + [tc for tc in gachon.teachers]
    hanyang_info = [st for st in hanyang.students] + [tc for tc in hanyang.teachers]
    kaist_info = [st for st in kaist.students] + [tc for tc in kaist.teachers]
    khu_info = [st for st in khu.students] + [tc for tc in khu.teachers]
    korea_info = [st for st in korea.students] + [tc for tc in korea.teachers]
    mju_info = [st for st in mju.students] + [tc for tc in mju.teachers]
    sejong_info = [st for st in sejong.students] + [tc for tc in sejong.teachers]
    snu_yonseig_info = [st for st in snu_yonsei.students] + [tc for tc in snu_yonsei.teachers]
    ssu_info = [st for st in ssu.students] + [tc for tc in ssu.teachers]
    uos_info = [st for st in uos.students] + [tc for tc in uos.teachers]
    master_info = [tc for tc in teacher.master]
    seed_num = [1,3,5,6,9]
    developer_seed = []
    for seed in seed_num:
        developer_seed.append(kaist.students[seed])

    all_info = ajou_info + gachon_info + hanyang_info + kaist_info + khu_info + mju_info + sejong_info + snu_yonseig_info + ssu_info + uos_info + master_info + korea_info + developer_seed

    # 이렇게 불러오는거야 ㅋㅋㅋ
    # candidate_members = Candidate.query.all()
    # candidate_members[0].photolink

    candidate_members = Candidate.query.all()
    random.shuffle(candidate_members)
    #candidate_members = candidate_members[:160]
    candidate_members = chunk(candidate_members)

    idx = 0
    game_round = 1
    for each_pair in candidate_members:
        A = each_pair[0]
        B = each_pair[1]

        nameA = A.name
        orgA = A.school
        photoA = A.photolink

        nameB = B.name
        orgB = B.school
        photoB = B.photolink

        if idx < 16:
            game_group = 1
        elif idx >= 16 and idx < 32:
            game_group = 2
        elif idx >= 32 and idx < 48:
            game_group = 3
        elif idx >= 48 and idx < 64:
            game_group = 4
        elif idx >= 64 and idx < 80:
            game_group = 5
        else:
            game_group = 6

        my_match = Match(
            season_num=32,
            game_round=game_round,
            candidate_A_namename=nameA,
            candidate_A_photolink=photoA,
            candidate_A_school=orgA,
            candidate_B_namename=nameB,
            candidate_B_photolink=photoB,
            candidate_B_school=orgB,
            group=game_group
        )
        db.session.add(my_match)
        db.session.commit()
        idx += 1
        game_round += 1
        if game_round == 17:
            game_round = 1
    '''

    # 선생님들만 가보자! (5명 자름)
    ajou_info = [tc for tc in ajou.teachers]
    gachon_info = [tc for tc in gachon.teachers]
    hanyang_info = [tc for tc in hanyang.teachers]
    kaist_info = [tc for tc in kaist.teachers]
    khu_info = [tc for tc in khu.teachers]
    korea_info = [tc for tc in korea.teachers]
    mju_info =  [tc for tc in mju.teachers]
    sejong_info = [tc for tc in sejong.teachers]
    snu_yonseig_info =  [tc for tc in snu_yonsei.teachers]
    ssu_info = [tc for tc in ssu.teachers]
    uos_info = [tc for tc in uos.teachers]

    all_teacher = [tc for tc in ajou.teachers] + [tc for tc in gachon.teachers] + [tc for tc in hanyang.teachers] + [tc for tc in kaist.teachers] + [tc for tc in khu.teachers] + [tc for tc in korea.teachers] + [tc for tc in mju.teachers] + [tc for tc in sejong.teachers] + [tc for tc in snu_yonsei.teachers] + [tc for tc in ssu.teachers] + [tc for tc in uos.teachers]

    candidate_members = Candidate.query.all() # Candidate DB에서 각각의 row를 list dictionary 형태로 가져온다.
    random.shuffle(candidate_members) # 한 번 섞어주시고,
    #candidate_members = candidate_members[:160]
    candidate_members = chunk(candidate_members) # Candidate DB의 두 개의 row를 하나의 짝으로 묶어줍시다.

    idx = 0  # 라운드를 세기 위한 인덱스
    game_round = 1 # 라운드를 세기 위한 인덱스
    for each_pair in candidate_members:
        A = each_pair[0]
        B = each_pair[1]

        nameA = A.name
        orgA = A.school
        photoA = A.photolink

        nameB = B.name
        orgB = B.school
        photoB = B.photolink

        if idx < 16:
            game_group = 1
        '''
        elif idx >= 16 and idx < 32:
            game_group = 2
        elif idx >= 32 and idx < 48:
            game_group = 3
        elif idx >= 48 and idx < 64:
            game_group = 4
        elif idx >= 64 and idx < 80:
            game_group = 5
        else:
            game_group = 6
        '''

        my_match = Match(
            season_num=32,
            game_round=game_round,
            candidate_A_namename=nameA,
            candidate_A_photolink=photoA,
            candidate_A_school=orgA,
            candidate_B_namename=nameB,
            candidate_B_photolink=photoB,
            candidate_B_school=orgB,
            group=1
        )
        db.session.add(my_match)
        db.session.commit()
        idx += 1
        game_round += 1
        if game_round == 17:
            game_round = 1



