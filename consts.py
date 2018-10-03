from enum import Enum

class Consts(Enum):
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
    SESSION = 'session' # 세션 키
    SEARCH = 'search' # 검색시 요청 상수
    RANK = 'rank'
    START = 'start' # 검색시 시작 인덱스
    COUNT = 'count' # 검색시 몇개 가져올 것인지 결정
    LCODE = 'lcode' # 게시글 번호
    TITLE = 'title' # 게시글 제목
    LIKE = 'like' # 좋아요 갯수
    
    DB_ERROR = '현재 데이터베이스 서버 접속이 원할하지 않습니다\n잠시후 시도해 주세요!'
    POST = ['POST', 'GET'] #서버에서 사용하는 상수
