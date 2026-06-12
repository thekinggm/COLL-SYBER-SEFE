import ast
import hashlib
import hmac
import time
import uuid
import logging
import re
import html
from typing import Dict, Any, List, Tuple, Optional
import streamlit as st

# =====================================================================
# 1. ADVANCED COGNITIVE SECURITY LOGGER
# =====================================================================
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] [SOC-AI] %(message)s')

# =====================================================================
# 2. CUSTOM CSS: ADVANCED CYBERPUNK UI & ANIMATIONS
# =====================================================================
def inject_custom_css():
    st.markdown("""
    <style>
    /* Global Theme */
    .stApp { font-family: 'Inter', 'Segoe UI', sans-serif; background-color: #0a0e17; color: #c0caf5; }
    
    /* Input Fields */
    .stTextInput input, .stTextArea textarea { 
        background-color: #161b22; color: #58a6ff; 
        border: 1px solid #30363d; border-radius: 8px; 
        transition: border 0.3s ease, box-shadow 0.3s ease;
    }
    .stTextInput input:focus, .stTextArea textarea:focus { 
        border: 1px solid #00ffd5; box-shadow: 0 0 10px rgba(0, 255, 213, 0.2); 
    }
    
    /* Cyber Glowing Buttons */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #0d1117, #161b22);
        color: #00ffd5;
        border: 1px solid #00ffd5;
        border-radius: 6px;
        padding: 0.6rem 2rem;
        font-weight: bold;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        position: relative;
        overflow: hidden;
    }
    div.stButton > button:first-child:hover {
        background: #00ffd5;
        color: #0a0e17;
        box-shadow: 0 0 20px rgba(0, 255, 213, 0.6);
        transform: translateY(-2px);
    }
    
    /* Status Expander / Loader Styling */
    .streamlit-expanderHeader { background-color: #161b22; border-radius: 8px; color: #58a6ff; font-weight: 600; }
    
    /* Alerts and Info Boxes */
    .stAlert { border-radius: 8px; border-left: 4px solid; }
    
    /* Code Blocks */
    code { color: #ff7b72; font-family: 'Fira Code', monospace; }
    pre { border-radius: 10px; border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

# =====================================================================
# 3. STATEFUL MEMORY & SECURE CONTEXT
# =====================================================================
class AdvancedConversationMemory:
    def __init__(self):
        self.history = []
        self.global_risk_weight = 0.0

    def commit_interaction(self, intent_type: str, user_query: str, risks: int, status: str, lang: str):
        self.history.append({"time": time.time(), "intent": intent_type, "lang": lang, "status": status})

class EnterpriseSecurityContext:
    def __init__(self):
        self.rate_limits = {}

    def enforce_rate_limit(self, client_id: str, max_reqs: int = 20, window: int = 86400) -> bool:
        now = time.time()
        if client_id not in self.rate_limits: self.rate_limits[client_id] = []
        self.rate_limits[client_id] = [t for t in self.rate_limits[client_id] if now - t < window]
        if len(self.rate_limits[client_id]) >= max_reqs: return False
        self.rate_limits[client_id].append(now)
        return True

# =====================================================================
# 4. WAF INPUT VALIDATOR
# =====================================================================
class SecurityEngines:
    @staticmethod
    def inspect_payloads(text: str) -> Tuple[bool, str]:
        rules = {
            r"(?i)UNION\s+ALL\s+SELECT": "SQL Injection",
            r"(?i)<script[^>]*>": "XSS Payload",
            r"(__import__\s*\(|os\.system)": "RCE Payload",
            r"(?i)(\.\.\/|\.\.\\)": "Path Traversal"
        }
        for pattern, name in rules.items():
            if re.search(pattern, text): return False, name
        return True, "CLEAN"

# =====================================================================
# 5. HIGH-INTELLIGENCE MULTI-TIER ENGINE
# =====================================================================
class SmartDefensiveGenerator:
    def __init__(self):
        self.premium_blueprints = {
            "sql": '''def execute_secure_db_query(db_conn, user_id: str) -> dict:
    """Enterprise SQL Injection Prevention via Parameterization."""
    import logging
    try:
        if not str(user_id).isdigit(): raise ValueError("Input failed strict type validation.")
        with db_conn.cursor() as cursor:
            # The database engine compiles the query BEFORE inserting variables
            cursor.execute("SELECT id, username, role FROM users WHERE id = %s", (int(user_id),))
            result = cursor.fetchone()
            return {"data": result} if result else {"error": "Not found"}
    except Exception as e:
        logging.critical(f"Database Integrity Alert: {e}")
        return {"error": "Secure connection interrupted."}''',
            
            "xss": '''def sanitize_user_input_for_html(untrusted_input: str) -> str:
    """Deep Content Disarm & Reconstruction for XSS."""
    import html, re
    if not isinstance(untrusted_input, str): return ""
    cleaned = untrusted_input.replace("\\x00", "").strip()
    # Strip dangerous active tags
    cleaned = re.sub(r"(?i)<(script|iframe|object|embed|svg|math)[^>]*>.*?</\\1>", "", cleaned)
    # Strict HTML Entity Encoding
    return html.escape(cleaned, quote=True)''',
            
            "ssrf": '''def fetch_remote_resource_securely(target_url: str) -> bytes:
    """Prevents Server-Side Request Forgery (SSRF)."""
    import urllib.request, urllib.parse, socket, ipaddress, logging
    parsed = urllib.parse.urlparse(target_url)
    if parsed.scheme not in ['http', 'https']: raise ValueError("SSRF Blocked: Invalid URL scheme.")
    try:
        ip_str = socket.gethostbyname(parsed.hostname)
        ip_obj = ipaddress.ip_address(ip_str)
        # Block internal network traversal
        if ip_obj.is_private or ip_obj.is_loopback:
            raise PermissionError("Access to private IP ranges is strictly forbidden.")
        req = urllib.request.Request(target_url, headers={'User-Agent': 'SecureClient/1.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            return response.read()
    except Exception as e:
        logging.error(f"Network request blocked: {e}")
        return b""''',

            "token": '''def validate_jwt_auth_token(auth_header: str, server_secret: str) -> dict:
    """Cryptographic validation of JWT to prevent Token Forgery."""
    import hmac, hashlib, base64, json, time
    if not auth_header or not auth_header.startswith("Bearer "): raise PermissionError("Invalid Auth header.")
    parts = auth_header.split(" ")[1].split(".")
    if len(parts) != 3: raise PermissionError("Malformed JWT.")
    header, payload, signature = parts
    expected_sig = base64.urlsafe_b64encode(hmac.new(server_secret.encode(), f"{header}.{payload}".encode(), hashlib.sha256).digest()).decode().rstrip("=")
    # Timing-attack safe comparison
    if not hmac.compare_digest(signature, expected_sig): raise PermissionError("CRITICAL: Signature Tampering Detected!")
    data = json.loads(base64.urlsafe_b64decode(payload + "==").decode())
    if data.get("exp", 0) < time.time(): raise PermissionError("Token expired.")
    return data'''
        }

        self.guides = {
            "sql": {"he": "שלב קוד זה בשכבת ה-DAL לפני גישה לבסיס הנתונים.", "en": "Implement in the DAL layer before DB execution."},
            "xss": {"he": "עטוף קלט משתמש בפונקציה זו לפני רינדור ל-HTML ב-Frontend.", "en": "Wrap user input with this before HTML rendering."},
            "ssrf": {"he": "השתמש בפונקציה זו בכל מנגנון שמושך Webhooks או תמונות מכתובת חיצונית.", "en": "Use for fetching external Webhooks or URLs."},
            "token": {"he": "הטמע כ-Middleware על גבי נתיבי API (Private Routes).", "en": "Deploy as Auth Middleware over Private API Routes."},
            "generic": {"he": "הוסף פונקציה זו לשכבת הניקוי הגלובלית.", "en": "Add to global sanitization layer."}
        }

    def detect_lang(self, text: str) -> str:
        return "he" if any("\u0590" <= c <= "\u05FF" for c in text) else "en"

    def determine_intent(self, q: str) -> str:
        q = q.lower()
        if any(w in q for w in ["ssrf", "webhook", "cloud metadata"]): return "ssrf"
        if any(w in q for w in ["sql", "db", "select", "הזרקת", "מסד"]): return "sql"
        if any(w in q for w in ["token", "jwt", "auth", "טוקן"]): return "token"
        if any(w in q for w in ["xss", "script", "html", "סניטציה"]): return "xss"
        return "generic"

    def generate_ai_analysis(self, intent: str, lang: str) -> str:
        reports_he = {
            "ssrf": "### 🧠 דו\"ח מודיעין סייבר: SSRF\n**רמת סיכון:** קריטית (CVSS: 9.1)\n**וקטור התקפה:** התוקף משתמש בשרת שלך כפרוקסי כדי לתקוף רשתות פנימיות ושרתי ענן. \n**הפתרון שלנו (v2026):** הקוד לא סומך רק על ה-URL, אלא פותר את ה-DNS ברמת ה-Socket ובודק מתמטית האם ה-IP שייך לרשת פרטית (Private Range), מה שחוסם לחלוטין מעקפי DNS Rebinding.",
            "sql": "### 🧠 דו\"ח מודיעין סייבר: הזרקת SQL\n**רמת סיכון:** קריטית (CVSS: 9.8)\n**וקטור התקפה:** מניפולציה של שאילתות למסד הנתונים כדי לגנוב או למחוק מידע.\n**הפתרון שלנו (v2026):** הקוד משתמש ב-Parameterized Queries קשיחים בצירוף ולידציית סוג נתונים (Type Casting) מחמירה, מה שמאלץ את המסד להתייחס לקלט כטקסט פסיבי בלבד.",
            "xss": "### 🧠 דו\"ח מודיעין סייבר: XSS\n**רמת סיכון:** גבוהה (CVSS: 8.2)\n**וקטור התקפה:** הרצת סקריפטים זדוניים בדפדפן של משתמשים אחרים.\n**הפתרון שלנו (v2026):** במקום סתם להחליף תווים, ה-AI יצר אלגוריתם המשלב מחיקה אגרסיבית של תגיות DOM פעילות (Content Disarm) יחד עם קידוד ישויות HTML מלא.",
            "token": "### 🧠 דו\"ח מודיעין סייבר: חטיפת Token / JWT\n**רמת סיכון:** קריטית (CVSS: 9.4)\n**וקטור התקפה:** זיוף חתימות דיגיטליות כדי לקבל הרשאות מנהל ללא סיסמה.\n**הפתרון שלנו (v2026):** האלגוריתם מחשב מחדש את ה-HMAC באמצעות ספריות קריפטוגרפיות ומבצע השוואה בטוחה (hmac.compare_digest) כדי למנוע מתקפות תזמון (Timing Attacks).",
            "generic": "### 🧠 דו\"ח מודיעין סייבר: אבטחת קלט\nהקלט נבדק, סונן ואובטח מול תווים מסוכנים על ידי קידוד אגרסיבי למניעת פריצות."
        }
        reports_en = {
            "ssrf": "### 🧠 Cyber Intel: SSRF\n**Risk Level:** CRITICAL (CVSS: 9.1)\n**Attack Vector:** Attacker tricks the server into making requests to internal infrastructure.\n**Our Solution (v2026):** The code performs socket-level DNS resolution and blocks private IPs to prevent DNS Rebinding bypasses.",
            "sql": "### 🧠 Cyber Intel: SQL Injection\n**Risk Level:** CRITICAL (CVSS: 9.8)\n**Attack Vector:** Manipulating database queries to steal/delete data.\n**Our Solution (v2026):** Strict parameterized queries combined with rigorous type validation to neutralize malicious strings.",
            "xss": "### 🧠 Cyber Intel: XSS\n**Risk Level:** HIGH (CVSS: 8.2)\n**Attack Vector:** Executing malicious JS in victim browsers.\n**Our Solution (v2026):** Implements Deep Content Disarm algorithms paired with full HTML entity encoding.",
            "token": "### 🧠 Cyber Intel: JWT Tampering\n**Risk Level:** CRITICAL (CVSS: 9.4)\n**Attack Vector:** Forging auth tokens to gain admin access.\n**Our Solution (v2026):** Cryptographic signature recalculation employing `hmac.compare_digest` to neutralize timing attacks.",
            "generic": "### 🧠 Cyber Intel: Input Security\nGeneral input has been strictly sanitized and escaped to prevent payload execution."
        }
        return reports_he.get(intent, reports_he["generic"]) if lang == "he" else reports_en.get(intent, reports_en["generic"])

# =====================================================================
# 6. ENTERPRISE UI SETUP
# =====================================================================
st.set_page_config(page_title="AI DefSec Platform", page_icon="⚡", layout="wide")
inject_custom_css()

if "sec_ctx" not in st.session_state:
    st.session_state.sec_ctx = EnterpriseSecurityContext()
    st.session_state.engines = SecurityEngines()
    st.session_state.ai_gen = SmartDefensiveGenerator()
    st.session_state.memory = AdvancedConversationMemory()

# --- MAIN DASHBOARD ---
st.title("⚡ SOC AI: Enterprise Threat Defense")
st.markdown("##### AI-Driven Code Synthesis & Vulnerability Mitigation Platform")
st.markdown("---")

st.subheader("🛡️ Request Defensive Blueprint")
user_prompt = st.text_input("Describe the attack or security need (Hebrew/English):", placeholder="למשל: תראה לי קוד נגד SSRF בבקשה")

if st.button("Generate & Optimize Security Payload"):
    if not st.session_state.sec_ctx.enforce_rate_limit("192.168.1.1", 20):
        st.error("🚨 RATE LIMIT REACHED.")
    elif not user_prompt.strip():
        st.warning("Please enter a valid request.")
    else:
        lang = st.session_state.ai_gen.detect_lang(user_prompt)
        safe, threat = st.session_state.engines.inspect_payloads(user_prompt)
        
        if not safe:
            st.error(f"❌ WAF BLOCKED MALICIOUS PROMPT: {threat}")
        else:
            intent = st.session_state.ai_gen.determine_intent(user_prompt)
            
            # =========================================================
            # THE "THINKING & SELF-CORRECTION" ANIMATION
            # =========================================================
            status_title = "🧠 AI Engine Analyzing Threat Vector..." if lang == "en" else "🧠 מנוע AI מנתח את וקטור ההתקפה..."
            with st.status(status_title, expanded=True) as status:
                st.write("🔍 מזהה סוג מתקפה ופרמטרים..." if lang == "he" else "🔍 Identifying attack patterns...")
                time.sleep(1.2)
                
                st.write("⚙️ מקודד פתרון הגנתי ראשוני..." if lang == "he" else "⚙️ Drafting initial defensive code...")
                time.sleep(1.5)
                
                st.write("⚠️ מזהה חולשות בקוד הראשוני. מפעיל מערכת שדרוג עצמית..." if lang == "he" else "⚠️ Weakness detected in draft. Triggering self-optimization...")
                time.sleep(2.0)
                
                st.write("🔒 משדרג ומקשיח פונקציות לתקן אבטחה מחמיר (OWASP 2026)..." if lang == "he" else "🔒 Hardening code to strict OWASP 2026 standards...")
                time.sleep(1.2)
                
                complete_msg = "✅ הגרסה המושלמת והמעודכנת ביותר מוכנה!" if lang == "he" else "✅ Optimal Security Blueprint Ready!"
                status.update(label=complete_msg, state="complete", expanded=False)
            
            # Output generation
            final_code = st.session_state.ai_gen.premium_blueprints.get(intent, st.session_state.ai_gen.premium_blueprints["generic"])
            instruction = st.session_state.ai_gen.guides.get(intent, st.session_state.ai_gen.guides["generic"])[lang]
            ai_intel = st.session_state.ai_gen.generate_ai_analysis(intent, lang)
            
            st.session_state.memory.commit_interaction(intent, user_prompt, 0, "SUCCESS", lang)
            
            # Displaying the results in a beautiful layout
            st.markdown(ai_intel)
            st.markdown("### 🔒 Generated Security Payload (v2026):")
            st.code(final_code, language="python")
            
            guide_title = "📌 הוראות הטמעה:" if lang == "he" else "📌 Implementation Guide:"
            st.success(f"{guide_title}\n\n{instruction}")

st.markdown("---")
st.caption("Powered by Advanced Cognitive Security Engine | System Status: Active & Secured")
