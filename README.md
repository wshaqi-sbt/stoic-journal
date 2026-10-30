# Stoic journal

A journal you keep with an AI coding assistant that works on files in a folder, such as Claude Code, Codex, Gemini CLI or Cursor. You dictate or type a note; the assistant files it, sets it next to your fitness tracker data, compares it with earlier entries, and tells you plainly when a pattern repeats or a decision contradicts what you said matters to you. It organizes and analyzes. The words stay yours.

Built on the Stoic dichotomy of control: separate what depends on you from what does not.

> [!WARNING]
> **Keep your journal private.** Create your copy as a **private** repository, or keep it only on your computer. Never push entries to a public repository: git history keeps every version, so deleting a file later does not remove it.

## What you get

- `AGENTS.md`: the instructions the assistant follows. Your profile goes in its About me section. `CLAUDE.md` and `GEMINI.md` only point to it, for tools that look for those names.
- `entries/`: one file per day.
- `state.md`: a daily table of how you felt next to tracker numbers, for spotting correlations.
- `patterns.md`: recurring tendencies and what you agreed about them.
- `aspirations.md`: what matters to you, used to check the direction of decisions.
- `health.md`, `dreams.md`: symptoms and dreams, when they come up.
- `whoop/`: optional script that pulls Whoop data into ready markdown tables.

Each starter file holds one example row so you can see the format. Delete it once you have your own.

## Setup

1. Click **Use this template** at the top of this page, then **Create a new repository**, and choose **Private**. Or download the ZIP and keep it local.
2. Clone your copy and open the folder in your assistant:
   ```
   git clone https://github.com/<you>/<your-journal>.git
   cd <your-journal>
   ```
   Then start it there, for example `claude`, `codex` or `gemini`, or open the folder in Cursor.
3. Type `set up my journal`. The assistant interviews you one question at a time and fills in About me in `AGENTS.md` and your first aspirations in `aspirations.md`. You can also fill them in by hand.

## Daily use

1. Dictate or type a note about your day, for example in your phone's voice memo app, and paste it into the assistant in this folder.
2. The assistant saves it in `entries/`, fills in `state.md`, compares it with earlier entries and gives you its conclusions.
3. It asks for your morning and evening score of your anchor state, 0 to 10, if the note lacks it, and what you are grateful for and proud of.
4. On Sundays it also asks how you moved closer to your aspirations that week.

When you face a decision, tell the assistant. It first checks what state you are deciding in.

## Tracker

A tracker is optional, and I recommend one. Numbers on sleep, recovery and heart rate variability show what the body went through, and the gap between them and how you describe your day is often the most useful part.

- **Whoop:** connect it with the script in `whoop/`, setup in [`whoop/README.md`](whoop/README.md).
- **Another tracker**, such as Oura, Garmin or Apple Watch: paste the numbers into your note by hand, or ask your assistant to write a similar script for its API.
- **No tracker:** the journal works without one; the tracker columns stay empty.

## License

MIT, see [LICENSE](LICENSE).
