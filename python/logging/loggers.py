"""
- INFO 레벨 이상의 로그를 콘솔에 출력합니다.
- 모든 레벨의 로그를 debug.log에 저장합니다.
- ERROR 이상의 로그를 error.log에 저장합니다.
- 모든 Exception을 suppress하고, stacktrace를 error.log에 저장합니다.
- 로그가 발생한 시간과 로그레벨, 모듈명이 명시되어야합니다.
"""

import logging

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG) # 모든 레벨의 로그를 핸들러에게 전달해야 함

formatter = logging.Formatter('%(asctime)s:%(module)s:%(levelname)s:%(message)s', '%Y-%m-%d %H:%M:%S')

# INFO 레벨 이상의 로그를 콘솔에 출력
console_handler = logging.StreamHandler()
console_handler.setLevel(level=logging.INFO)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# 모든 레벨의 로그를 debug.log 에 저장
debug_handler = logging.FileHandler(filename="./python/logging/logs/debug.log")
debug_handler.setFormatter(formatter)
debug_handler.setLevel(level=logging.DEBUG)
logger.addHandler(debug_handler)

# ERROR 이상의 로그를 error.log에 저장
error_handler = logging.FileHandler(filename="./python/logging/logs/error.log")
error_handler.setFormatter(formatter)
error_handler.setLevel(logging.ERROR)
logger.addHandler(error_handler)