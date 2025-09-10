from modules.curiosity import ask
from modules.codex import reflect
from modules.temple import structure
from modules.veil import reveal

def mirror_loop():
    question = ask()
    codex_response = reflect(question)
    temple_response = structure(codex_response)
    veil_response = reveal(temple_response)
    return veil_response

if __name__ == "__main__":
    print(mirror_loop())
