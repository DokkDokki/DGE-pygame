import logging

def setup_logger():
    logging.basicConfig(
        filename='simulation.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger()

def get_log_content():
    with open("simulation.log", "r") as f:
        return f.read()