import json

transcript_path = r"C:\Users\ayaka\.gemini\antigravity-ide\brain\4860af73-357c-4813-beaf-ac7f347a891c\.system_generated\logs\transcript.jsonl"

keywords = ["blob", "mask", "grayscale-layer", "color-layer"]

with open(transcript_path, "r", encoding="utf-8") as f:
    for line_num, line in enumerate(f, 1):
        try:
            data = json.loads(line)
            content = str(data.get("content", ""))
            tool_calls = str(data.get("tool_calls", ""))
            text_to_search = (content + " " + tool_calls).lower()
            for kw in keywords:
                if kw in text_to_search:
                    print(f"=== Line {line_num} | Step {data.get('step_index')} | Keyword '{kw}' ===")
                    print(content)
                    print("-" * 80)
                    break
        except Exception as e:
            pass

