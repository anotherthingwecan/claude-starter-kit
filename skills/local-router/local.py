#!/usr/bin/env python3
"""로컬 Ollama 모델에게 한 번 묻고 답만 출력한다.

사용: python local.py "지시" [--model qwen2.5-coder:3b]      (코드·텍스트는 --stdin 으로 넘김)
      python local.py --test                                  (Ollama 연결 점검)
실패하면 종료 코드 1과 이유를 stderr에 낸다. 호출한 쪽이 직접 처리로 돌아가라는 신호다.
"""
import argparse, json, sys, urllib.request

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
sys.stdin.reconfigure(encoding="utf-8")


def ask(prompt, model, host="http://localhost:11434"):
    body = json.dumps({"model": model, "prompt": prompt, "stream": False,
                       "options": {"num_ctx": 4096, "temperature": 0.2}}).encode()
    req = urllib.request.Request(host + "/api/generate", body, {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.load(r)["response"].strip()


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("instruction", nargs="?")
    ap.add_argument("--model", default="qwen2.5-coder:3b")
    ap.add_argument("--stdin", action="store_true", help="표준입력의 내용을 지시 뒤에 붙인다")
    ap.add_argument("--test", action="store_true")
    a = ap.parse_args()
    if a.test:
        try:
            assert ask("Reply with the single word: ok", a.model), "빈 응답"
        except Exception as e:
            sys.exit(f"점검 실패: {e}")
        print("local router OK"); sys.exit()
    if not a.instruction:
        ap.error("지시를 입력하세요")
    piped = sys.stdin.read() if a.stdin else ""  # 입력을 안 줬을 때 멈추지 않도록 명시한 경우에만 읽음
    try:
        out = ask(a.instruction + ("\n\n" + piped if piped else ""), a.model)
    except Exception as e:  # 연결 실패, 모델 없음, 시간 초과 모두 같은 신호로 처리
        sys.exit(f"로컬 모델 호출 실패: {e}")
    print(out)
