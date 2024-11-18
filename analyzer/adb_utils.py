import subprocess
import settings

def adb_connect():
    """ADB 연결 설정"""
    try:
        result = subprocess.run(
            [settings.ADB_PATH, "connect", f"{settings.EMULATOR_IP}:{settings.EMULATOR_PORT}"],
            check=True,
            text=True,
            capture_output=True,
            shell=True,
            encoding='utf-8'
        )
        print(f"ADB 연결 성공: {result.stdout}")
        return {"message": "ADB 연결 성공", "output": result.stdout}, 200
    except subprocess.CalledProcessError as e:
        print(f"ADB 연결 실패: {e.stderr}")
        return {"error": "ADB 연결 실패", "details": e.stderr}, 500
