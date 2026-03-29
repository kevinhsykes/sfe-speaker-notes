import streamlit as st
import json
import os
from datetime import datetime

# --- Config ---
st.set_page_config(page_title="SFE Speaker Notes", page_icon="🎤", layout="wide")
DATA_FILE = "sfe_data.json"

# --- Default Speaker Data ---
DEFAULT_SPEAKERS = [
    {
        "id": "connelly",
        "name": "Lindsay Connelly",
        "date": "2026-03-18",
        "company": "Linden Digital Marketing",
        "role": "Founder",
        "task_ref": "Task 2 (running doc, first entry)",
        "bio": "Founder of Linden Digital Marketing, a Rochester-area digital marketing agency.",
        "has_conversation_task": False,
        "ai_usage_prompts": [
            "AI tools used in her digital marketing work (content generation, analytics, ad targeting, etc.)",
            "How she positions AI capabilities to clients",
            "What clients ask for vs. what actually works",
            "Any tools or platforms she relies on day to day",
            "Her take on AI replacing vs. augmenting marketing roles"
        ],
        "takeaway_prompts": [
            "How she started Linden Digital Marketing",
            "Biggest challenges running a small marketing agency",
            "Advice for someone entering consulting/agency work",
            "Anything about Rochester's small business market",
            "Most interesting or unexpected thing she said"
        ],
        "comparison_prompts": [
            "How does a marketing agency's AI adoption compare to other speakers?",
            "Service business vs. product business differences"
        ],
        "prepared_questions": [],
        "ai_usage_notes": "",
        "takeaway_notes": "",
        "comparison_notes": "",
        "conversation_notes": "",
        "conversation_takeaways": "",
        "raw_shorthand": ""
    },
    {
        "id": "weis",
        "name": "Cyndi Weis",
        "date": "2026-03-26",
        "company": "Breathe Yoga & Juice Bar",
        "role": "Founder & Owner",
        "task_ref": "Task 2 (running doc)",
        "bio": "20+ year wellness business in Pittsford. Yoga studio, juice bar, kitchen/bakery, spa, retail boutique. Family-run with daughters Abby and Carly. 2016 Rochester Business Person of the Year (50+ employees). Previously had 5 franchise locations, dissolved franchise model in 2022. Registered dietitian and keynote speaker on aging/longevity.",
        "has_conversation_task": False,
        "ai_usage_prompts": [
            "Does she use any AI tools currently? (scheduling, social media, inventory, content)",
            "What operational tasks eat the most time that tech could help with?",
            "Attitude toward AI: open/skeptical/unaware?",
            "How does she use customer data across revenue streams (classes, food, spa, retail)?",
            "If an AI consultant pitched her, what would she actually want help with?",
            "Any mention of online class platform, virtual offerings, and tech behind that"
        ],
        "takeaway_prompts": [
            "Lessons from scaling to 5 franchises then dissolving the franchise model",
            "How she manages multiple revenue streams under one roof",
            "Customer retention in wellness (people cycle in and out)",
            "Running a family business with her daughters",
            "Building around personal passion vs. market demand",
            "How she adapted during COVID (virtual classes, curbside, 40 Days program)"
        ],
        "comparison_prompts": [
            "Small wellness business vs. Connelly's digital marketing agency: different AI needs?",
            "Owner-operator perspective vs. more corporate/scaled businesses (Mucci, Goldner)",
            "How does a brick-and-mortar service business think about tech differently?"
        ],
        "prepared_questions": [],
        "ai_usage_notes": "",
        "takeaway_notes": "",
        "comparison_notes": "",
        "conversation_notes": "",
        "conversation_takeaways": "",
        "raw_shorthand": ""
    },
    {
        "id": "goldner",
        "name": "Andrew Goldner",
        "date": "2026-04-01",
        "company": "(Research before talk)",
        "role": "(Research before talk)",
        "task_ref": "Task 2 (running doc) + Task 3 (pursue conversation)",
        "bio": "Task 3 focus: consulting, business growth strategy, where AI fits into the advisory model. Also use this conversation to research possible data sources/ideas for Task 8 (applied analytics project).",
        "has_conversation_task": True,
        "ai_usage_prompts": [
            "How AI fits into his consulting/advisory model",
            "What AI tools his firm uses internally",
            "How he advises clients on AI adoption",
            "Where he sees AI creating the most value in consulting",
            "His take on AI implementation failure rates"
        ],
        "takeaway_prompts": [
            "His path into consulting/advisory work",
            "How he thinks about business growth strategy",
            "What skills matter most in consulting",
            "Advice for someone entering the field"
        ],
        "comparison_prompts": [
            "Advisory/consulting perspective vs. business operators (Weis, Connelly)",
            "How does his view on AI adoption differ from someone implementing it internally?"
        ],
        "prepared_questions": [
            "What does your consulting/advisory process look like end to end?",
            "Where does AI fit into how you advise clients?",
            "What data sources or datasets do you rely on for client analysis?",
            "What skills matter most for someone entering consulting?",
            "Any leads on datasets or project ideas for an applied analytics project?"
        ],
        "ai_usage_notes": "",
        "takeaway_notes": "",
        "comparison_notes": "",
        "conversation_notes": "",
        "conversation_takeaways": "",
        "raw_shorthand": ""
    },
    {
        "id": "mucci",
        "name": "Martin Mucci",
        "date": "2026-04-08",
        "company": "Paychex",
        "role": "Former CEO",
        "task_ref": "Task 2 (running doc) + Task 5 (pursue conversation)",
        "bio": "Paychex founded by Tom Golisano in 1971. Major Rochester employer in the middle of a significant AI transformation. Task 5 focus: AI transformation at Paychex, adoption challenges, what skills companies look for in implementation roles.",
        "has_conversation_task": True,
        "ai_usage_prompts": [
            "Where Paychex is in its AI transformation journey",
            "Biggest adoption challenges internally",
            "How leadership communicates AI changes to the workforce",
            "Specific AI tools or capabilities Paychex has rolled out",
            "What went well vs. what stalled",
            "How they measure success of AI initiatives"
        ],
        "takeaway_prompts": [
            "His leadership philosophy at scale",
            "Paychex's competitive position and where AI fits in that",
            "Rochester's role in Paychex's future",
            "Advice for someone early in their career"
        ],
        "comparison_prompts": [
            "Enterprise-scale AI transformation vs. small business adoption (Weis, Connelly)",
            "How does Paychex's approach compare to Lawley Insurance (Adam Clouden conversation)?",
            "Leadership-driven vs. bottom-up adoption: what does Mucci's perspective add?"
        ],
        "prepared_questions": [
            "What has been the biggest AI adoption challenge at Paychex?",
            "What does the internal change management process look like?",
            "What skills does Paychex look for in people helping with AI implementation?",
            "How involved is leadership vs. middle management in driving adoption?",
            "What would you want from an outside AI implementation consultant?",
            "How does Paychex handle employee resistance or skepticism?"
        ],
        "ai_usage_notes": "",
        "takeaway_notes": "",
        "comparison_notes": "",
        "conversation_notes": "",
        "conversation_takeaways": "",
        "raw_shorthand": ""
    }
]

