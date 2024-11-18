import requests
from settings import SERVER, APIKEY

def start_static_analysis(file_hash):
    """정적 분석 시작"""
    headers = {'Authorization': APIKEY}
    data = {"hash": file_hash, "re_scan": 0}
    response = requests.post(SERVER + '/api/v1/scan', data=data, headers=headers)
    if response.status_code != 200:
        raise RuntimeError(f"정적 분석 시작 실패: {response.status_code}, {response.text}")
