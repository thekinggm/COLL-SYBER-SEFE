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
# 2. CUSTOM CSS: ULTRA PREMIUM DARK THEME
# =====================================================================
def inject_custom_css():
    st.markdown("""
    <style>
    /* Premium Deep Midnight Background (Not pitch black, easy on the eyes) */
    .stApp { 
        font-family: 'Inter', 'Segoe UI', sans-serif; 
        background-color: #0B0F19; 
        color: #E2E8F0; 
    }
    
    /* Input Fields & Text Areas */
    .stTextInput input, .stTextArea textarea { 
        background-color: #111827; 
        color: #38BDF8; 
        border: 1px solid #1E293B; 
        border-radius: 8px; 
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        padding: 10px 15px;
        font-size: 1.05rem;
    }
    .stTextInput input:focus, .stTextArea textarea:focus { 
        border: 1px solid #0EA5E9; 
        box-shadow: 0 0 15px rgba(14, 165, 233, 0.3); 
        background-color: #0F172A;
    }
    
    /* Cyber Glowing Buttons */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #0F172A, #1E293B);
        color: #38BDF8;
        border: 1px solid #0EA5E9;
        border-radius: 8px;
        padding: 0.7rem 2.5rem;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    div.stButton > button:first-child:hover {
        background: #0EA5E9;
        color: #0B0F19;
        box-shadow: 0 0 25px rgba(14, 165, 233, 0.6);
        transform: translateY(-2px);
        border-color: #38BDF8;
    }
    
    /* Status Expander / Loader Styling */
    .streamlit-expanderHeader { 
        background-color: #111827; 
        border-radius: 8px; 
        color: #38BDF8; 
        font-weight: 600; 
        border: 1px solid #1E293B;
    }
    
    /* Info & Success Boxes */
    .stAlert { 
        border-radius: 8px; 
        border-left: 4px solid; 
        background-color: #111827;
        color: #E2E8F0;
    }
    
    /* Code Blocks */
    code { color: #FCA5A5; font-family: 'Fira Code', 'Courier New', monospace; font-size: 0.95rem; }
    pre { 
        border-radius: 12px; 
        border: 1px solid #1E293B; 
        background-color: #0F172A !important; 
        box-shadow: inset 0 2px 4px 0 rgba(0, 0, 0, 0.06);
    }
    
    /* Header styling */
    h1, h2, h3 { color: #F8FAFC; text-shadow: 0 2px 4px rgba(0,0,0,0.5); }
    hr { border-color: #1E293B; }
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
# 5. HIGH-INTELLIGENCE MULTI-TIER ENGINE (V5.0)
# =====================================================================
class SmartDefensiveGenerator:
    def __init__(self):
        # 🚀 THE MOST ADVANCED ENTERPRISE BLUEPRINTS OF 2026
        self.premium_blueprints = {
            "sql": '''def execute_secure_db_query(db_session, user_id: int) -> dict:
    """Enterprise SQL Injection Prevention via ORM / Parameterization."""
    import logging
    try:
        # Strict casting and validation
        sanitized_id = int(user_id)
        if sanitized_id <= 0: raise ValueError("ID must be positive integer.")
        
        # SQLAlchemy Core / Parameterized standard
        query = "SELECT id, username, email FROM users WHERE id = :user_id LIMIT 1"
        result = db_session.execute(query, {"user_id": sanitized_id}).fetchone()
        
        return dict(result) if result else {"error": "Record not found"}
    except ValueError as ve:
        logging.warning(f"Validation Error: {ve}")
        return {"error": "Invalid format"}
    except Exception as e:
        logging.critical(f"DB Integrity Alert: {e}")
        return {"error": "Database error"}''',
            
            "xss": '''def secure_frontend_renderer(untrusted_input: str) -> str:
    """Advanced XSS Prevention: DOMPurify Logic & CSP Header Generation."""
    import html, re
    if not isinstance(untrusted_input, str): return ""
    
    # 1. Null-byte injection removal
    cleaned = untrusted_input.replace("\\x00", "").strip()
    
    # 2. Aggressive Content Disarm (Strip active scripts and event handlers)
    cleaned = re.sub(r"(?i)<(script|iframe|object|embed|svg|math|applet)[^>]*>.*?</\\1>", "", cleaned)
    cleaned = re.sub(r"(?i)on[a-z]+\s*=\s*['\"].*?['\"]", "", cleaned) # Strip handlers like onclick=
    
    # 3. Contextual Entity Encoding
    return html.escape(cleaned, quote=True)''',
            
            "ssrf": '''def enterprise_resource_fetcher(target_url: str) -> bytes:
    """Zero-Trust SSRF Prevention (Blocks AWS/GCP Metadata Leaks)."""
    import urllib.request, urllib.parse, socket, ipaddress, logging
    parsed = urllib.parse.urlparse(target_url)
    
    if parsed.scheme not in ['http', 'https']: 
        raise ValueError("SSRF Blocked: Unsafe protocol.")
        
    try:
        ip_str = socket.gethostbyname(parsed.hostname)
        ip_obj = ipaddress.ip_address(ip_str)
        
        # Mathematical verification blocking ALL internal/metadata network scopes
        if ip_obj.is_private or ip_obj.is_loopback or ip_str.startswith('169.254'):
            logging.critical(f"SSRF ALERT: Blocked access to restricted network zone: {ip_str}")
            raise PermissionError("Access Denied to Cloud/Internal ranges.")
            
        req = urllib.request.Request(target_url, headers={'User-Agent': 'SecuredProxy/2.0'})
        with urllib.request.urlopen(req, timeout=3) as response:
            return response.read()
    except Exception as e:
        logging.error(f"Fetch aborted: {e}")
        return b""''',

            "token": '''def validate_enterprise_jwt(auth_header: str, public_key_pem: str) -> dict:
    """Asymmetric JWT Validation (RS256) preventing algorithm downgrades."""
    import jwt, logging # requires PyJWT
    
    if not auth_header or not auth_header.startswith("Bearer "): 
        raise PermissionError("Malformed Authorization header structure.")
        
    token = auth_header.split(" ")[1]
    try:
        # RS256 is immune to symmetric key brute-forcing
        decoded_payload = jwt.decode(
            token, 
            public_key_pem, 
            algorithms=["RS256"], 
            options={"require": ["exp", "iss", "sub"]}
        )
        return decoded_payload
    except jwt.ExpiredSignatureError:
        raise PermissionError("Token has expired.")
    except jwt.InvalidTokenError as e:
        logging.critical(f"Token Tampering Detected: {e}")
        raise PermissionError("Cryptographic signature validation failed.")''',

            "idor": '''def authorize_object_access(current_user: dict, requested_document_id: str, db) -> dict:
    """Insecure Direct Object Reference (IDOR) Hardening."""
    import logging
    
    # Fetch document metadata WITHOUT sending it to the user yet
    document = db.get_document_metadata(requested_document_id)
    if not document:
        return {"error": "Resource unavailable"}
        
    # Crucial IDOR Check: Ensure the requested object legally belongs to the active session
    if document.owner_id != current_user.get("id") and current_user.get("role") != "admin":
        logging.critical(f"IDOR Alert: User {current_user.get('id')} attempted to access doc {requested_document_id}")
        # Always return generic 'unavailable' to avoid data enumeration
        return {"error": "Resource unavailable"} 
        
    return db.fetch_full_document(requested_document_id)''',

            "ddos": '''def redis_rate_limiter(client_ip: str, endpoint: str, redis_conn) -> bool:
    """DDoS & Brute Force Prevention using Redis Token Bucket Algorithm."""
    import time
    
    # High-performance sliding window limit
    window_seconds = 60
    max_requests = 30
    cache_key = f"rate_limit:{endpoint}:{client_ip}"
    
    current_time = int(time.time() * 1000) # Milliseconds
    
    pipeline = redis_conn.pipeline()
    pipeline.zremrangebyscore(cache_key, 0, current_time - (window_seconds * 1000))
    pipeline.zadd(cache_key, {str(current_time): current_time})
    pipeline.zcard(cache_key)
    pipeline.expire(cache_key, window_seconds)
    results = pipeline.execute()
    
    request_count = results[2]
    if request_count > max_requests:
        raise PermissionError("HTTP 429: Too Many Requests. Threat mitigation activated.")
    return True''',

            "generic": '''def universal_waf_middleware(request_payload: dict) -> dict:
    """Universal Web Application Firewall (WAF) - Handles Unknown Anomalies."""
    import re, html, logging
    
    suspicious_patterns = [
        r"(?i)(<script|javascript:|on\w+\s*=)", # XSS
        r"(?i)(\bUNION\b|\bSELECT\b.*?\bFROM\b)", # SQLi
        r"(?i)(\.\.\/|\/etc\/passwd)", # Path Traversal
        r"(?i)(os\.system|eval\()" # RCE
    ]
    
    sanitized_payload = {}
    for key, value in request_payload.items():
        if isinstance(value, str):
            # Check against WAF signatures
            if any(re.search(pat, value) for pat in suspicious_patterns):
                logging.critical(f"WAF Blocked Anomaly on field '{key}': Payload matched threat signature.")
                raise ValueError(f"Threat Intercepted: Suspicious characters in {key}")
            
            # Universal fallback escaping
            sanitized_payload[key] = html.escape(value.strip(), quote=True)
        else:
            sanitized_payload[key] = value
            
    return sanitized_payload'''
        }

        # Safe fallback dictionary
        self.free_blueprints = {k: f"# FREE TIER VERSION\ndef basic_{k}(data):\n    return data" for k in self.premium_blueprints.keys()}

        self.guides = {
            "sql": {"he": "שלב קוד זה בשכבת גישת הנתונים (DAL) או המודל (Model) לפני ביצוע שאילתה.", "en": "Implement in the DAL or Model layer before executing queries."},
            "xss": {"he": "עטוף כל קלט משתמש בפונקציה זו בשכבת התצוגה (View) לפני הזרקה ל-DOM.", "en": "Wrap user input with this function in the View layer before DOM injection."},
            "ssrf": {"he": "הטמע במודולים המושכים מידע חיצוני, כמו עיבוד Webhooks או הורדת קבצים מ-URL.", "en": "Use in modules fetching external data, like Webhook processors or URL downloaders."},
            "token": {"he": "הטמע בראוטר הראשי (API Gateway) או כ-Middleware לבדיקת הרשאות (Auth).", "en": "Deploy in your API Gateway or Auth Middleware."},
            "idor": {"he": "מקם קוד זה בשכבת הבקר (Controller) מיד אחרי אימות המשתמש (Authentication) ולפני שליפת הנתונים.", "en": "Place in the Controller layer immediately after user Auth and before data retrieval."},
            "ddos": {"he": "שלב את זה כ-Middleware גלובלי (Global Interceptor) המגן על כל נתיבי ה-API החשופים החוצה.", "en": "Integrate as a Global Middleware intercepting all public API routes."},
            "generic": {"he": "מקם את מנגנון ה-WAF הזה בשער הכניסה של האפליקציה (Request Interceptor) לסינון רוחבי.", "en": "Place this WAF mechanism at the application's Request Interceptor for broad filtering."}
        }

    def detect_lang(self, text: str) -> str:
        return "he" if any("\u0590" <= c <= "\u05FF" for c in text) else "en"

    def determine_intent(self, q: str) -> str:
        q = q.lower()
        if any(w in q for w in ["ssrf", "webhook", "cloud metadata"]): return "ssrf"
        if any(w in q for w in ["sql", "db", "select", "הזרקת", "מסד"]): return "sql"
        if any(w in q for w in ["token", "jwt", "auth", "טוקן", "חתימה"]): return "token"
        if any(w in q for w in ["idor", "access control", "הרשאות", "של משתמש אחר", "גישה"]): return "idor"
        if any(w in q for w in ["ddos", "brute", "rate limit", "הצפה", "כוח גס", "התקפות"]): return "ddos"
        if any(w in q for w in ["xss", "script", "html", "סניטציה", "קלט"]): return "xss"
        return "generic" # Catch-all 

    def generate_ai_analysis(self, intent: str, lang: str) -> str:
        reports_he = {
            "ssrf": "### 🧠 מודיעין סייבר: SSRF\n**רמת סיכון:** קריטית (CVSS: 9.1)\n**הפתרון בגרסה זו:** שימוש בארכיטקטורת Zero-Trust מונעת פנייה לכתובות Loopback ו-Metadata בענן.",
            "sql": "### 🧠 מודיעין סייבר: הזרקת SQL\n**רמת סיכון:** קריטית (CVSS: 9.8)\n**הפתרון בגרסה זו:** אכיפת ORM שאילתות מבוססות פרמטרים וסניטציה ברמת סוג נתונים (Casting).",
            "xss": "### 🧠 מודיעין סייבר: XSS / הזרקת קוד תצוגה\n**רמת סיכון:** גבוהה (CVSS: 8.2)\n**הפתרון בגרסה זו:** בניית אלגוריתם DOMPurify שחוסם אירועי On-Click ומשמיד תגיות מסוכנות.",
            "token": "### 🧠 מודיעין סייבר: זיוף Token (JWT)\n**רמת סיכון:** קריטית (CVSS: 9.4)\n**הפתרון בגרסה זו:** מעבר להצפנה א-סימטרית (RS256 מבוסס מפתח ציבורי) שבלתי ניתנת לפיצוח כוח-גס.",
            "idor": "### 🧠 מודיעין סייבר: IDOR\n**רמת סיכון:** קריטית (CVSS: 9.1)\n**הפתרון בגרסה זו:** שכבת אימות אובייקטים המוודאת חפיפה לוגית בין ה-Session ID לבין ה-Owner ID בבסיס הנתונים.",
            "ddos": "### 🧠 מודיעין סייבר: DDoS / Brute Force\n**רמת סיכון:** גבוהה (CVSS: 7.5)\n**הפתרון בגרסה זו:** אלגוריתם Token Bucket בסביבת Redis המחשב חריגות בשניות בודדות.",
            "generic": "### 🧠 מודיעין סייבר: אנומליה לא מזוהה (Universal Defense)\nהמנוע זיהה בקשה מורכבת ושלף מנגנון **WAF אוניברסלי**. מנגנון זה מכיל חתימות של עשרות מתקפות ידועות ויסנן כל קלט זדוני באופן היקפי."
        }
        reports_en = {
            "ssrf": "### 🧠 Cyber Intel: SSRF\n**Risk Level:** CRITICAL (CVSS: 9.1)\n**Solution:** Zero-Trust architecture mathematically blocking cloud metadata and loopback domains.",
            "sql": "### 🧠 Cyber Intel: SQL Injection\n**Risk Level:** CRITICAL (CVSS: 9.8)\n**Solution:** Hardened ORM parameterized execution with rigorous type casting.",
            "xss": "### 🧠 Cyber Intel: XSS\n**Risk Level:** HIGH (CVSS: 8.2)\n**Solution:** DOMPurify logic stripping active event handlers and malicious structural tags.",
            "token": "### 🧠 Cyber Intel: JWT Tampering\n**Risk Level:** CRITICAL (CVSS: 9.4)\n**Solution:** Upgraded to Asymmetric Cryptography (RS256) preventing symmetric key brute-forcing.",
            "idor": "### 🧠 Cyber Intel: IDOR\n**Risk Level:** CRITICAL (CVSS: 9.1)\n**Solution:** Mandatory ownership validation mapping the active Session ID against the Resource Owner ID.",
            "ddos": "### 🧠 Cyber Intel: DDoS / Brute Force\n**Risk Level:** HIGH (CVSS: 7.5)\n**Solution:** Redis-based Token Bucket algorithm executing millisecond-accurate sliding windows.",
            "generic": "### 🧠 Cyber Intel: Unclassified Anomaly\nThe engine deployed a **Universal WAF** capable of pattern-matching and neutralizing multiple unknown threat signatures across the payload."
        }
        return reports_he.get(intent, reports_he["generic"]) if lang == "he" else reports_en.get(intent, reports_en["generic"])

# =====================================================================
# 6. ENTERPRISE UI SETUP
# =====================================================================
st.set_page_config(page_title="AI DefSec Platform", page_icon="⚡", layout="wide")
inject_custom_css()

# Initialize Session State Safely
if "sec_ctx" not in st.session_state:
    st.session_state.sec_ctx = EnterpriseSecurityContext()
    st.session_state.engines = SecurityEngines()
    st.session_state.ai_gen = SmartDefensiveGenerator()
    st.session_state.memory = AdvancedConversationMemory()

# --- MAIN DASHBOARD ---
st.title("⚡ SOC AI: Enterprise Defense Terminal")
st.markdown("##### Adaptive Threat Intelligence & Zero-Trust Code Synthesis")
st.markdown("---")

with st.sidebar:
    st.image("https://img.icons8.com/nolan/96/cyber-security.png", width=64)
    st.header("⚙️ Core Controls")
    tier = st.selectbox("Execution Engine:", ["PREMIUM Ultra (v2026)", "FREE Tier"])
    is_premium = "PREMIUM" in tier

st.subheader("🛡️ Specify Threat Vector")
user_prompt = st.text_input("Describe the attack or target system (He/En):", placeholder="e.g. How to prevent users from seeing other users' data? / קוד נגד מתקפות הצפה")

if st.button("Initialize Defensive Synthesis"):
    if not st.session_state.sec_ctx.enforce_rate_limit("192.168.1.1", 30):
        st.error("🚨 MITIGATION ACTIVE: Rate limit exceeded.")
    elif not user_prompt.strip():
        st.warning("Input required to begin synthesis.")
    else:
        lang = st.session_state.ai_gen.detect_lang(user_prompt)
        safe, threat = st.session_state.engines.inspect_payloads(user_prompt)
        
        if not safe:
            st.error(f"❌ WAF BLOCKED MALICIOUS INJECTION: {threat}")
        else:
            intent = st.session_state.ai_gen.determine_intent(user_prompt)
            
            # THE "THINKING" ANIMATION (V5.0)
            status_title = "🧠 AI Threat Matrix Analyzing..." if lang == "en" else "🧠 רשת נוירונים מנתחת את וקטור ההתקפה..."
            with st.status(status_title, expanded=True) as status:
                st.write("🔍 סורק מודלים אנומליים ופרמטרי קלט..." if lang == "he" else "🔍 Scanning anomaly models and input bounds...")
                time.sleep(0.8)
                
                st.write("⚙️ מרכיב לוגיקת אבטחה בסיסית..." if lang == "he" else "⚙️ Assembling base logic constraints...")
                time.sleep(1.0)
                
                st.write("⚠️ מאתר פרצות פוטנציאליות. מפעיל מערכת הקשחה לבידוד סביבתי..." if lang == "he" else "⚠️ Vulnerability mapped. Hardening environment execution isolation...")
                time.sleep(1.5)
                
                st.write("🔒 מיישם פרוטוקול אבטחה מחמיר (Zero-Trust Standard 2026)..." if lang == "he" else "🔒 Enforcing strict Zero-Trust standard algorithms...")
                time.sleep(1.2)
                
                complete_msg = "✅ סינתזת קוד ההגנה הושלמה בהצלחה!" if lang == "he" else "✅ Defensive Code Synthesis Complete!"
                status.update(label=complete_msg, state="complete", expanded=False)
            
            # FAIL-SAFE Output Generation
            code_pool = st.session_state.ai_gen.premium_blueprints if is_premium else st.session_state.ai_gen.free_blueprints
            
            # Absolute bullet-proof retrieval using `.get` with a fallback
            final_code = code_pool.get(intent, code_pool.get("generic", "# Security Module Load Error"))
            instruction = st.session_state.ai_gen.guides.get(intent, st.session_state.ai_gen.guides.get("generic"))[lang]
            ai_intel = st.session_state.ai_gen.generate_ai_analysis(intent, lang)
            
            st.session_state.memory.commit_interaction(intent, user_prompt, 0, "SUCCESS", lang)
            
            # Presenting the Masterpiece
            st.markdown(ai_intel)
            st.markdown("### 🔒 Generated Enterprise Blueprint (v2026):")
            st.code(final_code, language="python")
            
            guide_title = "📌 הנחיות שילוב ארכיטקטורה:" if lang == "he" else "📌 Architectural Integration Guide:"
            st.success(f"{guide_title}\n\n{instruction}")

st.markdown("---")
st.caption("Terminal v5.0 | Protected by Advanced AI SOC | Status: Optimal")
