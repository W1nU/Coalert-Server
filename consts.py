from enum import Enum

class consts(Enum):
    NAME = 'name' # 사용자 이름
    ID = 'id' # 사용자 아이디
    PASSWORD = 'password' # 사용자 패스워드
    TYPE = 'type' # 사용자 피부타입, '건성': 0, '지성': 1, '중성': 2, '복합성': 3, '민감성': 4
    BIRTH = 'birth' # 사용자 생일
    SEX = 'sex' # 사용자 성별
    ACCESS = 'access' # 접속 타입
    EMAIL = 'email' # 사용자 이메일
    CNAME = 'cname' # 화장품 이름
    ONELINE = 'oneline' # 간단한 리뷰 한줄평
    RATE = 'rate' # 리뷰 점수
    IMEI = 'imei' # 핸드폰 고유번호
    COMPANY = 'company' # 화장품 제조사
    CONTENT = 'content' # 자세한 리뷰 내용
    CATEGORY = 'category' # 화장품 카테고리, 선블락 1, 아이쉐도우 2, 파운데이션 3, 립 4
    INGR = 'ingr' # 화장품 성분