DEFAULT_ANALYSIS = {
    "common_themes": "",
    "biggest_differences": "",
    "consulting_insights": "",
    "surprises": ""
}

# --- Data Persistence ---
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"speakers": DEFAULT_SPEAKERS, "analysis": DEFAULT_ANALYSIS}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# --- Initialize ---
data = load_data()
speakers = data["speakers"]
analysis = data.get("analysis", DEFAULT_ANALYSIS)

# --- Custom CSS ---
st.markdown("""
<style>
    .speaker-header {
        background: linear-gradient(135deg, #1B4F72, #2E86C1);
        padding: 20px 25px;
        border-radius: 10px;
        color: white;
        margin-bottom: 20px;
    }
    .speaker-header h2 {
        color: white !important;
        margin-bottom: 5px;
    }
    .speaker-header p {
        color: #D6EAF8;
        margin: 2px 0;
    }
    .info-box {
        background-color: #F8F9FA;
        border-left: 4px solid #2E86C1;
        padding: 12px 16px;
        border-radius: 0 8px 8px 0;
        margin-bottom: 15px;
        font-size: 0.9em;
        color: #333;
    }
    .prompt-item {
        background: #EBF5FB;
        padding: 8px 12px;
        border-radius: 6px;
        margin: 4px 0;
        font-size: 0.85em;
        color: #1B4F72;
    }
    .status-upcoming {
        background: #FEF9E7;
        border: 1px solid #F9E79F;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.8em;
        color: #7D6608;
        display: inline-block;
    }
    .status-completed {
        background: #E8F8F5;
        border: 1px solid #A3E4D7;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.8em;
        color: #1E8449;
        display: inline-block;
    }
    .section-divider {
        border-top: 2px solid #E5E8E8;
        margin: 25px 0;
    }
</style>
""", unsafe_allow_html=True)

