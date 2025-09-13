import time
from ai_guard import AIGuard

def main():
    user_id = input("Enter user ID: ")
    guard = AIGuard(user_id)

    print("Simulate input steps. Enter delays in seconds separated by spaces (e.g., 0.5 0.7 0.4):")
    inp = input("Timings: ")
    try:
        timings = list(map(float, inp.strip().split()))
    except:
        print("Invalid input.")
        return

    score = guard.score_attempt(timings)
    print(f"AI Guard score: {score}")

    if score > 70:
        print("✅ Login allowed")
    elif score > 50:
        print("⚠️ Medium confidence: require additional verification")
    else:
        print("❌ Login blocked")

    guard.update_profile(timings)
    print("Profile updated.")

if __name__ == "__main__":
    main()
