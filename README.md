# claude-starter-kit

Claude Pro 초보자를 위한 시작 자료와, Claude Code·Codex 공용 리팩터링 규칙(Ponytail 기반)입니다.

| 파일 | 내용 |
|---|---|
| `STARTER.md` | Claude Pro 초보자 스타터팩 (설치, 첫 실행, 자주 쓰는 명령, 안전 수칙) |
| `AGENTS.md` / `CLAUDE.md` | 리팩터링 규칙. Codex는 `AGENTS.md`, Claude Code는 `CLAUDE.md`(이 파일을 가져옴)를 읽습니다 |
| `docs/UIUX-PRO-STRUCTURE.md` | UI/UX Pro Max v2.13.0 구조 조사 |
| `analyze.py` + `refs/` | `refs/` 폴더의 파일만 근거로 로컬 Ollama 모델에게 질문 (Python 표준 라이브러리만 사용) |

`analyze.py`는 [Ollama](https://ollama.com)가 켜져 있고 `qwen2.5-coder:3b` 같은 모델이 받아져 있어야 합니다. 모델 없이 `python analyze.py --test`로 자체 점검만 할 수 있습니다.

Ponytail 규칙은 [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail)을 참고해 정리한 것입니다.
