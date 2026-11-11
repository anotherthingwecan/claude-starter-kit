# Claude Pro 초보자 스타터팩

Claude Pro 구독만 있으면 Claude Code(터미널 코딩 에이전트)를 쓸 수 있습니다. 15분 안에 끝나는 순서입니다.

## 1. 준비 (한 번만)
1. Claude Pro 계정으로 로그인 가능한지 확인합니다.
2. Git을 설치합니다: `winget install Git.Git`
3. Claude Code를 설치합니다. 설치 방법은 공식 안내를 따르세요(Windows는 winget 또는 공식 설치 스크립트). 설치 후 터미널에서 `claude --version`이 나오면 성공입니다.

## 2. 첫 실행
```bash
mkdir my-first && cd my-first
git init
claude
```
처음이면 브라우저가 열리고 Claude 계정으로 로그인합니다. 이후 `claude`만 치면 됩니다.

## 3. 이 저장소의 규칙 붙이기 (Ponytail 리팩터링 규칙)
내 프로젝트 폴더에 `AGENTS.md`와 `CLAUDE.md`를 복사합니다.
```bash
cp path/to/local-llm-coding-assistant/AGENTS.md path/to/local-llm-coding-assistant/CLAUDE.md .
```
Ponytail 플러그인까지 쓰려면 Claude Code 안에서 **두 줄을 따로** 입력합니다.
```
/plugin marketplace add DietrichGebert/ponytail
```
```
/plugin install ponytail@ponytail
```
Codex 사용자는 터미널에서:
```bash
codex plugin marketplace add DietrichGebert/ponytail
codex plugin add ponytail@ponytail
```
설치 후 Codex에서 `/hooks`를 열어 훅 2개를 신뢰하고 새 스레드를 시작합니다.

## 4. 매일 쓰는 것
| 하고 싶은 일 | 입력 |
|---|---|
| 작업 시켜보기 | `README를 읽고 이 프로젝트가 뭘 하는지 3줄로 설명해줘` |
| 파일 지정 | `@파일명 을 보고 버그를 찾아줘` |
| 셸 명령 직접 실행 | 맨 앞에 `!` (예: `! git status`) |
| 도움말 | `/help` |
| 대화 길어졌을 때 | `/compact` |
| 새 대화 | `/clear` |
| 코드 검토 | `/code-review` |
| 되돌리기 | 에이전트가 고친 뒤 `git diff`로 확인, 마음에 안 들면 `git restore .` |

## 5. 초보자 안전 수칙
- 작업 전에 `git commit`으로 저장해 두세요. 언제든 되돌릴 수 있습니다.
- 권한 요청이 뜨면 읽고 허용하세요. 무슨 명령인지 모르겠으면 거절하고 "이게 뭐 하는 명령이야?"라고 물어보세요.
- `.env`, 비밀번호, API 키는 대화에 붙여 넣지 마세요.
- 한 번에 큰 요청 하나보다 작은 요청 여러 개가 정확합니다.

## 6. 프롬프트 틀
```
목표: (한 문장)
대상 파일: @파일명
제약: 새 의존성 추가 금지, 기존 스타일 유지
완료 조건: 테스트 통과
```

## 7. 사용량 한도
Pro는 사용 한도가 있어서 긴 작업을 반복하면 잠시 막힐 수 있습니다. 간단한 질문은 Ollama로 돌리는 로컬 모델(Qwen2.5-Coder 3B 등)에 맡기면 한도를 아낄 수 있습니다. `analyze.py`가 그 모델을 씁니다.
