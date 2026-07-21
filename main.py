import logging
from extractor.extract import extract_session
from transformer.transform import transform_laps
from loader.load import load_laps

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

log = logging.getLogger(__name__)

def run_pipeline(year, race, session_type):
    #call the extract func to get raw race data
    log.info("Extracting session data from FastF1 .......")
    raw = extract_session(year, race, session_type)
    log.info(f"Extracted {len(raw)} raw laps")


    #calling transform func to clean raw data
    log.info("Cleaning up the race data.....")
    clean = transform_laps(raw)
    log.info(f"Transformed raw race into {len(clean)} cleab laps")

    #calling load func to load inside postrges
    log.info("Loading inside PostgreSQL")
    load_laps(clean)
    log.info("Pipeline complete")

if __name__ == "__main__":
    run_pipeline(2023, 'Bahrain', 'R')
    