import os, time, json
import openai

# 環境変数から取得（またはconfig.jsonで読み込んでもOK）
openai.api_key = os.getenv("OPENAI_API_KEY")

TARGET_FILE = "../workspace/target_code.py"
INSTRUCTION_FILE = "../instructions/instruction.json"

while True:
    if not os.path.exists(INSTRUCTION_FILE):
        time.sleep(2)
        continue

    with open(INSTRUCTION_FILE, "r") as f:
        instruction = json.load(f).get("instruction", "")

    with open(TARGET_FILE, "r") as f:
        original_code = f.read()

    prompt = (
        f"次のPythonコードを以下の指示に従って編集してください：\n\n"
        f"[元のコード]\n{original_code}\n\n"
        f"[指示]\n{instruction}\n\n"
        f"[編集後の完全なコードを出力してください]"
    )

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    edited_code = response.choices[0].message.content

    with open(TARGET_FILE, "w") as f:
        f.write(edited_code)

    print(">> コードを更新しました。")
    os.remove(INSTRUCTION_FILE)
