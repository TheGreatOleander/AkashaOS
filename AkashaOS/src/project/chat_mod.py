def init(memory):
    memory['chat_mod'] = {"history": []}
    print("[chat_mod] Chat module initialized.")

def save(memory):
    print("[chat_mod] Chat history saved.")

def loop(memory):
    user_input = input("[You] > ")
    memory['chat_mod']['history'].append(user_input)
    print(f"[chat_mod] AI says: I'm thinking about '{user_input}'...")