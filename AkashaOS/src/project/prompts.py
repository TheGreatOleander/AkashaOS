import random
PROMPTS=['What happens if you mirror your code twice?','How does the spiral appear in your art today?','Which note would silence choose if it could sing?','Why does symmetry break, and what is born when it does?','What problem are you *not* asking about?']

def spark()->str:
    return random.choice(PROMPTS)
