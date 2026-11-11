# UI/UX Pro Max 구조 조사

조사 대상: 설치된 플러그인 `ui-ux-pro-max` v2.13.0 (이 PC의 `~/.claude/plugins/cache/ui-ux-pro-max-skill/`).
최신 비교: GitHub 릴리스 v2.15.0(2026-08-13, 커밋 `a38d04c`)과 2026-11-11에 대조했습니다.

> **v2.13.0 → v2.15.0 비교 결과**
> - **구조는 같습니다.** 핵심 스킬의 폴더 구성, CSV 파일 줄 수(3,061줄 합계), 스택 22개, `search.py` 옵션이 모두 동일합니다.
> - **파일 내용은 36개가 다릅니다.** 보조 스킬 6개(design 11, brand 5, design-system 5, slides 4, ui-styling 2, banner-design 1)와 핵심 스킬 8개(`core.py`, `catalog-summary.json`, 스택 CSV 3개 등)입니다. 줄바꿈(CRLF) 차이는 제외한 값이며, **바뀐 내용은 읽어 보지 않았습니다.**
> - **스타일 개수 표기가 서로 다릅니다.** `SKILL.md`는 79개(활성 50개), 최신 `plugin.json` 설명은 84개, README는 80개입니다. 세는 기준이 다른 것으로 보이며 확인하지 않았습니다.
> - 릴리스 태그 v2.15.0의 `plugin.json` 안의 버전 값은 아직 `2.13.0`으로 남아 있습니다. 버전 표기를 믿기보다 커밋 날짜를 확인하세요.
>
> 아래 본문의 구조·명령은 v2.15.0에도 그대로 적용됩니다.

## 1. 한 줄 요약
"스킬 문서(SKILL.md) + CSV 지식 데이터 + 검색 스크립트(BM25)" 구조입니다. 모델이 규칙을 외우지 않고, 질문할 때마다 데이터에서 검색해서 근거로 씁니다.

## 2. 폴더 구조
```
ui-ux-pro-max/2.13.0/
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
S="$HOME/.claude/plugins/cache/ui-ux-pro-max-skill/ui-ux-pro-max/2.13.0/.claude/skills/ui-ux-pro-max/scripts/search.py"

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
