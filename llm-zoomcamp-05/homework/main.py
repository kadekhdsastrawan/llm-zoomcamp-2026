import os
from dotenv import load_dotenv

def main():
    load_dotenv()
    print(f"OPEN AI API KEY: {os.getenv("OPENAI_API_KEY")}")
    # print("Hello from homework!")


if __name__ == "__main__":
    main()