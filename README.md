# claude-starter-kit

Claude Pro 초보자를 위한 시작 자료와, Claude Code·Codex 공용 리팩터링 규칙(Ponytail 기반)입니다.

| 파일 | 내용 |
|---|---|
| `STARTER.md` | Claude Pro 초보자 스타터팩 (설치, 첫 실행, 자주 쓰는 명령, 안전 수칙) |
| `AGENTS.md` / `CLAUDE.md` | 리팩터링 규칙. Codex는 `AGENTS.md`, Claude Code는 `CLAUDE.md`(이 파일을 가져옴)를 읽습니다 |
| `docs/UIUX-PRO-STRUCTURE.md` | UI/UX Pro Max v2.13.0 구조 조사 |
| `skills/local-router/` | 작은 작업은 로컬 모델로, 나머지는 Claude가 처리하도록 분류하는 스킬 (`~/.claude/skills/`에 복사해서 사용) |
| `analyze.py` + `refs/` | `refs/` 폴더의 파일만 근거로 로컬 Ollama 모델에게 질문 (Python 표준 라이브러리만 사용) |

`analyze.py`는 [Ollama](https://ollama.com)가 켜져 있고 `qwen2.5-coder:3b` 같은 모델이 받아져 있어야 합니다. 모델 없이 `python analyze.py --test`로 자체 점검만 할 수 있습니다.

Ponytail 규칙은 [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail)을 참고해 정리한 것입니다.

## 사용 예시

### 1. 내 프로젝트에 리팩터링 규칙 붙이기
```bash
git clone https://github.com/anotherthingwecan/claude-starter-kit
cp claude-starter-kit/AGENTS.md claude-starter-kit/CLAUDE.md ./내-프로젝트/
cd 내-프로젝트 && claude        # Codex는 codex
```
이후 에이전트에게 이렇게 시킵니다.
```
@src/utils.js 를 리팩터링해줘. 새 의존성은 추가하지 말고, 호출처가 깨지지 않게 해줘.
```
에이전트는 규칙에 따라 호출처를 먼저 찾고, 동작을 고정하는 테스트를 만든 뒤, 가장 작은 변경으로 고치고, 답변 끝에 건너뛴 것과 위험을 적습니다.

### 2. 레퍼런스 파일만 근거로 분석하기
```bash
cp 디자인가이드.md refs/
python analyze.py "이 가이드의 색상과 간격 규칙을 요약해줘"
```
```
주의: 한도 때문에 제외/일부만 사용: 긴파일.md (일부만)     ← 한도를 넘으면 이렇게 알려 줍니다
(모델의 답변)
근거로 쓴 파일: 디자인가이드.md
```
UI/UX Pro Max 검색 결과를 `refs/`에 저장해서 쓰는 방법은 `docs/UIUX-PRO-STRUCTURE.md` 4장에 있습니다.

### 3. 모델 없이 점검만
```bash
python analyze.py --test        # self-check OK 가 나오면 정상
```

## 이걸 쓰면 좋은 점
- **변경이 작아집니다.** 규칙이 "지우기 → 이미 있는 것 쓰기 → 표준 기능 → 한 줄 → 최소 코드" 순서를 강제해서, 요청하지 않은 추상화와 새 의존성이 줄어듭니다.
- **되돌리기 쉽습니다.** 리팩터링 전에 현재 동작을 고정하는 테스트를 먼저 만들고, 이름·구조·동작 변경을 한 커밋에 섞지 않습니다.
- **Claude Code와 Codex가 같은 규칙을 씁니다.** 규칙 본문은 `AGENTS.md` 한 곳에만 있고 `CLAUDE.md`는 그것을 가져옵니다. 한쪽만 고치면 됩니다.
- **답변이 솔직해집니다.** 답변 끝에 건너뛴 것, 확인하지 못한 것, 위험을 적게 합니다.
- **초보자가 바로 따라 할 수 있습니다.** `STARTER.md`는 설치부터 안전 수칙, 프롬프트 틀까지 순서대로 있습니다.
- **레퍼런스 분석은 내 PC에서만 돌아갑니다.** `analyze.py`는 Python 표준 라이브러리만 쓰고, 파일 내용이 외부로 전송되지 않으며, 한도 때문에 잘린 파일을 알려 줍니다. Claude 사용량도 쓰지 않습니다.
- **가볍습니다.** 의존성 설치도, 설정 파일도 없습니다.

## 한계
- 규칙은 에이전트에게 주는 지침이라서 항상 지켜진다는 보장은 없습니다. 결과는 `git diff`로 직접 확인하세요.
- `analyze.py`는 한 번에 약 12,000자까지만 읽고, 3B 같은 작은 모델은 한국어 분석이 얕을 수 있습니다. 중요한 판단은 더 큰 모델에게 맡기세요.
