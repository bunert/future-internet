import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

class Log:
    def __init__(self, n: int):
        self.n = n

    def info(self, msg):
        logging.info(f"[{self.n:02d}] {msg}")