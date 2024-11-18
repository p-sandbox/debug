# settings.py
import os

##############################################################################
###################################경로 설정###################################
###################################설정 필수###################################
# MobSF 서버 설정
SERVER = "http://127.0.0.1:8000"
APIKEY = "146157e092040b595560024717c7ded24ce65bed8e279fc3a13f6bbd7eb18be0"  # MobSF의 API 키
#########################################################################################

# frida 서버 설정
FRIDA_SERVER_PATH = r"C:\Users\han31\Desktop\sand_project\frida\frida-core-devkit-16.5.6-android-x86_64"

# adb 경로 설정 (필요할 경우 전체 경로로 지정)
ADB_PATH = r"C:\Users\han31\AppData\Local\Android\Sdk\platform-tools\adb.exe"
APKTOOL_PATH = r"C:\Windows\apktool.jar"  # apktool.jar 파일의 전체 경로 (사용자 환경에 맞게 수정)

# Java 설정
JAVA_HOME = os.environ.get("JAVA_HOME", r"C:\Program Files\Java\jdk-23")  # Java JDK 설치 경로 (필요시 수정)

# wkhtmltopdf 경로
WKHTMLTOPDF_PATH = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"


####################################설정 필수#####################################
# 에뮬레이터 연결 설정
EMULATOR_IP = "192.168.56.113"
EMULATOR_PORT = "5555"
#################################################################################

# 복호화 키 (AES-128/ECB)
DECRYPTION_KEY = b'dbcdcfghijklmaop'  # 16바이트 길이의 AES 키

#서명 키
KEYSTORE_PATH = os.path.join(os.getcwd(), "yeop.keystore")  
KEY_ALIAS = "yeop"  # Keystore의 키 별칭
KEYSTORE_PASSWORD = "yeop8650"  # Keystore 비밀번호
KEY_PASSWORD = "yeop8650"  # 키 비밀번호

# 지역 위치 정보
DNAME = {
    "CN": "yeop",        # Common Name (예: 사용자 이름 또는 애플리케이션 이름)
    "OU": "yeop",    # Organizational Unit (예: 팀 또는 부서 이름)
    "O": "yeop",      # Organization (예: 회사 이름)
    "L": "busan",            # Locality (예: 도시)
    "S": "busan",           # State (예: 주 또는 지역 이름)
    "C": "KR"               # Country Code (ISO 3166-1 alpha-2 형식)
}

# 동적 분석 모니터링 간격 (초 단위)
MONITOR_INTERVAL = 10

# 보고서 및 파일 경로 설정
UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")     
REPORT_FOLDER = os.path.join(os.getcwd(), "reports")
DEX_FOLDER = os.path.join(os.getcwd(), "DEX")


# 보고서 저장 경로 설정
REPORT_FOLDER = "reports"
PDF_REPORT_PATH = f"{REPORT_FOLDER}/report.pdf"
STATIC_JSON_REPORT_PATH = f"{REPORT_FOLDER}/static_report.json"
DYNAMIC_JSON_REPORT_PATH = f"{REPORT_FOLDER}/dynamic_report.json"




