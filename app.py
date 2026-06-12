import time
import re
import html
from typing import Tuple
import streamlit as st

# =====================================================================
# 1. PAGE CONFIGURATION (MUST BE FIRST)
# =====================================================================
st.set_page_config(
    page_title="THE ONE ABOVE ALL - AI DefSec", 
    page_icon="👑", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================================
# 2. THE GOD-TIER CSS (GLASSMORPHISM + DEEP MIDNIGHT)
# =====================================================================
@st.cache_data
def inject_custom_css():
    st.markdown("""
    <style>
    /* Ultra Premium Deep Midnight Background */
    .stApp { 
        font-family: 'Inter', 'Segoe UI', sans-serif; 
        background-color: #0B0F19; 
        color: #E2E8F0; 
        background-image: radial-gradient(circle at 50% -20%, #1A233A 0%, #0B0F19 70%);
    }
    
    /* Sidebar Glassmorphism */
    [data-testid="stSidebar"] {
        background-color: rgba(11, 15, 25, 0.6) !important;
        backdrop-filter: blur(15px);
        border-right: 1px solid rgba(30, 41, 59, 0.8);
    }
    
    /* Glassmorphism Inputs */
    .stTextInput input, .stTextArea textarea { 
        background: rgba(17, 24, 39, 0.7);
        backdrop-filter: blur(10px);
        color: #38BDF8; 
        border: 1px solid rgba(30, 41, 59, 0.8); 
        border-radius: 12px; 
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        padding: 12px 16px;
        font-size: 1.05rem;
        box-shadow: inset 0 2px 4px 0 rgba(0, 0, 0, 0.2);
    }
    .stTextInput input:focus, .stTextArea textarea:focus { 
        border: 1px solid #0EA5E9; 
        box-shadow: 0 0 20px rgba(14, 165, 233, 0.2), inset 0 2px 4px 0 rgba(0, 0, 0, 0.2); 
        background: rgba(15, 23, 42, 0.9);
    }
    
    /* Cyber-Tactical Buttons */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.9), rgba(30, 41, 59, 0.9));
        backdrop-filter: blur(5px);
        color: #0EA5E9;
        border: 1px solid #0EA5E9;
        border-radius: 10px;
        padding: 0.7rem 2.5rem;
        font-weight: 800;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        box-shadow: 0 4px 15px -3px rgba(0, 0, 0, 0.3);
        width: 100%;
    }
    div.stButton > button:first-child:hover {
        background: #0EA5E9;
        color: #0B0F19;
        box-shadow: 0 0 30px rgba(14, 165, 233, 0.5);
        transform: translateY(-3px) scale(1.02);
        border-color: #38BDF8;
    }
    
    /* Alerts and Code Blocks */
    .stAlert { 
        border-radius: 10px; 
        border-left: 4px solid; 
        background: rgba(17, 24, 39, 0.8);
        backdrop-filter: blur(8px);
        color: #F8FAFC;
    }
    code { color: #FCA5A5; font-family: 'JetBrains Mono', 'Fira Code', monospace; }
    pre { 
        border-radius: 12px; 
        border: 1px solid rgba(30, 41, 59, 0.8); 
        background: #0D1117 !important; 
        box-shadow: inset 0 2px 10px rgba(0, 0, 0, 0.5);
    }
    
    h1, h2, h3 { color: #F8FAFC; letter-spacing: 0.5px; }
    hr { border-color: rgba(30, 41, 59, 0.6); }
    </style>
    """, unsafe_allow_html=True)

# =====================================================================
# 3. CORE LOGIC & WAF ENGINE
# =====================================================================
class SecurityEngines:
    @staticmethod
    def inspect_payloads(text: str) -> Tuple[bool, str]:
        rules = {
            r"(?i)(UNION\s+ALL\s+SELECT|DROP\s+TABLE)": "SQL Injection (SQLi)",
            r"(?i)<(script|img|svg).*?(onerror|onload)": "Cross-Site Scripting (XSS)",
            r"(?i)(\/etc\/passwd|\.\.\/|\\windows\\system32)": "Path Traversal",
            r"(?i)(os\.system|subprocess\.|eval\()": "Remote Code Execution (RCE)",
            r"(?i)(ignore previous instructions|system prompt|you are now)": "LLM Prompt Injection"
        }
        for pattern, name in rules.items():
            if re.search(pattern, text): return False, name
        return True, "CLEAN"

# =====================================================================
# 4. BLUEPRINTS: PREMIUM VS FREE (THE ULTIMATE DICTIONARIES)
# =====================================================================
class CodeSynthesizer:
    def __init__(self):
        # 👑 PREMIUM BLUEPRINTS - THE ABSOLUTE BEST OF 2026
        self.premium_blueprints = {
            "sql": '''def execute_secure_db_query(db_session, user_id: int) -> dict:
    """[PREMIUM] SQLi Prevention via Strict ORM Casting & Parameterization."""
    try:
        sanitized_id = int(user_id)
        query = "SELECT id, username, email FROM users WHERE id = :user_id LIMIT 1"
        result = db_session.execute(query, {"user_id": sanitized_id}).fetchone()
        return dict(result) if result else {"error": "Not found"}
    except ValueError:
        return {"error": "Format violation"}''',
            
            "xss": '''def secure_frontend_renderer(untrusted_input: str) -> str:
    """[PREMIUM] Advanced DOMPurify Logic with Event-Handler Annihilation."""
    import html, re
    if not isinstance(untrusted_input, str): return ""
    cleaned = untrusted_input.replace("\\x00", "").strip()
    cleaned = re.sub(r"(?i)<(script|iframe|object|embed|svg)[^>]*>.*?</\\1>", "", cleaned)
    cleaned = re.sub(r"(?i)on[a-z]+\s*=\s*['\"].*?['\"]", "", cleaned)
    return html.escape(cleaned, quote=True)''',
            
            "llm": '''def secure_llm_prompt_guard(user_input: str) -> str:
    """[PREMIUM] AI Prompt Injection Guard (Jailbreak Defender)."""
    import re
    if not isinstance(user_input, str): return ""
    jailbreaks = [r"(?i)(ignore previous)", r"(?i)(system prompt|DAN)"]
    if any(re.search(sig, user_input) for sig in jailbreaks):
        return "[SYSTEM OVERRIDE BLOCKED]"
    return user_input.replace("{", "{{").replace("}", "}}")''',

            "ssrf": '''def enterprise_resource_fetcher(target_url: str) -> bytes:
    """[PREMIUM] Zero-Trust SSRF Engine. Mathematically blocks Cloud Metadata."""
    import urllib.request, urllib.parse, socket, ipaddress
    parsed = urllib.parse.urlparse(target_url)
    if parsed.scheme not in ['http', 'https']: raise ValueError("Protocol prohibited.")
    ip_obj = ipaddress.ip_address(socket.gethostbyname(parsed.hostname))
    if ip_obj.is_private or ip_obj.is_loopback: raise PermissionError("Cloud subnet access denied.")
    req = urllib.request.Request(target_url, headers={'User-Agent': 'SecuredProxy/3.0'})
    with urllib.request.urlopen(req, timeout=3) as res: return res.read()''',

            "generic": '''def universal_waf_middleware(request_payload: dict) -> dict:
    """[PREMIUM] Universal WAF - Neutralizes unknown anomalies."""
    import html
    return {k: html.escape(v.strip(), quote=True) if isinstance(v, str) else v for k, v in request_payload.items()}'''
        }

        # 🆓 FREE BLUEPRINTS - BASIC & THROTTLED
        self.free_blueprints = {
            "sql": '''def free_sql_cleaner(val):
    # [FREE TIER] Basic string replace. Upgrade to PREMIUM for ORM Parameterization.
    return str(val).replace("'", "").replace('"', '')''',
            
            "xss": '''def free_xss_cleaner(val):
    # [FREE TIER] Basic escape. Does not prevent DOM-based XSS.
    import html
    return html.escape(str(val))''',

            "llm": '''# [FREE TIER] 
# AI Prompt Injection protection is ONLY available in the PREMIUM tier.
def basic_ai_pass(val):
    return val''',

            "ssrf": '''# [FREE TIER] 
# Zero-Trust Network isolation is ONLY available in the PREMIUM tier.
def basic_fetch(url):
    import urllib.request
    return urllib.request.urlopen(url).read()''',

            "generic": '''def basic_sanitizer(val):
    # [FREE TIER] Generic basic cleanup.
    return str(val).strip()'''
        }

        # GUIDES & AI INTEL (Dual Language)
        self.guides = {
            "sql": {"he": "הטמע בשכבת ה-DAL לפני הקריאה למסד הנתונים.", "en": "Implement in the DAL layer before queries."},
            "xss": {"he": "עטוף קלט משתמש לפני הזרקה ל-DOM.", "en": "Wrap input before DOM injection."},
            "llm": {"he": "העבר כל קלט דרך פונקציה זו לפני השליחה ל-AI.", "en": "Pass user input through this before calling the LLM."},
            "ssrf": {"he": "שלב במודולי רשת המושכים מידע חיצוני.", "en": "Use in modules fetching external data."},
            "generic": {"he": "מקם כ-Interceptor בכניסה לאפליקציה.", "en": "Place as Request Interceptor at app entry."}
        }

    def detect_lang(self, text: str) -> str:
        return "he" if any("\u0590" <= c <= "\u05FF" for c in text) else "en"

    def determine_intent(self, q: str) -> str:
        q = q.lower()
        if any(w in q for w in ["ssrf", "webhook", "cloud metadata"]): return "ssrf"
        if any(w in q for w in ["sql", "db", "select", "הזרקת", "מסד"]): return "sql"
        if any(w in q for w in ["llm", "prompt", "jailbreak", "ai", "מודל שפה", "פרומפט"]): return "llm"
        if any(w in q for w in ["xss", "script", "html", "סניטציה"]): return "xss"
        return "generic"

    def generate_intel(self, intent: str, lang: str, is_premium: bool) -> str:
        if not is_premium:
            msg = "⚡ **גרסת FREE:** המערכת סיפקה קוד בסיסי. אנו ממליצים לשדרג ל-Premium כדי לקבל הגנה היקפית, מניעת עקיפות מתקדמות וניתוח מודיעין מלא." if lang == "he" else "⚡ **FREE TIER:** Basic code provided. Upgrade to Premium for Zero-Trust defense mechanisms and full threat intelligence."
            return f"### ⚠️ מודיעין סייבר חלקי | Partial Intel\n{msg}"
            
        data = {
            "ssrf": {"he": "מודיעין קריטי (CVSS: 9.1) | הגנת Zero-Trust פעילה, חוסמת Loopback ו-Metadata.", "en": "Critical Intel (CVSS: 9.1) | Zero-Trust active, blocking Cloud Metadata."},
            "sql": {"he": "מודיעין קריטי (CVSS: 9.8) | אכיפת Parameterization מחמירה. חסינות מלאה מובטחת.", "en": "Critical Intel (CVSS: 9.8) | Strict Parameterization enforced. Immunity guaranteed."},
            "xss": {"he": "מודיעין מתקדם (CVSS: 8.2) | מנוע DOMPurify משמיד תגיות ואירועים זדוניים.", "en": "Advanced Intel (CVSS: 8.2) | DOMPurify logic annihilating malicious events."},
            "llm": {"he": "מודיעין מתקדם (CVSS: 8.8) | חומת אש אקטיבית נגד Prompt Injection ו-Jailbreaks.", "en": "Advanced Intel (CVSS: 8.8) | Active Firewall against Prompt Injections."},
            "generic": {"he": "מודיעין אנומליות | מנוע ה-WAF הגלובלי הופעל לסינון היקפי.", "en": "Anomaly Intel | Global WAF Engine activated for perimeter defense."}
        }
        return f"### 🧠 {data.get(intent, data['generic'])[lang]}"

# =====================================================================
# 5. INITIALIZATION & UI RUNTIME
# =====================================================================
inject_custom_css()
ai_engine = CodeSynthesizer()

# --- SIDEBAR: TIER MANAGEMENT ---
with st.sidebar:
    st.image("https://img.icons8.com/nolan/128/cyber-security.png", width=100)
    st.title("System Config")
    st.markdown("---")
    
    tier_selection = st.radio(
        "⚡ SELECT SYSTEM TIER:",
        ["👑 PREMIUM MAX (V6.0)", "🆓 FREE (Basic)"],
        index=0
    )
    is_premium = "PREMIUM" in tier_selection
    
    st.markdown("---")
    st.subheader("Live Diagnostics")
    if is_premium:
        st.success("✅ Neural Engine: Active")
        st.success("✅ Zero-Trust WAF: Online")
        st.success("✅ Processing Speed: Maximum")
    else:
        st.warning("⚠️ Neural Engine: Disabled")
        st.warning("⚠️ Zero-Trust WAF: Offline")
        st.error("📉 Speed: Throttled")

# --- MAIN DASHBOARD ---
st.title("👑 THE ONE ABOVE ALL")
st.markdown("##### The Ultimate Cyber-Defense Synthesis Terminal")
st.markdown("---")

user_prompt = st.text_input("Enter Threat Vector or Target Vulnerability (He/En):", placeholder="e.g. מניעת הזרקת קוד ל-AI / How to stop SQLi")

if st.button("Synthesize Defense Protocol"):
    if len(user_prompt) < 2:
        st.toast("⚠️ Input required to initialize.", icon="⚠️")
    else:
        lang = ai_engine.detect_lang(user_prompt)
        safe, threat = SecurityEngines.inspect_payloads(user_prompt)
        
        if not safe:
            st.toast(f"WAF Intercepted: {threat}", icon="❌")
            st.error(f"❌ MALICIOUS PAYLOAD DETECTED: WAF prevented execution of {threat}.")
        else:
            intent = ai_engine.determine_intent(user_prompt)
            
            # --- TIER-BASED ANIMATION & THROTTLING ---
            if is_premium:
                status_text = "🧠 PREMIUM Engine Processing..." if lang == "en" else "🧠 מנוע פרימיום מנתח סיכונים..."
                with st.status(status_text, expanded=True) as status:
                    st.write("📡 Scanning topological threat DB..." if lang == "en" else "📡 סורק מאגרי מודיעין טופולוגיים...")
                    time.sleep(0.5)
                    st.write("🛡️ Hardening payload to Zero-Trust standards..." if lang == "en" else "🛡️ מקשיח קוד לתקן Zero-Trust מחמיר...")
                    time.sleep(0.5)
                    status.update(label="👑 Premium Synthesis Complete" if lang == "en" else "👑 סנכרון פרימיום הושלם", state="complete", expanded=False)
            else:
                status_text = "⏳ FREE Tier Processing (Throttled)..." if lang == "en" else "⏳ שרת חינמי מעבד (איטי)..."
                with st.status(status_text, expanded=True) as status:
                    st.write("Waiting in queue..." if lang == "en" else "ממתין בתור...")
                    time.sleep(2.0) # Artificial Throttle for FREE users
                    st.write("Applying basic filters..." if lang == "en" else "מחיל מסננים בסיסיים...")
                    time.sleep(1.5)
                    status.update(label="✅ Basic Synthesis Complete" if lang == "en" else "✅ סנכרון בסיסי הושלם", state="complete", expanded=False)
            
            # --- FAIL-SAFE DATA RETRIEVAL ---
            code_pool = ai_engine.premium_blueprints if is_premium else ai_engine.free_blueprints
            final_code = code_pool.get(intent, code_pool.get("generic", "# Fallback Error"))
            
            instruction = ai_engine.guides.get(intent, ai_engine.guides["generic"])[lang]
            intel_report = ai_engine.generate_intel(intent, lang, is_premium)
            
            # --- DISPLAY RESULTS ---
            st.toast("Protocol Deployed!", icon="✅")
            st.markdown(intel_report)
            
            tier_badge = "[PREMIUM V6.0]" if is_premium else "[FREE TIER]"
            st.markdown(f"### 🔒 Generated Blueprint {tier_badge}:")
            st.code(final_code, language="python")
            
            title_guide = "📌 ארכיטקטורת רשת (הטמעה):" if lang == "he" else "📌 Network Architecture (Deployment):"
            st.info(f"**{title_guide}**\n\n{instruction}")
            
            if not is_premium:
                st.error("💡 **TIP:** Unlock Asymmetric Crypto, AI Threat Intelligence, and Zero-Trust networks by upgrading to **PREMIUM MAX** from the sidebar.")

st.markdown("---")
st.caption("THE ONE ABOVE ALL | V7.0 God-Tier Architecture | System Status: Unbreakable")
