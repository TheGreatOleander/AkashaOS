NUDGES=['Pause and breathe. Alignment comes in silence.','Write down what you seek, then listen for the echo.','Clarity prefers small steps.','Every problem is a riddle in disguise.']

def gentle_nudge(seed:int=0)->str:
    return NUDGES[seed%len(NUDGES)]
