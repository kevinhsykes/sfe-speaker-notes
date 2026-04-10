# SFE Speaker Notes — Claude Code Instructions

## What this is
Streamlit app for tracking guest speaker notes from the Golisano Institute Speaking from Experience (SFE) series — Spring 2026 AI & Business program.

**Note:** Core SFE functionality has been migrated to `golisano-study-tools` at the `/sfe` route with a Supabase backend. This standalone Streamlit version is the original prototype using local JSON storage.

## Structure
```
sfe-speaker-notes/
  app.py              # Main Streamlit app (~53 KB)
  sfe_data.json       # Auto-created JSON database
  requirements.txt    # streamlit, openpyxl
  SETUP.md
  README.md
```

## Stack
- Python 3.11+, Streamlit 1.41.0
- openpyxl for Excel export
- JSON file storage (no database)

## Rules
1. **This is the legacy version.** Active development is in `golisano-study-tools/` at `/sfe`. Don't add major features here unless explicitly asked.
2. **UNIVERSAL_QUESTIONS array** is hardcoded for consistent cross-speaker comparison. Don't change the question IDs.
3. **Speaker object schema** has fixed keys: id, name, date, company, role, ai_usage[], takeaways[], comparisons[]. Don't rename or remove.
4. **Data lives in sfe_data.json.** Back it up before destructive operations.
5. **Pre-populated** with ~2 speaker records (Lindsay Connelly, Cyndi Weis).

## Cross-repo
- `golisano-study-tools` has the production SFE section at `/sfe` with Supabase
- `kevinsykes-ai` references this as the "AI Adoption Research" project
