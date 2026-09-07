# Task 3 — Customer Support Chatbot

A support bot that understands questions in natural language and answers across three channels — web, Telegram, and notebook — all backed by one Dialogflow agent.

---

## The problem

Support teams answer the same questions endlessly: opening hours, order status, refund policy. Keyword matching handles *"what are your hours"* and then falls over on *"when do you open?"* — same question, no shared keywords.

**Dialogflow ES** matches on *intent* rather than wording. Train it with a handful of phrasings and it generalises to the ones you didn't think of.

## Architecture

One agent, three front-ends. Each interface only translates between its own input format and Dialogflow's — all the language understanding lives in the agent, so improving it improves every channel at once.

```
   Streamlit web app  ┐
   Telegram bot       ├──►  detect_intent()  ──►  Dialogflow ES agent
   Colab widget       ┘                              (intents, training
                                                      phrases, responses)
```

**Session IDs** are what let the agent hold a conversation. Dialogflow ties context to a session id, so a follow-up like *"and what about Sundays?"* only resolves if it arrives under the same id as the question before it. Each interface here keeps one id for the life of a conversation.

## The three interfaces

| File | Interface | Best for |
|---|---|---|
| `chatbot_app.py` | Streamlit web app | Demos, embedding on a site |
| `telegrambot_py.py` | Telegram bot | Real users on their phones |
| `dialogflowbot.py` | Colab widget | Quick testing while tuning intents |

`Chatbot_streamlit.mp4` is a recording of the web app answering live questions.

---

## Setup

### 1. Dialogflow credentials

All three interfaces authenticate with a **Google Cloud service account key**:

1. In the [Google Cloud console](https://console.cloud.google.com/), open the project holding your Dialogflow agent.
2. **IAM & Admin → Service Accounts → Create service account**.
3. Grant it the **Dialogflow API Client** role.
4. **Keys → Add key → JSON**, and save it as `dialogflow-key.json` in this folder.

> ⚠️ **Never commit this file.** It grants API access to your Google Cloud project. It's already listed in `.gitignore` — keep it that way.

### 2. Point at your agent

The default project id is `customersupportbot-lvuh`. Use your own with:

```bash
set DIALOGFLOW_PROJECT_ID=your-project-id      # Windows
export DIALOGFLOW_PROJECT_ID=your-project-id   # macOS / Linux
```

### 3. Install

```bash
pip install google-cloud-dialogflow streamlit python-telegram-bot ipywidgets
```

---

## Running each interface

### Streamlit web app

```bash
streamlit run chatbot_app.py
```

Opens at `http://localhost:8501`.

### Telegram bot

Get a token from [@BotFather](https://t.me/BotFather) (`/newbot`), then:

```bash
set TELEGRAM_BOT_TOKEN=your-token-here      # Windows
export TELEGRAM_BOT_TOKEN=your-token-here   # macOS / Linux
python telegrambot_py.py
```

Message your bot on Telegram; `/start` gets a greeting, anything else is routed to Dialogflow.

> 🔒 **The token is read from the environment, never written into the source.** A token committed to a repository is a *published* credential — anyone who reads the file can receive your bot's messages and reply as it. And because git keeps history forever, deleting the line later doesn't undo it: the only real fix is revoking the token via `/revoke` in @BotFather and issuing a new one.

### Colab widget

Upload `dialogflow-key.json` to the Colab session, then run `dialogflowbot.py`. A text box appears inline and replies print beneath it.

---

## Extending the bot

Everything the bot knows lives in the Dialogflow console, not in this code:

1. Open your agent → **Intents → Create intent**.
2. Add **training phrases** — 10–15 genuinely different phrasings work far better than 30 near-identical ones.
3. Add the **response** text.
4. Save. All three interfaces pick it up immediately; nothing here needs redeploying.

If the bot replies with its fallback intent, the question didn't match anything — check **Training** in the console to see what real users actually asked, and add the phrasings you missed.
