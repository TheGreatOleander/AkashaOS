"""Demo CLI for AkashaOS AI Guard"""
from ai_guard import AIGuard

def main():
    guard = AIGuard()
    print("=== AkashaOS AI Guard Demo ===")
    user_input = input("Enter your flare phrase: ")
    if guard.authenticate(user_input, "default"):
        print(guard.guard_output("Welcome back, dreamer.", "default"))
    else:
        print("Access denied.")

if __name__ == "__main__":
    main()
