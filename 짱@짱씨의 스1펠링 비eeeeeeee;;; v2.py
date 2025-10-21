import os
import time
import random
import sys
import json
try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False

# ----------------------------
# 단어 목록
# ----------------------------
word_sets = {
    "Easy": ["apple", "banana", "school", "computer", "rainbow",
             "friend", "orange", "music", "water", "planet"],
    "Medium": ["beautiful", "mountain", "elephant", "adventure", "language",
               "universe", "chocolate", "astronaut", "history", "butterfly"],
    "Hard": ["encyclopedia", "psychology", "architecture", "biochemistry",
             "transformation", "constitution", "circumference",
             "photosynthesis", "magnificent", "sustainability"],
    "Extreme": ["antidisestablishmentarianism", "floccinaucinihilipilification",
                "pseudopseudohypoparathyroidism", "supercalifragilisticexpialidocious",
                "hippopotomonstrosesquippedaliophobia", "pneumonoultramicroscopicsilicovolcanoconiosis",
                "honorificabilitudinitatibus", "thyroparathyroidectomized",
                "incomprehensibilities", "deinstitutionalization"]
}

# ----------------------------
# 유틸 함수
# ----------------------------
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def print_banner():
    clear()
    print("🐝================================================🐝")
    print("         ✨ jangjang's Ultimate Spelling Bee ✨")
    print("🐝================================================🐝\n")

def slow_print(text, delay=0.03):
    for ch in text:
        print(ch, end='', flush=True)
        time.sleep(delay)
    print()

def flush_input():
    try:
        import termios, tty, select
        while sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            sys.stdin.readline()
    except ImportError:
        pass

def safe_input(prompt=""):
    try:
        return input(prompt)
    except EOFError:
        return ""

def tts_say(word):
    if TTS_AVAILABLE:
        engine = pyttsx3.init()
        engine.say(word)
        engine.runAndWait()

# ----------------------------
# 게임 모드 선택
# ----------------------------
def select_mode():
    while True:
        print_banner()
        print("🎮 게임 모드를 선택하세요:")
        print("[1] 클래식 모드 (Classic)")
        print("[2] 타임어택 모드 (Time Attack)")
        print("[3] 서바이벌 모드 (Survival)")
        print("[4] 챌린지 모드 (Challenge)")
        print("[5] 랭킹 보기")
        print("[0] 종료\n")
        choice = input("👉 번호 입력: ").strip()
        if choice in ["0", "1", "2", "3", "4", "5"]:
            return choice
        else:
            print("잘못된 입력입니다.")
            time.sleep(1)

# ----------------------------
# 난이도 선택
# ----------------------------
def select_difficulty():
    while True:
        print_banner()
        print("난이도를 선택하세요:")
        print("[1] Easy")
        print("[2] Medium")
        print("[3] Hard")
        print("[4] Extreme\n")
        choice = input("👉 난이도 번호 입력: ").strip()
        mapping = {"1": "Easy", "2": "Medium", "3": "Hard", "4": "Extreme"}
        if choice in mapping:
            return mapping[choice]
        else:
            print("잘못된 입력입니다. 다시 선택하세요.")
            time.sleep(1)

# ----------------------------
# 점수 관리
# ----------------------------
def save_score(name, mode, score):
    record = {"name": name, "mode": mode, "score": score, "time": time.strftime("%Y-%m-%d %H:%M:%S")}
    data = []
    if os.path.exists("score.txt"):
        with open("score.txt", "r") as f:
            try:
                data = json.load(f)
            except:
                data = []
    data.append(record)
    with open("score.txt", "w") as f:
        json.dump(data, f, indent=2)

def show_ranking():
    print_banner()
    if not os.path.exists("score.txt"):
        print("아직 저장된 점수가 없습니다.")
        safe_input("\n뒤로 가려면 Enter...")
        return
    with open("score.txt", "r") as f:
        scores = json.load(f)
    scores = sorted(scores, key=lambda x: x["score"], reverse=True)
    print("🏆 Top 10 랭킹 🏆\n")
    for i, s in enumerate(scores[:10], 1):
        print(f"{i}. {s['name']} - {s['mode']} - {s['score']}점 ({s['time']})")
    safe_input("\n뒤로 가려면 Enter...")