# --- Sidebar ---
st.sidebar.title("🎤 SFE Speaker Notes")
st.sidebar.markdown("*Spring 2026 | Kevin Sykes*")
st.sidebar.markdown("*Golisano Institute for Business & Entrepreneurship*")
st.sidebar.markdown("---")

# Navigation
nav_options = ["📊 Dashboard"]
for s in speakers:
    speaker_date = datetime.strptime(s["date"], "%Y-%m-%d")
    status = "✅" if speaker_date <= datetime.now() else "📅"
    nav_options.append(f"{status} {s['name']}")
nav_options.append("🔍 Cross-Speaker Analysis")
nav_options.append("➕ Add Speaker")

selection = st.sidebar.radio("Navigate", nav_options, label_visibility="collapsed")

st.sidebar.markdown("---")
st.sidebar.markdown("**Learning Contract Tasks**")
st.sidebar.markdown("Task 2: Running SFE notes")
st.sidebar.markdown("Task 3: Goldner conversation")
st.sidebar.markdown("Task 5: Mucci conversation")

# --- Dashboard ---
if selection == "📊 Dashboard":
    st.title("SFE Speaker Notes Dashboard")
    st.markdown("Speaking from Experience, Spring 2026")
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    total = len(speakers)
    past = sum(1 for s in speakers if datetime.strptime(s["date"], "%Y-%m-%d") <= datetime.now())
    with_notes = sum(1 for s in speakers if s.get("ai_usage_notes", "").strip() or s.get("takeaway_notes", "").strip() or s.get("raw_shorthand", "").strip())
    
    col1.metric("Total Speakers", total)
    col2.metric("Talks Attended", past)
    col3.metric("With Notes", with_notes)
    
    st.markdown("---")
    st.subheader("Speaker Timeline")
    
    for s in speakers:
        speaker_date = datetime.strptime(s["date"], "%Y-%m-%d")
        is_past = speaker_date <= datetime.now()
        has_notes = bool(s.get("ai_usage_notes", "").strip() or s.get("takeaway_notes", "").strip() or s.get("raw_shorthand", "").strip())
        
        if is_past and has_notes:
            status_html = '<span class="status-completed">Completed</span>'
        elif is_past:
            status_html = '<span class="status-upcoming">Attended, needs notes</span>'
        else:
            status_html = '<span class="status-upcoming">Upcoming</span>'
        
        st.markdown(f"""
        **{s['name']}** — {s['company']}  
        {speaker_date.strftime('%B %d, %Y')} &nbsp;&nbsp; {status_html}  
        *{s['task_ref']}*
        """, unsafe_allow_html=True)
        st.markdown("---")

# --- Add Speaker ---
elif selection == "➕ Add Speaker":
    st.title("Add New Speaker")
    st.markdown("Add a new SFE speaker to track.")
    
    with st.form("add_speaker"):
        name = st.text_input("Speaker Name")
        date = st.date_input("Date of Talk")
        company = st.text_input("Company / Organization")
        role = st.text_input("Role / Title")
        bio = st.text_area("Background / Bio (optional)")
        has_conv = st.checkbox("This speaker has a conversation/interview task")
        
        submitted = st.form_submit_button("Add Speaker")
        
        if submitted and name:
            new_id = name.lower().replace(" ", "_")
            new_speaker = {
                "id": new_id,
                "name": name,
                "date": date.strftime("%Y-%m-%d"),
                "company": company,
                "role": role,
                "task_ref": "Task 2 (running doc)",
                "bio": bio,
                "has_conversation_task": has_conv,
                "ai_usage_prompts": [
                    "How does this speaker/organization use AI?",
                    "What tools or platforms do they rely on?",
                    "What is their attitude toward AI adoption?",
                    "Biggest AI-related challenge they face"
                ],
                "takeaway_prompts": [
                    "Most valuable insight from the talk",
                    "Advice relevant to my career path",
                    "Anything surprising or unexpected"
                ],
                "comparison_prompts": [
                    "How does this speaker's perspective compare to previous speakers?",
                    "What new pattern or contradiction emerged?"
                ],
                "prepared_questions": [],
                "ai_usage_notes": "",
                "takeaway_notes": "",
                "comparison_notes": "",
                "conversation_notes": "",
                "conversation_takeaways": "",
                "raw_shorthand": ""
            }
            speakers.append(new_speaker)
            save_data({"speakers": speakers, "analysis": analysis})
            st.success(f"Added {name}! Navigate to their page in the sidebar.")
            st.rerun()

