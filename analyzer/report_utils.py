import requests
import json
from settings import SERVER, APIKEY, REPORT_FOLDER

def download_pdf_report(file_hash):
    """PDF 보고서 다운로드"""
    headers = {'Authorization': APIKEY}
    data = {"hash": file_hash}
    response = requests.post(SERVER + '/api/v1/download_pdf', data=data, headers=headers, stream=True)
    if response.status_code == 200:
        report_path = f"{REPORT_FOLDER}/report.pdf"
        with open(report_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)
        return report_path
    else:
        raise RuntimeError(f"PDF 보고서 다운로드 실패: {response.status_code}, {response.text}")

def download_static_json_report(file_hash):
    """정적 분석 JSON 보고서 다운로드"""
    headers = {'Authorization': APIKEY}
    data = {"hash": file_hash}
    response = requests.post(SERVER + '/api/v1/report_json', data=data, headers=headers)
    if response.status_code == 200:
        report_path = f"{REPORT_FOLDER}/static_report.json"
        with open(report_path, 'w') as f:
            json.dump(response.json(), f, indent=4)
        return report_path
    else:
        raise RuntimeError(f"정적 JSON 보고서 다운로드 실패: {response.status_code}, {response.text}")

def download_dynamic_json_report(file_hash):
    """동적 분석 JSON 보고서 다운로드"""
    headers = {'Authorization': APIKEY}
    data = {"hash": file_hash}
    response = requests.post(SERVER + '/api/v1/dynamic/report_json', data=data, headers=headers)
    if response.status_code == 200:
        report_path = f"{REPORT_FOLDER}/dynamic_report.json"
        with open(report_path, 'w') as f:
            json.dump(response.json(), f, indent=4)
        return report_path
    else:
        raise RuntimeError(f"동적 JSON 보고서 다운로드 실패: {response.status_code}, {response.text}")
