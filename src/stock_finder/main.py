#!/usr/bin/env python
import sys
import warnings
import time
from tenacity import retry, stop_after_attempt, wait_exponential
from datetime import datetime

from stock_finder.crew import StockFinder

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """
    Run the crew.
    """
    inputs = {
        'sector' : 'Technology',
        "current_date": str(datetime.now())
    }
    
    try:
        time.sleep(5)
        @retry(stop = stop_after_attempt(3), wait = wait_exponential(multiplier=2, min=2, max=5))
        def retry_kickoff_minimal_requests():
            return StockFinder().crew().kickoff(inputs=inputs)
        
        result = retry_kickoff_minimal_requests()
        if result:
            print("============ OUTPUT ==============")
            print(result.raw)
        else:
            print('No result obtained')
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

if __name__ == '__main__': 
    run()