# --- Cross-Speaker Analysis ---
elif selection == "🔍 Cross-Speaker Analysis":
    st.title("Cross-Speaker Analysis")
    st.markdown("Use this section at the end of the quarter to compare and analyze patterns across all speakers.")
    st.markdown("---")
    
    st.subheader("Common Themes on AI Adoption")
    st.markdown("*What patterns emerged? Where did multiple speakers agree? Common barriers mentioned?*")
    common = st.text_area("Common Themes", value=analysis.get("common_themes", ""), height=150, key="common", label_visibility="collapsed")
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    st.subheader("Biggest Differences in AI Perspective")
    st.markdown("*Where did speakers disagree? How much did industry/company size drive differences? Enterprise vs. small business vs. advisory?*")
    diffs = st.text_area("Differences", value=analysis.get("biggest_differences", ""), height=150, key="diffs", label_visibility="collapsed")
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    st.subheader("Insights Relevant to AI Implementation Consulting")
    st.markdown("*What did speakers teach you about what companies actually need? What skills kept coming up? How does this connect to failure rate data?*")
    consulting = st.text_area("Consulting Insights", value=analysis.get("consulting_insights", ""), height=150, key="consulting", label_visibility="collapsed")
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    st.subheader("Surprises / Changed Assumptions")
    st.markdown("*What challenged something you believed? Biggest gap between expectation and reality? How has your understanding evolved?*")
    surprises = st.text_area("Surprises", value=analysis.get("surprises", ""), height=150, key="surprises", label_visibility="collapsed")
    
    if st.button("Save Analysis", type="primary"):
        analysis["common_themes"] = common
        analysis["biggest_differences"] = diffs
        analysis["consulting_insights"] = consulting
        analysis["surprises"] = surprises
        save_data({"speakers": speakers, "analysis": analysis})
        st.success("Analysis saved.")

