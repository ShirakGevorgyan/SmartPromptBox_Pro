# SmartPromptBox Pro

&#x20; &#x20;

AI-ով աշխատող **Telegram Bot**՝ տրամադրության վրա հիմնված երգերի/ֆիլմերի առաջարկներով, LLM-զրույցով հիշողությամբ, նկարի գեներացիայով և ամբողջական **CI/CD** հոսքով։

> README_AM-ը **Հայերեն** է։ Անգլերեն տարբերակը նույնպես ներառված է repository-ում։

---

## Բովանդակություն

- [Ակնարկ](#-ակնարկ)
- [Հատկություններ](#-հատկություններ)
- [Ճարտարապետություն](#-ճարտարապետություն)
- [Տեխնոլոգիաներ](#-տեխնոլոգիաներ)
- [Թղթապանակների կառուցվածք](#-թղթապանակների-կառուցվածք)
- [Նախապայմաններ](#-նախապայմաններ)
- [Շրջապատի փոփոխականներ (.env)](#-շրջապատի-փոփոխականներ-env)
- [Արագ գործարկում (Տեղային)](#-արագ-գործարկում-տեղային)
- [Docker / Compose](#-docker--compose)
- [Makefile (ըստ ցանկության)](#-makefile-ըստ-ցանկության)
- [Սլեշ հրամաններ](#-սլեշ-հրամաններ)
- [Թեստավորում](#-թեստավորում)
- [CI (GitHub Actions)](#-ci-github-actions)
- [CD (Self-hosted)](#-cd-self-hosted)
- [DevOps / Ansible Deploy](#-devops--ansible-deploy)
- [Սքրինշոթեր](#-սքրինշոթեր)
- [Տվյալների շերտ](#-տվյալների-շերտ)
- [FSM վիճակներ](#-fsm-վիճակներ)
- [Առողջություն / Smoke](#-առողջություն--smoke)
- [Միջանկյալներ](#-միջանկյալներ)
- [Անվտանգություն](#-անվտանգություն)
- [Տարբերակավորում և Թողարկումներ](#-տարբերակավորում-և-թողարկումներ)
- [Խափանումների ուղեցույց](#-խափանումների-ուղեցույց)
- [ՀՏՀ](#-հթհ)
- [Ցանկալի բարելավումներ](#-ցանկալի-բարելավումներ)
- [Ներդրումներ](#-ներդրումներ)
- [Լիցենզիա](#-լիցենզիա)

---

## 📌 Ակնարկ

**SmartPromptBox Pro** — մոդուլային Telegram bot՝ գործնական, բարձր որակի AI հնարավորություններով․

- Ընտրում ես **տրամադրություն**, անմիջապես ստանում ես **երգեր, ֆիլմեր, մեջբերումներ**, նաև **նկարի prompt-ներ**։
- **Հիշողությամբ զրույց**՝ SQLite-ի վրա՝ կոնտեքստի պահպանումով։
- **Նկարի գեներացիա**՝ պարզ տեքստային հրահանգներից։
- Վստահ deploy՝ խիստ **CI** (lint, types, security, tests, build) և ավտոմատ **CD**։

---

## ✨ Հատկություններ

- **🧠 Mood Assistant** — տրամադրություն ընտրելուց հետո bot-ը առաջարկում է՝
  - 5 երգ, 5 ֆիլմ, 5 մեջբերում
  - 2 նկարի prompt (+ կամընտրով գեներացիա)
- **🎵 Երգեր** — թեմատիկ հավաքածուներ և արագ առաջարկներ (YouTube հղումներով)
- **🎬 Ֆիլմեր և Սերիալներ** — ըստ ժանրի/վերնագրի/տրամադրության, հարուստ քարտերով
- **🤖 GPT Զրույց հիշողությամբ** — զրույցները պահվում են SQLite-ում՝ կոնտեքստի համար
- **🎨 Նկար գեներացիա** — պատկերներ տեքստային prompt-ներից
- **🧪 Թեստեր** — unit / integration / e2e + input-sanitization
- **🐳 Dockerized** — dev/prod պատկերներ + Compose, healthcheck-երով
- **⚙️ CI/CD** — ruff + mypy + pip-audit + unit tests + Docker build + Compose smoke; Telegram նոտիֆիկացիաներ

---

## 🧱 Ճարտարապետություն

**Բարձր մակարդակի բաղադրիչներ**

- `telegram_bot/` — aiogram v3 հավելված (routers, handlers, keyboards)
- `llm/` — LLM adapters (mood inference, songs/movies/series pickers, image gen)
- `data/` — մոդելներ և հիշողության persistence
- `utils/` — օգնական գործիքներ (retry, summarizer, logging)
- `devops/` — Dockerfile-ներ, Compose stacks, Ansible deploy

**Հոսք**

1. Օգտատերը սեղմում է մենյուի կոճակը (օր․ *Mood Assistant*).
2. Handler-ը ստուգում է input-ը → կանչում է LLM/կամ curated provider (retry-ով).
3. Պատասխանը ձևաչափվում է և ուղարկվում է Telegram.
4. Զրույցի դեպքում՝ մեսիջները պահվում են **UserMemory**-ում և ըստ կարիքի՝ ամփոփվում։

---

## 📦 Տեխնոլոգիաներ

- **Python 3.10**, **aiogram 3**, **OpenAI API**
- **SQLAlchemy + SQLite**
- **Docker / Docker Compose**
- **GitHub Actions**

---

## 🗂️ Թղթապանակների կառուցվածք

```text
app/
  __init__.py
  main.py
  meta.py
  states/
    __init__.py
    gpt_states.py
  scripts/
    __init__.py
    init_db.py
  data/
    __init__.py
    database.py
    db_session_tracker.py
    memory_service.py
    models/
      __init__.py
      base.py
      memory_model.py
      session_model.py
  llm/
    __init__.py
    assistant.py
    song_llm.py
    movie_picker.py
    series_picker.py
    mood_inferencer.py
    image_generator.py
    img_generator.py
    text_utils.py
  telegram_bot/
    __init__.py
    bot.py
    menu.py
    handlers/
      gpt_memory_chat_handler.py
      img_handler.py
      misc_commands.py
      mood_handler.py
      movie_menu_handler.py
      random_songs_handler.py
      series_menu_handler.py
    middlewares/
      __init__.py
      errors.py
      logging.py
      request_id.py
  utils/
    __init__.py
    logging_config.py
    retry.py
    summarizer.py
    trivial_check.py

devops/
  ansible/
    ansible.cfg
    inventory/hosts.ini
    playbooks/deploy.yml
    roles/deploy_app/tasks/main.yml
  compose/
    docker-compose.dev.yml
    docker-compose.prod.yml
  docker/
    app/Dockerfile
    app/Dockerfile.dev

.github/workflows/
  ci.yml
  cd.yml

tests/
  conftest.py
  smoke/
  unit/
    test_data/
    test_llm/
    test_states/
    test_telegram_bot/
    test_utils/
  integration/
    test_handler_llm/
  e2e/
  security/
  regression/
  performance/

root files: requirements.txt, requirements-dev.txt, .env.example, .dockerignore, .gitignore, mypy.ini, README.md
```

---

## ✅ Նախապայմաններ

- **Python 3.10**
- **Telegram Bot Token** (@BotFather)
- **OpenAI API Key**
- **Docker & Docker Compose** (ըստ ցանկության)

---

## 🔐 Շրջապատի փոփոխականներ (.env)

Ստեղծիր `.env` (տես՝ `.env.example`).

| Բանալին                            | Նկարագրություն                   |
| ---------------------------------- | -------------------------------- |
| `OPENAI_API_KEY`                   | OpenAI գաղտնաբառ                 |
| `TELEGRAM_BOT_TOKEN`               | Հիմնական bot token               |
| `TELEGRAM_BOT_TOKEN_TEST_NOTIFIER` | CI/CD notifier token             |
| `TELEGRAM_CHAT_ID`                 | CI/CD լոգերի հասցեատեր           |
| `DATABASE_URL`                     | օրինակ՝ `sqlite:///db/memory.db` |
| `LOG_LEVEL`                        | `INFO` (լռելայն), `DEBUG`        |
| `DISABLE_TELEGRAM`                 | `0`՝ bot-ը միացրած               |
| `BOT_NAME`                         | Ցուցադրվող անունը `/about`-ում   |
| `BOT_VERSION`                      | Տարբերակը `/about`-ում           |

---

## 🚀 Արագ գործարկում (Տեղային)

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # լրացրու բանալիները
python -m app.scripts.init_db   # DB ինիցիալիզացիա (միանգամյա)
python -m app.telegram_bot.bot  # գործարկում bot-ը
```

**Օգտակար հրամաններ**

```bash
ruff .        # lint
mypy app      # typing
PYTHONPATH=. pytest -q  # tests
```

---

## 🐳 Docker / Compose

**Development**

```bash
docker compose -f devops/compose/docker-compose.dev.yml up --build
```

**Production**

```bash
docker compose -f devops/compose/docker-compose.prod.yml up -d --build
```

Նշումներ

- Healthcheck-ի պարզ տարբերակ
  ```dockerfile
  HEALTHCHECK CMD python -c "import app; print('ok')"
  ```
  կամ՝ utility-ով
  ```dockerfile
  HEALTHCHECK CMD python -c "from app.utils.trivial_check import ok; import sys; sys.exit(0 if ok() else 1)"
  ```
- SQLite-ի ֆայլերը mount են `./db/` պանակում

---

## 🧰 Makefile (ըստ ցանկության)

Հարմարության համար՝ repository-ի արմատում ավելացրու `Makefile`.

```Makefile
.PHONY: venv setup run lint type test dev prod logs ps down
venv:
	python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt
setup: venv
	cp -n .env.example .env || true
run:
	python -m app.telegram_bot.bot
lint:
	ruff .
type:
	mypy app
test:
	PYTHONPATH=. pytest -q
dev:
	docker compose -f devops/compose/docker-compose.dev.yml up --build
prod:
	docker compose -f devops/compose/docker-compose.prod.yml up -d --build
logs:
	docker compose -f devops/compose/docker-compose.prod.yml logs -f --tail=200
ps:
	docker compose -f devops/compose/docker-compose.prod.yml ps
down:
	docker compose -f devops/compose/docker-compose.prod.yml down --remove-orphans
```

---

## 🤖 Սլեշ հրամաններ

- `/help` — օգտագործման հակիրճ ուղեցույց
- `/about` — տարբերակ, uptime, Python/aiogram info
- `/ping` — pong
- `/id` — User/Chat ID
- **«Մաքրել չատը»** — վերաբեռնում է ընթացիկ զրույցի հիշողությունը

---

## 🧪 Թեստավորում

Թեստերը `tests/` պանակում են․

- **unit** — առանձին մոդուլներ և utilities
- **integration** — handler + LLM ինտեգրացիա, retry վարք
- **e2e** — հիմնական հոսքեր (mood/songs/movies/series/img)
- **security** — input sanitization
- **performance** — արագագործության չափումներ
- **regression** — FSM/LLM կայունության թեստեր

Օրինակներ

```bash
pip install -r requirements-dev.txt
PYTHONPATH=. pytest -q
PYTHONPATH=. pytest --maxfail=1 --disable-warnings -q
bash tests/run_all_tests.sh
```

---

## 🔁 CI (GitHub Actions)

Workflow: `.github/workflows/ci.yml`

- **Jobs** (երթականությամբ)․
  1. Ruff Lint
  2. Mypy (types)
  3. pip-audit (security)
  4. Ansible Syntax Check
  5. Unit tests + Coverage
  6. Docker Build (dev & prod)
  7. Compose Smoke (config + import sanity)
- **Artifacts**․ ցանկության դեպքում `coverage.xml`, Docker cache, logs
- **Նոտիֆիկացիա**․ Telegram հաղորդագրություն **View CI logs** կոճակով



---

## 🚚 CD (Self-hosted)

Workflow: `.github/workflows/cd.yml`

- **Trigger**․ CI հաջող ավարտից հետո (`main` → deploy)
- **Քայլեր**․ self-hosted runner → pull → env refresh (GitHub Secrets) → `docker compose -f devops/compose/docker-compose.prod.yml up -d --build` → healthcheck
- **Նոտիֆիկացիա**․ Telegram հաղորդագրություն `RUNNING (healthy)` հաստատումով + **View CD logs** հղումով



---

## 🧰 DevOps / Ansible Deploy

- Playbook՝ `devops/ansible/playbooks/deploy.yml`
- Ինվենտորի՝ `devops/ansible/inventory/hosts.ini`
- Ռոլ՝ `roles/deploy_app/tasks/main.yml` (Docker login/build/pull, Compose up)
- CI-ում կատարվում է **Ansible Syntax Check**; CD-ում՝ իրական deploy սերվերին

---

## 🖼️ Սքրինշոթեր

**Սկիզբ / Մենյու**

&#x20; &#x20;

**Mood Assistant → Ընտրություն → Արդյունքներ**

&#x20;&#x20;

**Երգեր**

&#x20;

**Ֆիլմեր և Սերիալներ**

&#x20; &#x20;

**Նկար գեներացիա**

&#x20;

**GPT Զրույց + Մաքրում**

&#x20;

---

## 🧱 Տվյալների շերտ

- Լռելայն `DATABASE_URL`՝ `sqlite:///db/memory.db` (mounted volume)
- Հիմնական մոդել՝ `UserMemory(id, user_id, role, content, user_name, bot_name, last_mood, history)`
- `memory_service.py` — պատմության պահպանում/ընթերցում, ըստ կարիքի ամփոփում
- `db_session_tracker.py` — DB սեսիաների վերահսկում թեստավորման ժամանակ

---

## 🔄 FSM վիճակներ

- `app/states/gpt_states.py` — chatbot-ի FSM transition-ների սահմանումներ

---

## 🩺 Առողջություն / Smoke

- `utils/trivial_check.py` — օգտագործվում է smoke/health-check-ում արագ հաստատման համար

---

## 🛡️ Միջանկյալներ

- `errors.py` — catch-all → user-friendly հաղորդագրություն
- `logging.py`, `request_id.py` — request correlation և structured logs

---

## 🔒 Անվտանգություն

- Գաղտնիքները մի՛ commit արա՝ օգտագործիր **GitHub Secrets** և տեղային `.env` (`.gitignore`)
- Token-ները չեն դուրս գրվում logs-ում
- Input sanitization-ը ծածկված է թեստերով
- Ծանր գործողությունները rate-limit արա (Telegram-ի սահմանափակումները նույնպես գործում են)

---

## 🏷️ Տարբերակավորում և Թողարկումներ

- **SemVer**՝ `MAJOR.MINOR.PATCH`
- **Աղբյուր**՝ `app/meta.py` (`/about`-ում երևացող տարբերակ). ցանկության դեպքում՝ նաև `.env`-ում `BOT_VERSION`
- **Tag & Release**
  ```bash
  git commit -m "chore(release): vX.Y.Z"
  git tag -a vX.Y.Z -m "release vX.Y.Z"
  git push origin main --tags
  ```
  GitHub Release-ում գրանցիր փոփոխությունների ամփոփումը
- **Deploy**՝ CD-ն ավտոմատ է `main`-ի հաջող CI-ից հետո

---

## 🛠️ Խափանումների ուղեցույց

- **Bot-ը չի պատասխանում** → ստուգիր container-ի վիճակը
  ```bash
  docker compose -f devops/compose/docker-compose.prod.yml ps
  docker logs -f compose-app-1 --tail=200
  ```
- **CI հաղորդագրությունը չի գալիս** → հաստատիր chat id-ը `/id`-ով, ստուգիր GitHub Secrets-ը
- **OpenAI 401/429** → 401՝ բանալին սխալ/ժամկետանց է, 429՝ rate limit → backoff
- **Image gen ձախողում** → միացրու image adapter-ը, հաստատիր API բանալին
- **Build failure** → փորձիր տեղում
  ```bash
  docker build . -f devops/docker/app/Dockerfile
  ```
- **Compose config sanity**
  ```bash
  docker compose -f devops/compose/docker-compose.prod.yml config
  ```

---

## ❓ ՀՏՀ

- **Միայն unit թեստե՞ր** → `pytest tests/unit -q`
- **Սքրինշոթերը որտե՞ղ են** → `docs/images/`
- **Ինչպե՞ս փոխեմ մոդելները/պրոմպտերը** → խմբագրիր `app/llm/assistant.py` և հարակից utilities
- **Ինչպե՞ս զրուցի հիշողությունը մաքրեմ** → «Մաքրել չատը» կամ ջնջիր `./db/`-ի SQLite ֆայլը (dev)

---

## 🧩 Ցանկալի բարելավումներ

- Dockerfile healthcheck՝ մեկ տողով ✅
- Pre-commit hooks (ruff + mypy + pytest)
- Observability (մետրիկա/թրեյսինգ)
- Coverage badge + Codecov ինտեգրում

---

## 🙌 Ներդրումներ

PR-ներն ու issue-ները միշտ ողջունելի են․

1. Բացիր նկարագրական issue կամ PR
2. Գործարկիր `ruff`, `mypy`, `pytest`
3. Փոքր, հստակ կոմիտներ

---

## 📜 Լիցենզիա

Ավելացրու `LICENSE` (օր.՝ MIT)
