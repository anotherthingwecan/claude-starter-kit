#!/usr/bin/env python3
"""refs/ 폴더의 파일만 근거로 로컬 Ollama 모델에게 질문한다.

사용: python analyze.py "이 레퍼런스의 색상 규칙을 요약해줘" [--model qwen2.5-coder:3b] [--dir refs]
"""
import argparse, json, pathlib, re, sys, urllib.request

SUFFIXES = {".md", ".txt", ".csv", ".json", ".html", ".css", ".js", ".ts", ".tsx", ".py", ".yaml", ".yml"}
# shortcut: 글자 수로 자르고 키워드로 순위만 매김, 파일이 많아지면 임베딩 검색(RAG)으로 교체
MAX_CHARS = 12000  # num_ctx 8192 토큰에 한글 포함해 여유를 둔 값


def load_refs(folder):
    files = [p for p in sorted(pathlib.Path(folder).rglob("*")) if p.is_file() and p.suffix.lower() in SUFFIXES and p.name != "README.md"]
    return [(p, p.read_text(encoding="utf-8", errors="replace")) for p in files]


def pick(refs, question):
    words = set(re.findall(r"\w{2,}", question.lower()))
    score = lambda item: -sum(item[1].lower().count(w) for w in words)
    chosen, used, skipped = [], 0, []
    for path, text in sorted(refs, key=score):
        room = MAX_CHARS - used
        if room < 500:
            skipped.append(path.name)
            continue
        chosen.append((path.name, text[:room]))
        used += min(len(text), room)
        if len(text) > room:
            skipped.append(path.name + " (일부만)")
    return chosen, skipped


def build_prompt(chosen, question):
    docs = "\n\n".join(f"### 파일: {name}\n{text}" for name, text in chosen)
    return ("아래 레퍼런스 파일의 내용만 근거로 답하세요. 파일에 없는 내용은 '레퍼런스에 없음'이라고 쓰고, "
            "답변 끝에 근거로 쓴 파일 이름을 적으세요.\n\n" + docs + "\n\n질문: " + question)


def ask(model, prompt, host="http://localhost:11434"):
    body = json.dumps({"model": model, "prompt": prompt, "stream": False, "options": {"num_ctx": 8192, "temperature": 0.2}}).encode()
    req = urllib.request.Request(host + "/api/generate", body, {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=600) as r:
        return json.load(r)["response"]


def self_check():
    refs = [(pathlib.Path("a.md"), "색상 팔레트 파랑 " * 3), (pathlib.Path("b.md"), "폰트 규칙 " * 3000)]
    chosen, skipped = pick(refs, "색상 팔레트")
    assert chosen[0][0] == "a.md", "질문과 맞는 파일이 먼저여야 함"
    assert sum(len(t) for _, t in chosen) <= MAX_CHARS, "글자 수 한도 초과"
    assert "b.md (일부만)" in skipped, "잘린 파일을 알려야 함"
    print("self-check OK")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("question", nargs="?")
    ap.add_argument("--model", default="qwen2.5-coder:3b")
    ap.add_argument("--dir", default="refs")
    ap.add_argument("--test", action="store_true", help="모델 없이 자체 점검만 실행")
    a = ap.parse_args()
    if a.test:
        self_check(); sys.exit()
    if not a.question:
        ap.error("질문을 입력하세요")
    refs = load_refs(a.dir)
    if not refs:
        sys.exit(f"'{a.dir}' 폴더에 분석할 파일이 없습니다. 레퍼런스 파일을 넣고 다시 실행하세요.")
    chosen, skipped = pick(refs, a.question)
    if skipped:
        print("주의: 한도 때문에 제외/일부만 사용:", ", ".join(skipped), file=sys.stderr)
    try:
        print(ask(a.model, build_prompt(chosen, a.question)))
    except OSError as e:
        sys.exit(f"Ollama에 연결하지 못했습니다 ({e}). Ollama가 켜져 있는지 확인하세요.")
