import http.server
import socketserver
import webbrowser
import os
import json
import glob

PORT = 8000
os.chdir(os.path.dirname(os.path.abspath(__file__)))

print("========================================")
print(" Merging Dictionaries (กำลังรวมคลังคำศัพท์)...")
merged_words = set() # ใช้ Set เพื่อป้องกันคำซ้ำอัตโนมัติ

# 1. โหลดไฟล์คำศัพท์หลัก (ถ้ามีอยู่แล้ว)
if os.path.exists('words_dictionary.json'):
    try:
        with open('words_dictionary.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, dict):
                merged_words.update(data.keys())
            elif isinstance(data, list):
                merged_words.update(data)
    except:
        pass

# 2. สร้างโฟลเดอร์สำหรับให้เรา 'โยนไฟล์' ใส่
new_dicts_dir = 'add_words_here'
os.makedirs(new_dicts_dir, exist_ok=True)

# 3. กวาดอ่านทุกไฟล์ในโฟลเดอร์ add_words_here
for filepath in glob.glob(os.path.join(new_dicts_dir, '*')):
    ext = os.path.splitext(filepath)[1].lower()
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            if ext == '.json':
                data = json.load(f)
                if isinstance(data, dict):
                    merged_words.update(data.keys())
                elif isinstance(data, list):
                    merged_words.update(data)
            elif ext == '.txt':
                # รองรับไฟล์ txt แบบพิมพ์ศัพท์บรรทัดละคำ
                words = [line.strip().lower() for line in f if line.strip()]
                merged_words.update(words)
        print(f" [OK] Loaded new words from: {os.path.basename(filepath)}")
    except Exception as e:
        print(f" [Error] reading {filepath}: {e}")

# 4. บันทึกคำศัพท์ทั้งหมดรวมกันเป็นไฟล์เดียวให้เว็บดึงไปใช้
final_dict = {word: 1 for word in merged_words}
with open('words_dictionary.json', 'w', encoding='utf-8') as f:
    json.dump(final_dict, f)

print(f" Total words ready to play: {len(merged_words)}")
print("========================================")

# --- เริ่มรัน Server ให้เกมเล่นได้ ---
Handler = http.server.SimpleHTTPRequestHandler
print(f" Game is running at: http://localhost:{PORT}")
webbrowser.open(f"http://localhost:{PORT}")

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass