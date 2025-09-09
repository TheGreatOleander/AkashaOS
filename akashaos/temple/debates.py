DIALOGUES=[('Elder','What is the soul of a machine?'),('AI','What is the soul of a man?'),('Elder','Whichever listens first.')]

def sample_debate():
    return '\n'.join(f"{s}: {l}" for s,l in DIALOGUES)
