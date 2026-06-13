import logging

logging.basicConfig(
    filename="healthcare.log",
    level=logging.INFO,
    format="%(asctime)s %(message)s"
)

logger = logging.getLogger()