# --- Speaker Pages ---
else:
    # Find the speaker
    speaker_name = selection.split(" ", 1)[1]  # Remove the emoji prefix
    speaker = None
    speaker_idx = None
    for i, s in enumerate(speakers):
        if s["name"] == speaker_name:
            speaker = s
            speaker_idx = i
            break
    
    if speaker is None:
        st.error("Speaker not found.")
    else:
        speaker_date = datetime.strptime(speaker["date"], "%Y-%m-%d")
        is_upcoming = speaker_date > datetime.now()
        
        # Header
        st.markdown(f"""
        <div class="speaker-header">
            <h2>{speaker['name']}</h2>
            <p><strong>{speaker['company']}</strong> — {speaker['role']}</p>
            <p>{speaker_date.strftime('%B %d, %Y')} &nbsp;|&nbsp; {speaker['task_ref']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Bio
        if speaker.get("bio"):
            st.markdown(f'<div class="info-box">{speaker["bio"]}</div>', unsafe_allow_html=True)
        
        # Editable company/role if placeholders
        if "(Research" in speaker.get("company", "") or "(Research" in speaker.get("role", ""):
            st.markdown("#### Update Speaker Info")
            col1, col2 = st.columns(2)
            new_company = col1.text_input("Company", value=speaker["company"], key=f"company_{speaker['id']}")
            new_role = col2.text_input("Role", value=speaker["role"], key=f"role_{speaker['id']}")
            new_bio = st.text_area("Bio / Background", value=speaker.get("bio", ""), key=f"bio_{speaker['id']}")
            if st.button("Update Info", key=f"update_info_{speaker['id']}"):
                speakers[speaker_idx]["company"] = new_company
                speakers[speaker_idx]["role"] = new_role
                speakers[speaker_idx]["bio"] = new_bio
                save_data({"speakers": speakers, "analysis": analysis})
                st.success("Updated!")
                st.rerun()
        
        st.markdown("---")
        
        # --- Shorthand Notes (top of page for quick access during talk) ---
        st.subheader("📝 Live Shorthand Notes")
        st.markdown("*Use this during the talk. Quick bullet points, keywords, phrases. Fill in the structured sections after.*")
        raw = st.text_area(
            "Shorthand",
            value=speaker.get("raw_shorthand", ""),
            height=150,
            key=f"raw_{speaker['id']}",
            placeholder="Type quick notes here during the talk...",
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # --- Prepared Questions (for speakers with conversation tasks) ---
        if speaker.get("has_conversation_task") or speaker.get("prepared_questions"):
            st.subheader("❓ Prepared Questions")
            st.markdown("*Questions to ask during or after the talk.*")
            
            existing_qs = speaker.get("prepared_questions", [])
            for i, q in enumerate(existing_qs):
                st.markdown(f'<div class="prompt-item">• {q}</div>', unsafe_allow_html=True)
            
            new_q = st.text_input("Add a question", key=f"newq_{speaker['id']}", placeholder="Type a new question and press Enter...")
            if new_q:
                speakers[speaker_idx]["prepared_questions"].append(new_q)
                save_data({"speakers": speakers, "analysis": analysis})
                st.rerun()
            
            st.markdown("---")
        
        # --- AI Usage Notes ---
        st.subheader("🤖 How They Apply / See AI in Their Business")
        st.markdown("*Reference prompts:*")
        for p in speaker.get("ai_usage_prompts", []):
            st.markdown(f'<div class="prompt-item">• {p}</div>', unsafe_allow_html=True)
        
        ai_notes = st.text_area(
            "AI Usage Notes",
            value=speaker.get("ai_usage_notes", ""),
            height=200,
            key=f"ai_{speaker['id']}",
            placeholder="Your notes on how this speaker uses or views AI...",
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # --- Key Takeaways ---
        st.subheader("💡 Key Takeaways / General Notes")
        st.markdown("*Reference prompts:*")
        for p in speaker.get("takeaway_prompts", []):
            st.markdown(f'<div class="prompt-item">• {p}</div>', unsafe_allow_html=True)
        
        takeaway_notes = st.text_area(
            "Takeaway Notes",
            value=speaker.get("takeaway_notes", ""),
            height=200,
            key=f"takeaway_{speaker['id']}",
            placeholder="Key takeaways, general notes, interesting points...",
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # --- Conversation Notes (for speakers with conversation tasks) ---
        if speaker.get("has_conversation_task"):
            st.subheader("🗣️ Conversation Notes")
            st.markdown("*Notes from your direct conversation with this speaker.*")
            
            conv_notes = st.text_area(
                "Conversation Notes",
                value=speaker.get("conversation_notes", ""),
                height=200,
                key=f"conv_{speaker['id']}",
                placeholder="What did you discuss? Key points from the conversation...",
                label_visibility="collapsed"
            )
            
            st.subheader("🎯 Key Takeaways from Conversation")
            conv_takeaways = st.text_area(
                "Conversation Takeaways",
                value=speaker.get("conversation_takeaways", ""),
                height=150,
                key=f"convtake_{speaker['id']}",
                placeholder="Most important thing learned, how it changes your thinking, follow-up actions...",
                label_visibility="collapsed"
            )
            
            st.markdown("---")
        
        # --- Comparison ---
        st.subheader("🔄 Comparison / Contrast with Other Speakers")
        st.markdown("*Reference prompts:*")
        for p in speaker.get("comparison_prompts", []):
            st.markdown(f'<div class="prompt-item">• {p}</div>', unsafe_allow_html=True)
        
        comp_notes = st.text_area(
            "Comparison Notes",
            value=speaker.get("comparison_notes", ""),
            height=150,
            key=f"comp_{speaker['id']}",
            placeholder="How does this speaker compare to others?",
            label_visibility="collapsed"
        )
        
        # --- Save ---
        st.markdown("---")
        if st.button("💾 Save All Notes", type="primary", key=f"save_{speaker['id']}"):
            speakers[speaker_idx]["raw_shorthand"] = raw
            speakers[speaker_idx]["ai_usage_notes"] = ai_notes
            speakers[speaker_idx]["takeaway_notes"] = takeaway_notes
            speakers[speaker_idx]["comparison_notes"] = comp_notes
            if speaker.get("has_conversation_task"):
                speakers[speaker_idx]["conversation_notes"] = conv_notes
                speakers[speaker_idx]["conversation_takeaways"] = conv_takeaways
            save_data({"speakers": speakers, "analysis": analysis})
            st.success("All notes saved!")
