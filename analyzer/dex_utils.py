import os
import shutil
import subprocess
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import logging
from settings import (
    APKTOOL_PATH, DECRYPTION_KEY, JAVA_HOME,
    REPORT_FOLDER, KEYSTORE_PATH, KEY_ALIAS, KEYSTORE_PASSWORD, KEY_PASSWORD, DNAME
)

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Java 실행 파일 경로 찾기
def find_java_binary():
    if JAVA_HOME:
        return os.path.join(JAVA_HOME, "bin", "java")
    return "java"

# 키스토어 생성
def generate_keystore(keystore_path):
    """
    settings.py의 서명 키 정보와 지역 위치 정보를 사용하여 키스토어 생성
    """
    keytool_path = os.path.join(JAVA_HOME, "bin", "keytool")
    dname = f"CN={DNAME['CN']}, OU={DNAME['OU']}, O={DNAME['O']}, L={DNAME['L']}, S={DNAME['S']}, C={DNAME['C']}"
    command = [
        keytool_path, "-genkeypair",
        "-alias", KEY_ALIAS,
        "-keyalg", "RSA",
        "-keysize", "2048",
        "-validity", "365",
        "-keystore", keystore_path,
        "-storepass", KEYSTORE_PASSWORD,
        "-keypass", KEY_PASSWORD,
        "-dname", dname
    ]
    try:
        subprocess.run(command, check=True, text=True)
        logger.info(f"키스토어가 생성되었습니다: {keystore_path} (DNAME: {dname})")
    except subprocess.CalledProcessError as e:
        logger.error(f"키스토어 생성에 실패했습니다: {e}")
        raise

# 키스토어 삭제
def delete_keystore(keystore_path):
    """
    키스토어 삭제
    """
    try:
        if os.path.exists(keystore_path):
            os.remove(keystore_path)
            logger.info(f"키스토어가 삭제되었습니다: {keystore_path}")
    except Exception as e:
        logger.error(f"키스토어 삭제에 실패했습니다: {e}")
        raise

# APK 디패키징
def unpack_apk(apk_path, output_dir):
    java_path = find_java_binary()
    command = [java_path, "-jar", APKTOOL_PATH, "d", "-f", "-s", apk_path, "-o", output_dir]
    try:
        subprocess.run(command, check=True, text=True)
        logger.info(f"APK가 성공적으로 디패키징되었습니다: {output_dir}")
    except subprocess.CalledProcessError as e:
        logger.error(f"APK 디패키징에 실패했습니다: {e}")
        raise

# 암호화된 DEX 파일 검색
def find_encrypted_dex(directory):
    encrypted_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".dex"):
                file_path = os.path.join(root, file)
                if is_encrypted(file_path):
                    encrypted_files.append(file_path)
    return encrypted_files

# 암호화 여부 확인
def is_encrypted(file_path):
    with open(file_path, "rb") as file:
        magic_number = file.read(4)
        return magic_number != b"dex\n"

# 로컬 AES 복호화 수행
def decrypt_with_local_aes(file_path):
    """로컬에서 AES 복호화 수행"""
    with open(file_path, "rb") as f:
        encrypted_data = f.read()

    cipher = AES.new(DECRYPTION_KEY, AES.MODE_ECB)
    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)

    if decrypted_data[:4] == b"dex\n":  # DEX 매직 넘버 확인
        return decrypted_data
    else:
        raise ValueError("복호화된 DEX 파일에서 올바른 서명을 찾을 수 없습니다.")

# DEX 대체
def replace_encrypted_dex(file_path, decrypted_data):
    with open(file_path, "wb") as file:
        file.write(decrypted_data)
    logger.info(f"암호화된 DEX 파일이 복호화된 데이터로 대체되었습니다: {file_path}")

# APK 리패키징
def repack_apk(source_dir, output_apk_path):
    java_path = find_java_binary()
    command = [java_path, "-jar", APKTOOL_PATH, "b", source_dir, "-o", output_apk_path]
    try:
        subprocess.run(command, check=True, text=True)
        logger.info(f"APK가 성공적으로 리패키징되었습니다: {output_apk_path}")
    except subprocess.CalledProcessError as e:
        logger.error(f"APK 리패키징에 실패했습니다: {e}")
        raise

# APK 서명
def sign_apk(apk_path, signed_apk_path, keystore_path):
    jarsigner_path = os.path.join(JAVA_HOME, "bin", "jarsigner")
    command = [
        jarsigner_path, "-keystore", keystore_path,
        "-storepass", KEYSTORE_PASSWORD, "-keypass", KEY_PASSWORD,
        "-signedjar", signed_apk_path, apk_path, KEY_ALIAS
    ]
    try:
        subprocess.run(command, check=True, text=True)
        logger.info(f"APK가 성공적으로 서명되었습니다: {signed_apk_path}")
    except subprocess.CalledProcessError as e:
        logger.error(f"APK 서명에 실패했습니다: {e}")
        raise

# 전체 프로세스 실행
def process_apk(apk_path, output_dir, repackaged_apk_path):
    """
    APK 처리 프로세스: 디패키징, DEX 복호화, 리패키징 및 서명
    """
    signed_apk_path = repackaged_apk_path.replace(".apk", "_signed.apk")
    try:
        # 1. 키스토어 생성
        if not os.path.exists(KEYSTORE_PATH):  # 키스토어가 없을 때만 생성
            generate_keystore(KEYSTORE_PATH)

        # 2. APK 디패키징
        unpack_apk(apk_path, output_dir)

        # 3. 암호화된 DEX 복호화
        encrypted_dex_files = find_encrypted_dex(output_dir)
        for dex_file in encrypted_dex_files:
            decrypted_data = decrypt_with_local_aes(dex_file)
            replace_encrypted_dex(dex_file, decrypted_data)

        # 4. APK 리패키징
        repack_apk(output_dir, repackaged_apk_path)

        # 5. APK 서명
        sign_apk(repackaged_apk_path, signed_apk_path, KEYSTORE_PATH)

        # 최종 서명된 APK 경로 반환
        return signed_apk_path
    finally:
        # 6. 필요 시 키스토어 삭제
        delete_keystore(KEYSTORE_PATH)

        # 7. 임시 파일 정리
        shutil.rmtree(output_dir, ignore_errors=True)
