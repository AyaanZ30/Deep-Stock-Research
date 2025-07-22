#!/usr/bin/env python
import sys
import warnings
import time

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
        time.sleep(30)
        result = StockFinder().crew().kickoff(inputs=inputs)
        if result:
            print("============ OUTPUT ==============")
            print(result.raw)
        else:
            print('No result obtained')
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

if __name__ == '__main__': 
    run()

