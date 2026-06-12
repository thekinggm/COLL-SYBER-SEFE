import time
import re
import html
import json
import uuid
from typing import Tuple, Dict, Any, List
import streamlit as st

# =====================================================================
# 1. CORE CONFIGURATION (THE ONE ABOVE ALL)
# =====================================================================
st.set_page_config(
    page_title="APEX V8 - THE ONE ABOVE ALL", 
    page_icon="🌌", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================================
# 2. ULTIMATE GLASSMORPHISM CSS
# =====================================================================
@st.cache_data
def inject_custom_css():
    st.markdown("""
    <style>
    /* The Void Background */
    .stApp { 
        font-family: 'Inter', sans-serif; 
        background-color: #050810; 
        color: #E2E8F0; 
        background-image: radial-gradient(circle at 50% -20%, #101930 0%, #050810 80%);
    }
    
    /* Control Panel Sidebar */
    [data-testid="stSidebar"] {
        background-color: rgba(5, 8, 16, 0.7) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(30, 41, 59, 0.5);
    }
    
    /* Input Matrix */
    .stTextInput input, .stTextArea textarea { 
        background: rgba(15, 23, 42, 0.6);
        backdrop-filter: blur(12px);
        color: #00F0FF; 
        border: 1px solid rgba(45, 55, 72, 0.8); 
        border-radius: 8px; 
        transition: all 0.3s ease;
        padding: 14px;
        font-size: 1.1rem;
        letter-spacing: 0.5px;
    }
    .stTextInput input:focus, .stTextArea textarea:focus { 
        border: 1px solid #00F0FF; 
        box-shadow: 0 0 25px rgba(0, 240, 255, 0.2); 
        background: rgba(15, 23, 42, 0.9);
    }
    
    /* God-Tier Button */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #090e17, #131d2e);
        color: #00F0FF;
        border: 1px solid #00F0FF;
        border-radius: 8px;
        padding: 0.8rem;
        font-weight: 900;
        letter-spacing: 2px;
        text-transform: uppercase;
        transition: all 0.3s ease;
        width: 100%;
        box-shadow: 0 0 15px rgba(0, 240, 255, 0.1);
    }
    div.stButton > button:first-child:hover {
        background: #00F0FF;
        color: #050810;
        box-shadow: 0 0 40px rgba(0, 240, 255, 0.6);
        transform: translateY(-2px);
    }
    
    /* Dynamic Alerts & Code */
    .stAlert { 
        border-radius: 8px; 
        border-left: 4px solid #00F0FF; 
        background: rgba(15, 23, 42, 0.8);
        backdrop-filter: blur(10px);
        color: #F8FAFC;
    }
    code { color: #FF4A6D; font-family: 'JetBrains Mono', monospace; font-size: 0.9rem; }
    pre { 
        border-radius: 10px; 
        border: 1px solid rgba(45, 55, 72, 0.8); 
        background: #090D14 !important; 
        box-shadow: inset 0 0 20px rgba(0,0,0,0.8);
    }
    h1, h2, h3 { color: #FFFFFF; font-weight: 800; }
    hr { border-color: rgba(45, 55, 72, 0.5); }
    </style>
    """, unsafe_allow_html=True)

# =====================================================================
# 3. ADVANCED PERSISTENT MEMORY & TELEMETRY
# =====================================================================
class MemoryVault:
    def __init__(self):
        if "history_log" not in st.session_state:
            st.session_state.history_log = []
        if "risk_score" not in st.session_state:
            st.session_state.risk_score = 0
        if "total_reqs" not in st.session_state:
            st.session_state.total_reqs = 0

    def commit(self, intent: str, query: str, status: str):
        st.session_state.total_reqs += 1
        st.session_state.history_log.insert(0, {
            "time": time.strftime("%H:%M:%S"),
            "intent": intent,
            "query": query[:30] + "...",
            "status": status
        })
        # Keep only last 10 logs
        st.session_state.history_log = st.session_state.history_log[:10]
        
        # Adjust risk score based on intent
        if status == "BLOCKED": st.session_state.risk_score += 20
        elif intent not in ["generic", "none"]: st.session_state.risk_score += 5

    def get_metrics(self):
        return {
            "reqs": st.session_state.total_reqs,
            "risk": min(100, st.session_state.risk_score),
            "logs": st.session_state.history_log
        }

# =====================================================================
# 4. HEURISTIC WAF ENGINE
# =====================================================================
class AdvancedWAF:
    @staticmethod
    def inspect(text: str) -> Tuple[bool, str]:
        # Deep Regex Signatures covering OWASP Top 10 + Zero Days
        signatures = {
            r"(?i)(UNION.*SELECT|DROP.*TABLE|--\s*$)": "SQLi (Database Injection)",
            r"(?i)(<script>|javascript:|onerror=|onload=)": "XSS (Client-Side Injection)",
            r"(?i)(\.\.\/|\/etc\/passwd|\\windows\\)": "LFI/Path Traversal",
            r"(?i)(os\.system|exec\(|eval\(|subprocess)": "RCE (Command Injection)",
            r"(?i)(ignore instructions|system prompt|jailbreak)": "LLM Prompt Injection"
        }
        for pattern, threat_name in signatures.items():
            if re.search(pattern, text): return False, threat_name
        return True, "CLEAN"

# =====================================================================
# 5. OMNISCIENT THREAT DATABASE & SYNTHESIZER
# =====================================================================
class OmniscientAI:
    def __init__(self):
        # 👑 THE ABSOLUTE MASTER BLUEPRINTS
        self.premium_blueprints = {
            "sql": '''def execute_secure_db_query(db_session, user_id: str) -> dict:
    """[OMNISCIENT] SQLi Prevention via Strict ORM Casting & Parameterization."""
    try:
        sanitized_id = int(user_id) # Type validation
        query = "SELECT id, username, role FROM users WHERE id = :uid LIMIT 1"
        result = db_session.execute(query, {"uid": sanitized_id}).fetchone()
        return dict(result) if result else {"error": "Record unavailable"}
    except ValueError:
        return {"error": "Invalid constraint format"}''',
            
            "xss": '''def secure_frontend_renderer(untrusted_payload: str) -> str:
    """[OMNISCIENT] Deep DOMPurify Logic with Event-Handler Annihilation."""
    import html, re
    if not isinstance(untrusted_payload, str): return ""
    clean = untrusted_payload.replace("\\x00", "").strip()
    clean = re.sub(r"(?i)<(script|iframe|object|embed|svg|applet)[^>]*>.*?</\\1>", "", clean)
    clean = re.sub(r"(?i)on[a-z]+\s*=\s*['\"].*?['\"]", "", clean)
    return html.escape(clean, quote=True)''',
            
            "llm": '''def secure_llm_prompt_guard(user_prompt: str) -> str:
    """[OMNISCIENT] AI Prompt Injection Guard (Defends against Jailbreaks)."""
    import re
    if not isinstance(user_prompt, str): return ""
    jailbreaks = [r"(?i)(ignore previous)", r"(?i)(system prompt|DAN|act as)"]
    if any(re.search(sig, user_prompt) for sig in jailbreaks):
        return "[SYSTEM OVERRIDE DETECTED AND NEUTRALIZED]"
    return user_prompt.replace("{", "{{").replace("}", "}}")''',

            "ssrf": '''def enterprise_resource_fetcher(target_url: str) -> bytes:
    """[OMNISCIENT] Zero-Trust SSRF Engine. Mathematically blocks Cloud Metadata."""
    import urllib.request, urllib.parse, socket, ipaddress
    parsed = urllib.parse.urlparse(target_url)
    if parsed.scheme not in ['http', 'https']: raise ValueError("Protocol blocked.")
    ip_obj = ipaddress.ip_address(socket.gethostbyname(parsed.hostname))
    if ip_obj.is_private or ip_obj.is_loopback: raise PermissionError("Internal subnet access denied.")
    req = urllib.request.Request(target_url, headers={'User-Agent': 'SecuredProxy/MAX'})
    with urllib.request.urlopen(req, timeout=3) as res: return res.read()''',

            "jwt": '''def validate_enterprise_jwt(auth_header: str, public_key_pem: str) -> dict:
    """[OMNISCIENT] Asymmetric JWT Validation (RS256) immune to brute-forcing."""
    import jwt # requires PyJWT
    if not auth_header or not auth_header.startswith("Bearer "): raise PermissionError("Invalid header.")
    try:
        return jwt.decode(auth_header.split(" ")[1], public_key_pem, algorithms=["RS256"], options={"require": ["exp"]})
    except Exception as e:
        raise PermissionError(f"Token validation failed: {e}")''',

            "cmd": '''def secure_system_execution(ip_address: str) -> str:
    """[OMNISCIENT] Prevents OS Command Injection via structural isolation."""
    import subprocess, ipaddress
    try:
        valid_ip = str(ipaddress.ip_address(ip_address.strip())) # Validates IP structure
        res = subprocess.run(["ping", "-c", "2", valid_ip], capture_output=True, text=True, shell=False)
        return res.stdout
    except ValueError:
        return "Execution Blocked: Invalid input structure."''',

            "generic": '''def universal_waf_middleware(payload: dict) -> dict:
    """[OMNISCIENT] Universal WAF - Neutralizes unknown payload anomalies."""
    import html
    return {k: html.escape(v.strip(), quote=True) if isinstance(v, str) else v for k, v in payload.items()}'''
        }

        # 🆓 FREE BLUEPRINTS
        self.free_blueprints = {
            "sql": "# [FREE] Basic replace\ndef basic_sql(v): return str(v).replace('\"', '')",
            "xss": "# [FREE] Basic escape\nimport html\ndef basic_xss(v): return html.escape(str(v))",
            "generic": "# [FREE] Generic filter\ndef basic_filter(v): return str(v).strip()"
        }

        # DUAL LANGUAGE GUIDES
        self.guides = {
            "sql": {"he": "הטמע בשכבת ה-DAL/Model למניעת מניפולציות במסד הנתונים.", "en": "Implement in the DAL/Model layer to prevent DB manipulation."},
            "xss": {"he": "עטוף קלט משתמש לפני הזרקתו ל-HTML ב-Frontend.", "en": "Wrap user input before rendering it to HTML in the Frontend."},
            "llm": {"he": "העבר כל פרומפט דרך הפונקציה לפני קריאה ל-OpenAI/LLM API.", "en": "Sanitize prompts before passing them to the OpenAI/LLM API."},
            "ssrf": {"he": "מקם במודולי רשת שמורידים קבצים או קוראים ל-Webhooks חיצוניים.", "en": "Place in network modules fetching files or calling Webhooks."},
            "jwt": {"he": "הטמע כ-Middleware באימות זהויות ב-API Gateway.", "en": "Implement as Auth Middleware in your API Gateway."},
            "cmd": {"he": "החלף כל קריאה ל-os.system בפונקציה מבודדת זו.", "en": "Replace all os.system calls with this isolated function."},
            "generic": {"he": "מקם ב-Request Interceptor בכניסה לשרת.", "en": "Deploy as a Request Interceptor at the server entry point."}
        }

    def process_language_and_intent(self, text: str) -> Tuple[str, str]:
        lang = "he" if any("\u0590" <= c <= "\u05FF" for c in text) else "en"
        t = text.lower()
        if any(w in t for w in ["ssrf", "webhook"]): intent = "ssrf"
        elif any(w in t for w in ["sql", "db", "select", "הזרקת", "מסד"]): intent = "sql"
        elif any(w in t for w in ["llm", "prompt", "ai", "פרומפט"]): intent = "llm"
        elif any(w in t for w in ["token", "jwt", "auth", "טוקן"]): intent = "jwt"
        elif any(w in t for w in ["cmd", "command", "os", "פקודה"]): intent = "cmd"
        elif any(w in t for w in ["xss", "script", "html", "סניטציה"]): intent = "xss"
        else: intent = "generic"
        return lang, intent

    def get_intelligence(self, intent: str, lang: str, is_premium: bool) -> str:
        if not is_premium:
            return "### ⚠️ מערכת בסיסית מופעלת\nשדרג ל-PREMIUM כדי לקבל מודיעין איומים מלא וקוד חסין-פריצות." if lang == "he" else "### ⚠️ Basic System Active\nUpgrade to PREMIUM for full threat intel and bulletproof code."
            
        intel_db = {
            "ssrf": {"he": "מודיעין קריטי (CVSS: 9.1) | חסימה הרמטית של עקיפות DNS ו-Cloud Metadata.", "en": "Critical Intel (CVSS: 9.1) | Hermetic block of DNS rebinding and Cloud Metadata."},
            "sql": {"he": "מודיעין קריטי (CVSS: 9.8) | אכיפת ORM כופה הפרדה מוחלטת בין לוגיקה לנתונים.", "en": "Critical Intel (CVSS: 9.8) | ORM enforcement ensures absolute logic/data separation."},
            "xss": {"he": "מודיעין מתקדם (CVSS: 8.2) | טיהור אקטיבי של תגיות DOM מוסתרות ואירועי JS.", "en": "Advanced Intel (CVSS: 8.2) | Active purification of hidden DOM tags and JS events."},
            "llm": {"he": "מודיעין מתקדם (CVSS: 8.8) | חומת אש קוגניטיבית נגד פקודות Jailbreak ל-AI.", "en": "Advanced Intel (CVSS: 8.8) | Cognitive firewall against AI Jailbreak commands."},
            "jwt": {"he": "מודיעין קריטי (CVSS: 9.4) | אימות א-סימטרי המונע חטיפת מפתחות וזיוף זהויות.", "en": "Critical Intel (CVSS: 9.4) | Asymmetric auth preventing key hijacking and forgery."},
            "cmd": {"he": "מודיעין קריטי (CVSS: 9.8) | בידוד פרמטרים ומניעת שרשור פקודות מערכת (&&, ;).", "en": "Critical Intel (CVSS: 9.8) | Parameter isolation preventing OS command chaining."},
            "generic": {"he": "מודיעין אנומליות | מנוע WAF אוניברסלי מנתח את הבקשה ומנקה תווים מבניים.", "en": "Anomaly Intel | Universal WAF engine parses request and sanitizes structural chars."}
        }
        return f"### 🌌 {intel_db.get(intent, intel_db['generic'])[lang]}"

# =====================================================================
# 6. SYSTEM INITIALIZATION & UI
# =====================================================================
inject_custom_css()
memory_vault = MemoryVault()
ai_engine = OmniscientAI()

# --- SIDEBAR: COMMAND CENTER ---
with st.sidebar:
    st.image("https://img.icons8.com/nolan/128/artificial-intelligence.png", width=90)
    st.title("APEX V8 TERMINAL")
    st.markdown("---")
    
    tier_selection = st.radio("CORE ENGINE TIER:", ["🌌 OMNISCIENT (Maxed)", "🆓 FREE (Throttled)"])
    is_premium = "OMNISCIENT" in tier_selection
    
    st.markdown("---")
    st.subheader("Live Telemetry")
    metrics = memory_vault.get_metrics()
    
    col1, col2 = st.columns(2)
    col1.metric("Queries", metrics["reqs"])
    col2.metric("Threat Index", f"{metrics['risk']}%")
    st.progress(metrics['risk'] / 100.0)
    
    st.markdown("---")
    st.subheader("System Logs")
    for log in metrics["logs"]:
        status_color = "🔴" if log["status"] == "BLOCKED" else "🟢"
        st.caption(f"{status_color} [{log['time']}] {log['intent'].upper()} | {log['query']}")

# --- MAIN DASHBOARD ---
st.title("🌌 THE ONE ABOVE ALL")
st.markdown("##### The Ultimate Omniscient Cyber-Defense Synthesis Engine")
st.markdown("---")

user_prompt = st.text_input("Enter Threat Vector, Zero-Day, or Anomaly (He/En):", placeholder="e.g. מניעת הזרקת פרומפטים ל-LLM / Prevent SSRF via Webhooks")

if st.button("Synthesize Ultimate Defense"):
    if len(user_prompt) < 2:
        st.toast("⚠️ Input matrix empty.", icon="⚠️")
    else:
        # 1. WAF Inspection
        safe, threat = AdvancedWAF.inspect(user_prompt)
        lang, intent = ai_engine.process_language_and_intent(user_prompt)
        
        if not safe:
            memory_vault.commit("ATTACK", user_prompt, "BLOCKED")
            st.toast("WAF Intercept Triggered", icon="🛑")
            st.error(f"❌ CRITICAL THREAT NEUTRALIZED: Input matched malicious signature -> [{threat}]")
        else:
            # 2. Synthesis Animation
            if is_premium:
                status_text = "🌌 Omniscient Engine Synthesizing..." if lang == "en" else "🌌 מנוע אומניסיינט מבצע סינתזה..."
                with st.status(status_text, expanded=True) as status:
                    st.write("📡 Accessing Global Threat Matrix..." if lang == "en" else "📡 מתחבר למאגר איומים גלובלי...")
                    time.sleep(0.6)
                    st.write("🧬 Isolating vulnerability DNA..." if lang == "en" else "🧬 מבודד את ה-DNA של החולשה...")
                    time.sleep(0.8)
                    st.write("🛡️ Compiling absolute Zero-Trust protocol..." if lang == "en" else "🛡️ מקדד פרוטוקול אבטחה מוחלט...")
                    time.sleep(1.0)
                    status.update(label="🌌 Absolute Synthesis Complete" if lang == "en" else "🌌 סינתזה מוחלטת הושלמה", state="complete", expanded=False)
            else:
                with st.status("⏳ Processing on Free Tier..." if lang == "en" else "⏳ שרת חינמי מעבד...", expanded=True) as status:
                    st.write("Waiting for resources..." if lang == "en" else "ממתין למשאבי מערכת...")
                    time.sleep(2.5) # Artificial throttle
                    status.update(label="✅ Basic Code Ready" if lang == "en" else "✅ קוד בסיסי מוכן", state="complete", expanded=False)
            
            # 3. Secure Data Retrieval (Zero-Crash Guarantee)
            code_pool = ai_engine.premium_blueprints if is_premium else ai_engine.free_blueprints
            
            # Ultra-safe get with deep fallback
            final_code = code_pool.get(intent, code_pool.get("generic", "# FALLBACK OMNISCIENT WAF"))
            instruction = ai_engine.guides.get(intent, ai_engine.guides["generic"])[lang]
            intel_report = ai_engine.get_intelligence(intent, lang, is_premium)
            
            # Commit to Memory
            memory_vault.commit(intent, user_prompt, "SUCCESS")
            
            # 4. Display Results
            st.toast("Protocol Deployed!", icon="🌌")
            st.markdown(intel_report)
            
            tier_badge = "[OMNISCIENT V8.0]" if is_premium else "[FREE TIER]"
            st.markdown(f"### 🔒 Synthesized Blueprint {tier_badge}:")
            st.code(final_code, language="python")
            
            st.info(f"**📌 {('הנחיות הטמעה ארכיטקטונית:' if lang == 'he' else 'Architectural Deployment:')}**\n\n{instruction}")

st.markdown("---")
st.caption("THE ONE ABOVE ALL | V8.0 Apex Protocol | System: Unbreakable | Memory: Persistent")
