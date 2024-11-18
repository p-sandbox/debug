import os

def delete_uploaded_file(filepath):
    """업로드된 APK 파일 삭제"""
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
            print(f"파일 삭제 성공: {filepath}")
        else:
            print(f"파일이 존재하지 않습니다: {filepath}")
    except Exception as e:
        print(f"파일 삭제 중 오류 발생: {e}")
        raise RuntimeError(f"파일 삭제 실패: {e}")
