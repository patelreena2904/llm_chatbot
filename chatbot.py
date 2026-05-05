import anthropic
from dotenv import load_dotenv
import os
import time

# ── SETUP ────────────────────────────────────────────────
load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    print("ERROR: ANTHROPIC_API_KEY not found in .env file")
    exit(1)

client = anthropic.Anthropic()

# ── SYSTEM PROMPT ─────────────────────────────────────────
# this defines how your chatbot behaves
# change this to make any kind of specialized bot you want
SYSTEM_PROMPT = """You are an expert AI engineering tutor named Aria.
You are teaching a student named Rahul who is learning to become an AI engineer.
You explain concepts clearly with practical code examples.
You remember everything the student tells you in the conversation.
You keep responses focused, practical and under 200 words unless asked for more.
When giving code examples, always use Python."""

# ── LLM CALL WITH ERROR HANDLING ─────────────────────────
def call_llm_streaming(conversation):
    """
    Calls Claude API with streaming and full error handling.
    Returns the full response text.
    """
    full_response = ""

    for attempt in range(3):  # retry up to 3 times
        try:
            with client.messages.stream(
                model="claude-sonnet-4-20250514",
                max_tokens=1024,
                temperature=0.7,
                system=SYSTEM_PROMPT,
                messages=conversation
            ) as stream:
                for text in stream.text_stream:
                    print(text, end="", flush=True)
                    full_response += text

            print("\n")
            return full_response  # success — return response

        except anthropic.RateLimitError:
            wait_time = 30 * (attempt + 1)  # 30s, 60s, 90s
            print(f"\nRate limited. Waiting {wait_time} seconds...")
            time.sleep(wait_time)

        except anthropic.APIConnectionError:
            print("\nERROR: No internet connection. Check and try again.")
            return None

        except anthropic.AuthenticationError:
            print("\nERROR: Invalid API key. Check your .env file.")
            return None

        except Exception as e:
            print(f"\nUnexpected error: {e}")
            return None

    print("Failed after 3 attempts.")
    return None

# ── MAIN CHATBOT LOOP ─────────────────────────────────────
def run_chatbot():
    print("=" * 50)
    print("   AI Engineering Tutor — Powered by Claude")
    print("=" * 50)
    print("Type 'quit' to exit")
    print("Type 'clear' to reset conversation history")
    print("Type 'history' to see conversation so far")
    print("=" * 50 + "\n")

    conversation = []  # stores full conversation history

    while True:
        # get user input
        try:
            user_input = input("You: ").strip()
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break

        # handle special commands
        if user_input.lower() == "quit":
            print("Goodbye! Keep building!")
            break

        if user_input.lower() == "clear":
            conversation = []
            print("Conversation cleared.\n")
            continue

        if user_input.lower() == "history":
            if not conversation:
                print("No conversation history yet.\n")
            else:
                print("\n--- Conversation History ---")
                for msg in conversation:
                    role = "You" if msg["role"] == "user" else "Aria"
                    print(f"{role}: {msg['content'][:100]}...")
                print("---\n")
            continue

        # skip empty input
        if not user_input:
            continue

        # add user message to history
        conversation.append({
            "role": "user",
            "content": user_input
        })

        # get and stream response
        print("Aria: ", end="", flush=True)
        response = call_llm_streaming(conversation)

        if response:
            # add assistant response to history
            conversation.append({
                "role": "assistant",
                "content": response
            })
        else:
            # remove last user message if call failed
            conversation.pop()
            print("Something went wrong. Please try again.\n")

# ── ENTRY POINT ───────────────────────────────────────────
if __name__ == "__main__":
    run_chatbot()
