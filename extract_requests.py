import json

transcript_path = r"C:\Users\ayaka\.gemini\antigravity-ide\brain\4860af73-357c-4813-beaf-ac7f347a891c\.system_generated\logs\transcript.jsonl"

with open(transcript_path, "r", encoding="utf-8") as f:
    for line_num, line in enumerate(f, 1):
        try:
            data = json.loads(line)
            if data.get("source") == "USER_EXPLICIT" and data.get("type") == "USER_INPUT":
                content = str(data.get("content", ""))
                # Print step index and first 300 characters of the content
                print(f"=== Step {data.get('step_index')} (Line {line_num}) ===")
                print(content[:300].strip())
                if len(content) > 300:
                    print("... [TRUNCATED] ...")
                print("-" * 50)
        except Exception as e:
            pass