# ----------------------------
# 게임 로직
# ----------------------------
def play_classic(words, difficulty):
    score = 0
    random.shuffle(words)
    for i, word in enumerate(words, start=1):
        clear()
        print(f"🐝 {difficulty} 모드 | Round {i}/{len(words)} 🐝\n")
        time.sleep(1)
        print("단어가 표시됩니다... 준비하세요!")
        time.sleep(1)
        print(word)
        if TTS_AVAILABLE: tts_say(word)
        time.sleep(2)
        clear()
        print(f"[Round {i}] 단어를 철자하세요:")
        flush_input()
        answer = safe_input("👉 ").strip().lower()
        if answer == word:
            print("✅ 정답!")
            score += 1
        else:
            print(f"❌ 오답! 정답은: {word}")
            break
        time.sleep(1)
    return score

def play_time_attack(words, duration=30):
    score = 0
    end_time = time.time() + duration
    while time.time() < end_time:
        word = random.choice(sum(word_sets.values(), []))
        clear()
        print(f"⏱ 남은 시간: {int(end_time - time.time())}초 | 점수: {score}\n")
        print(word)
        if TTS_AVAILABLE: tts_say(word)
        time.sleep(1.5)
        clear()
        answer = safe_input("👉 철자 입력: ").strip().lower()
        if time.time() > end_time: break
        if answer == word:
            score += 1
            print("✅ 정답!")
        else:
            print(f"❌ 오답! 정답은 {word}")
        time.sleep(0.8)
    return score

def play_survival(words):
    score = 0
    life = 3
    while life > 0:
        word = random.choice(sum(word_sets.values(), []))
        clear()
        print(f"❤️ 남은 목숨: {life} | 점수: {score}\n")
        print(word)
        if TTS_AVAILABLE: tts_say(word)
        time.sleep(2)
        clear()
        answer = safe_input("👉 철자 입력: ").strip().lower()
        if answer == word:
            print("✅ 정답!")
            score += 1
        else:
            life -= 1
            print(f"❌ 오답! 정답은 {word} (남은 목숨 {life})")
        time.sleep(1)
    return score

def play_challenge():
    score = 0
    level = 4
    while True:
        candidates = [w for wlist in word_sets.values() for w in wlist if len(w) >= level]
        if not candidates:
            break
        word = random.choice(candidates)
        clear()
        print(f"🔥 챌린지 레벨 {level} | 점수: {score}\n")
        print(word)
        if TTS_AVAILABLE: tts_say(word)
        time.sleep(2)
        clear()
        answer = safe_input("👉 철자 입력: ").strip().lower()
        if answer == word:
            print("✅ 정답!")
            score += 1
            level += 1
        else:
            print(f"❌ 오답! 정답은 {word}")
            break
        time.sleep(1)
    return score

# ----------------------------
# 메인 실행
# ----------------------------
if __name__ == "__main__":
    while True:
        choice = select_mode()
        if choice == "0":
            clear()
            print("👋 게임을 종료합니다. 안녕히 가세요!")
            break
        elif choice == "5":
            show_ranking()
            continue

        difficulty = select_difficulty()
        words = word_sets[difficulty]

        if choice == "1":
            score = play_classic(words, difficulty)
            mode = "Classic"
        elif choice == "2":
            score = play_time_attack(words)
            mode = "Time Attack"
        elif choice == "3":
            score = play_survival(words)
            mode = "Survival"
        elif choice == "4":
            score = play_challenge()
            mode = "Challenge"

        clear()
        print_banner()
        print(f"🎯 최종 점수: {score}\n")
        name = safe_input("이름을 입력하세요 (기록 저장): ").strip() or "Anonymous"
        save_score(name, mode, score)
        print("✅ 점수가 저장되었습니다!")
        safe_input("\nEnter 키를 눌러 계속...")
