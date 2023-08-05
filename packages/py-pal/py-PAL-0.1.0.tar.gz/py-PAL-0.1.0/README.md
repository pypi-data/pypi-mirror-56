# pyPAL - Python Performance Analysis Library
## Setup
This project requires CPython to run.
Install Python >= 3.7, then install pyPAL by running:

    pip install pypal

## Usage
Calling pyPAL as module:

    pyPAL file.py   

Using the decorator:

    @profile
    def test():
        pass

Using the context manager:

    with Tracer() as t:
        start_game()

Using the API:

    t = Tracer()
    t.trace()
    
    # Your function
    run()
    
    t.stop()
    estimator = ComplexityEstimator(tracer)
    res = estimator.export()
    
    # Do something with the resulting DataFrame
    print(res)
    