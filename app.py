from flask import Flask, render_template, request, jsonify
from analyzer.adb_utils import adb_connect
from analyzer.upload_utils import upload_file
from analyzer.static_analysis import start_static_analysis
from analyzer.dynamic_analysis import start_dynamic_analysis, stop_dynamic_analysis
from analyzer.report_utils import download_pdf_report, download_static_json_report, download_dynamic_json_report
from analyzer.file_cleanup import delete_uploaded_file
from analyzer.dex_utils import process_apk
import os
from settings import UPLOAD_FOLDER, REPORT_FOLDER

app = Flask(__name__)

# 업로드된 파일 저장 경로 설정
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/static_analysis')
def static_analysis_page():
    return render_template('static_analysis.html')

@app.route('/dynamic_analysis')
def dynamic_analysis_page():
    return render_template('dynamic_analysis.html')

@app.route('/api_documentation')
def api_documentation():
    return render_template('api_documentation.html')

@app.route('/final_analysis')
def synthesis_analysis():
    return render_template('final_analysis.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/adb_connect', methods=['GET'])
def connect_adb():
    """ADB 연결 요청 처리"""
    result, status_code = adb_connect()
    return jsonify(result), status_code

@app.route('/api/upload', methods=['POST'])
def upload_and_analyze():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "파일이 요청에 포함되지 않았습니다."}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "업로드할 파일 이름이 없습니다."}), 400

        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        # 분석 프로세스 시작 전 리패키징
        output_dir = os.path.join(REPORT_FOLDER, "unpacked")
        os.makedirs(output_dir, exist_ok=True)  # unpacked 디렉토리가 없으면 생성
        repackaged_apk_path = os.path.join(REPORT_FOLDER, f"repackaged_{file.filename}")
        
        # process_apk가 최종 서명된 APK 경로를 반환
        signed_apk_path = process_apk(filepath, output_dir, repackaged_apk_path)

        # 분석 프로세스 시작
        adb_connect()
        file_hash = upload_file(signed_apk_path)  # 서명된 APK를 업로드
        start_static_analysis(file_hash)
        start_dynamic_analysis(file_hash)
        stop_dynamic_analysis(file_hash)

        # 보고서 다운로드
        pdf_report = download_pdf_report(file_hash)
        static_report = download_static_json_report(file_hash)
        dynamic_report = download_dynamic_json_report(file_hash)

        # 업로드된 파일 삭제
        delete_uploaded_file(filepath)
        delete_uploaded_file(signed_apk_path)  # 서명된 파일 삭제

        return jsonify({
            "status": "success",
            "message": "분석 및 보고서 다운로드가 완료되었습니다.",
            "reports": {
                "pdf": pdf_report,
                "static_json": static_report,
                "dynamic_json": dynamic_report
            }
        }), 200

    except Exception as e:
        print(f"오류 발생: {e}")  # 터미널에 오류 출력
        return jsonify({"error": "파일 처리 중 오류 발생", "details": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
