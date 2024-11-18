import os
import subprocess
from settings import APKTOOL_PATH

def decompile_apk(apk_path, output_dir):
    """APK 파일 디패키징"""
    try:
        os.makedirs(output_dir, exist_ok=True)
        subprocess.run(["java", "-jar", APKTOOL_PATH, "d", apk_path, "-o", output_dir, "-f"], check=True)
        print(f"APK 디패키징 성공: {apk_path}")
    except Exception as e:
        print(f"APK 디패키징 실패: {e}")
        raise RuntimeError(f"APK 디패키징 실패: {e}")

def recompile_apk(source_dir, output_apk):
    """APK 파일 리패키징"""
    try:
        subprocess.run(["java", "-jar", APKTOOL_PATH, "b", source_dir, "-o", output_apk], check=True)
        print(f"APK 리패키징 성공: {output_apk}")
    except Exception as e:
        print(f"APK 리패키징 실패: {e}")
        raise RuntimeError(f"APK 리패키징 실패: {e}")
