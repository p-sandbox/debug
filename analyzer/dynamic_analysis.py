import requests
import time
from settings import SERVER, APIKEY

def start_dynamic_analysis(file_hash):
    """동적 분석 시작"""
    headers = {'Authorization': APIKEY}
    data = {"hash": file_hash}
    response = requests.post(SERVER + '/api/v1/dynamic/start_analysis', data=data, headers=headers)
    if response.status_code == 200:
        print("동적 분석이 성공적으로 시작되었습니다.")
    else:
        raise RuntimeError(f"동적 분석 시작 실패: {response.status_code}, {response.text}")

def stop_dynamic_analysis(file_hash):
    """동적 분석 중지"""
    headers = {'Authorization': APIKEY}
    data = {"hash": file_hash}
    response = requests.post(SERVER + '/api/v1/dynamic/stop_analysis', data=data, headers=headers)
    if response.status_code == 200:
        print("동적 분석이 성공적으로 중지되었습니다.")
    else:
        raise RuntimeError(f"동적 분석 중지 실패: {response.status_code}, {response.text}")
    time.sleep(5)  # 중지 후 대기
