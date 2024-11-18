import os
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
from settings import SERVER, APIKEY

def find_java_binary():
    java_home = os.environ.get('JAVA_HOME')
    if java_home:
        return os.path.join(java_home, 'bin', 'java')
    return 'java'

def upload_file(filepath):
    """파일을 MobSF에 업로드하고 해시값 반환"""
    print("파일 업로드 시작")
    try:
        with open(filepath, 'rb') as file:
            multipart_data = MultipartEncoder(fields={'file': (filepath, file, 'application/octet-stream')})
            headers = {
                'Content-Type': multipart_data.content_type,
                'Authorization': APIKEY
            }
            response = requests.post(SERVER + '/api/v1/upload', data=multipart_data, headers=headers)

            if response.status_code == 200:
                print("파일 업로드 성공")
                response_data = response.json()
                return response_data.get("hash")
            else:
                print(f"파일 업로드 실패: {response.status_code}, {response.text}")
                raise RuntimeError(f"파일 업로드 실패: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"파일 업로드 중 오류 발생: {e}")
        raise e
