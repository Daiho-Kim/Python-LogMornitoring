import time
import threading
import json
import os
import requests

# Slack Webhook URL 입력
# SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/XXX/YYY/ZZZ"
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"

# Slack 알림 전송 함수
def send_slack_alert(message, webhook_url):
    payload = {
        "text": message
    }
    try:
        response = requests.post(webhook_url, json=payload)
        if response.status_code != 200:
            print(f"Slack 전송 실패: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Slack 오류: {e}")

# 공통 알림 함수
def send_alert(message):
    send_slack_alert(f"[로그 알림] {message}", SLACK_WEBHOOK_URL)

# 파일을 읽어 키워드 목록을 반환하는 함수
def load_keywords(keyword_file: str) -> list:
    try:
        with open(keyword_file, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"[ERROR] 키워드 파일 읽기 실패: {e}")
        return []

# 로그 파일을 모니터링하고 키워드를 감지하는 함수
def monitor_log(log_file: str, keyword_file: str, idle_timeout: int = 300):
    keywords = load_keywords(keyword_file)
    if not keywords:
        print(f"[WARNING] 키워드가 없습니다: {keyword_file}")
        return

    print(f"[INFO] 모니터링 시작: {log_file} (키워드: {keyword_file}, 타임아웃: {idle_timeout}s)")

    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            f.seek(0, os.SEEK_END)  # 파일 끝으로 이동
            last_activity = time.time()

            while True:
                line = f.readline()
                if not line:
                    time.sleep(1)
                    if time.time() - last_activity > idle_timeout:
                        send_alert(f"[IDLE] 로그 활동 없음: {log_file}")
                        last_activity = time.time()
                    continue

                last_activity = time.time()
                for keyword in keywords:
                    if keyword in line:
                        send_alert(f"[MATCH] {log_file}: '{keyword}' 감지됨 → {line.strip()}")
                        break

    except FileNotFoundError:
        send_alert(f"[ERROR] 로그 파일 없음: {log_file}")
    except Exception as e:
        send_alert(f"[ERROR] 로그 모니터링 중 오류 발생: {e}")

# JSON 설정 파일을 읽어 모니터링 설정을 반환하는 함수
def load_json_config(config_path: str) -> list:
    try:
        with open(config_path, 'r', encoding="utf-8-sig") as f:
            print("[INFO] {config_path} is opened")
            config = json.load(f)
            print("[INFO] json load")
            return config.get("monitoring", [])
    except Exception as e:
        print(f"[ERROR] JSON 설정 파일 읽기 실패: {e}")
        return []

# 모니터링을 시작하는 함수
def start_monitoring(configs: list):
    threads = []
    for cfg in configs:
        log_file = cfg.get("log_file")
        keyword_file = cfg.get("keyword_file")
        idle_timeout = int(cfg.get("idle_timeout", 300))

        if log_file and keyword_file:
            t = threading.Thread(target=monitor_log, args=(log_file, keyword_file, idle_timeout))
            t.start()
            threads.append(t)
        else:
            print("[WARNING] 설정 항목 누락: log_file 또는 keyword_file")

    for t in threads:
        t.join()

# Main 실행 부분
if __name__ == "__main__":
    config_path = "C:\\Users\\kimda\\source\\repos\\LogMonitoring\\LogMonitoring\\mornitoring_list.json"
    configs = load_json_config(config_path)
    if configs:
        start_monitoring(configs)
    else:
        print("[ERROR] 모니터링 설정이 없습니다.")
