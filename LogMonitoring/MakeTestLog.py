import time
import random
import os
from datetime import datetime

LOG_PATH = "logs/app1.log"  # 생성할 로그 파일 경로
INTERVAL = 2  # 로그 생성 간격 (초)

# 로그 메시지 샘플
MESSAGES = [
    "INFO: Application started successfully",
    "DEBUG: User clicked the login button",
    "WARNING: Disk space running low",
    "ERROR: Failed to connect to database",
    "INFO: Scheduled task completed",
    "CRITICAL: System overheating detected",
    "DEBUG: Cache cleared",
    "ERROR: Invalid user credentials",
    "INFO: Backup completed",
    "WARNING: High memory usage"
]

def generate_log(log_path: str, interval: int = 2):
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    print(f"[INFO] 로그 생성 시작: {log_path}")
    try:
        with open(log_path, 'a', encoding='utf-8') as f:
            while True:
                msg = random.choice(MESSAGES)
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                line = f"{timestamp} {msg}\n"
                f.write(line)
                f.flush()
                print(f"[WRITE] {line.strip()}")
                time.sleep(interval)
    except KeyboardInterrupt:
        print("\n[INFO] 로그 생성 중단됨")

if __name__ == "__main__":
    generate_log(LOG_PATH, INTERVAL)