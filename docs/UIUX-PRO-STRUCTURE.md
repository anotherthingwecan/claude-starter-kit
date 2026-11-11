# UI/UX Pro Max 구조 조사

조사 대상: 플러그인 `ui-ux-pro-max` (처음 v2.13.0으로 조사하고, 2026-11-11에 v2.15.0으로 올려 다시 확인했습니다). 설치 위치는 `~/.claude/plugins/cache/ui-ux-pro-max-skill/`입니다.

> **v2.13.0 → v2.15.0 변경점** (GitHub `main` 커밋 `6ae86f6`, 2026-11-10 기준으로 직접 대조)
> - **구조는 같습니다.** 핵심 스킬의 폴더 구성, 스택 22개, `search.py`의 기존 옵션이 그대로입니다.
> - **새 옵션 `--rtl`:** 스타일·제품 검색 결과를 오른쪽→왼쪽 언어(RTL) 호환 수준(`full`/`partial`/`caveats`)으로 거를 수 있습니다. `--domain style` 또는 `--domain product`가 필요하고, `--design-system`·`--stack`과는 같이 쓸 수 없습니다. `styles.csv`와 `products.csv`에 `rtl_level` 열이 추가됐습니다.
> - **데이터 갱신:** 스타일 검색 가능 80개(활성 51개), 스택 지침 1,278개(이전 1,271개), Nuxt UI 스택 4.12.0으로 상향, UX 지침 1개 추가.
> - **보조 스킬 수정:** Python 스크립트의 파일 인코딩을 UTF-8로 명시, Gemini 이미지 모델 ID를 환경변수(`GEMINI_FLASH_IMAGE_MODEL`, `GEMINI_PRO_IMAGE_MODEL`)로 바꿀 수 있게 함, 생성 실패 시 종료 코드 개선, 아이콘 SVG 크기 처리 수정.
> - **안전성:** 바뀐 코드에 새로 추가된 `subprocess`, `eval`, 네트워크 호출은 없었습니다. 차이가 난 파일 전체를 읽지는 않았고, 코드 파일과 데이터 파일의 변경분을 훑어봤습니다.
> - **주의:** GitHub의 릴리스 태그 `v2.15.0`(2026-08-13)은 `main`의 `2.15.0`보다 오래된 내용이라 데이터가 더 낮은 값입니다. 버전 숫자보다 커밋 날짜를 확인하세요.
> - **스타일 개수 표기:** `SKILL.md`, `plugin.json`, README의 숫자가 서로 다릅니다(79·80·84). 세는 기준이 달라 보이며 확인하지 않았습니다.

## 1. 한 줄 요약
"스킬 문서(SKILL.md) + CSV 지식 데이터 + 검색 스크립트(BM25)" 구조입니다. 모델이 규칙을 외우지 않고, 질문할 때마다 데이터에서 검색해서 근거로 씁니다.

## 2. 폴더 구조
```
ui-ux-pro-max/<버전>/
├─ .claude/skills/
│   ├─ ui-ux-pro-max/        ← 핵심 스킬
│   │   ├─ SKILL.md           10단계 우선순위 규칙표 (접근성 → 터치 → 성능 → 스타일 …)
│   │   ├─ data/              CSV 지식 베이스
│   │   ├─ references/        quick-reference.md(256줄), pro-rules.md(117줄)
│   │   └─ scripts/           search.py, design_system.py, core.py, validate_data.py, tests/
│   ├─ design / design-system / ui-styling / brand / slides / banner-design   ← 보조 스킬
├─ .claude-plugin/            plugin.json, marketplace.json
├─ cli/                       npm CLI(uipro), 위 자산을 각 에이전트용으로 설치
├─ src/ stack/ gallery/ preview/ screenshots/ docs/   소스·갤러리·문서
```

## 3. 데이터 규모 (data/ 폴더, 줄 수 = 헤더 포함)
| 파일 | 줄 수 | 내용 |
|---|---|---|
| styles.csv | 89 | 디자인 스타일 |
| colors.csv / products.csv / ui-reasoning.csv | 각 193 | 제품별 팔레트·추론 프로필 |
| typography.csv | 75 | 폰트 조합 |
| google-fonts.csv | 1,935 | 구글 폰트 목록 |
| ux-guidelines.csv | 120 | UX 지침 |
| icons.csv / charts.csv / landing.csv / motion.csv / app-interface.csv / react-performance.csv | 106 / 26 / 35 / 18 / 33 / 45 | 아이콘, 차트, 랜딩, 모션 등 |
| stacks/*.csv | 22개 | React, Next.js, Vue, SwiftUI, Flutter 등 스택별 규칙 |

## 4. 우리 쪽에서 쓰는 법: 검색 결과를 레퍼런스로 저장
`search.py`는 질문을 받아 관련 행만 뽑아 줍니다. 그 출력을 `refs/`에 저장하면 `analyze.py`가 그 파일만 근거로 로컬 모델에게 분석시킵니다.

```bash
S="$HOME/.claude/plugins/cache/ui-ux-pro-max-skill/ui-ux-pro-max/2.15.0/.claude/skills/ui-ux-pro-max/scripts/search.py"

# 디자인 시스템 추천을 마크다운으로 저장
python "$S" "핀테크 대시보드" --design-system --format markdown > refs/fintech-ds.md

# 도메인 검색 결과 저장 (ux, style, color, typography, chart, landing …)
python "$S" "모바일 폼 접근성" --domain ux -n 10 > refs/form-ux.md

python analyze.py "refs의 내용만 보고 폼 화면에서 먼저 고칠 것 3가지를 알려줘"
```
`--persist`를 쓰면 `design-system/<프로젝트>/MASTER.md`로 저장되며, 그 파일을 `refs/`에 복사해도 됩니다.

## 5. 한계
- 로컬 3B 모델은 한 번에 약 12,000자까지만 읽습니다(`analyze.py`의 `MAX_CHARS`). 넘으면 질문과 관련 있는 파일 순으로 채우고 나머지는 제외하며 경고를 출력합니다.
- 3B 모델은 한국어 분석 품질이 제한적입니다. 중요한 판단은 Claude에게 맡기세요.
- 위 `search.py` 옵션은 스크립트의 `--help` 기준으로 정리했으며, 이 문서의 명령을 모두 실행해 본 것은 아닙니다.
