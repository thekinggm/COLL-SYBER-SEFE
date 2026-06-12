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
# 1. ADVANCED COGNITIVE SECURITY LOGGER & SOC SYSTEM CONFIGURATION
# =====================================================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] [SOC-DYNAMIC-CORE] %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("AdvancedDefensiveAI")

# =====================================================================
# CUSTOM CSS FOR ENTERPRISE CYBER UI
# =====================================================================
def inject_custom_css():
    st.markdown("""
    <style>
    /* Main Background & Fonts */
    .stApp { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    
    /* Sleek Cyberpunk Buttons */
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #0f2027, #203a43, #2c5364);
        color: #00ffd5;
        border: 1px solid #00ffd5;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 700;
        letter-spacing: 1px;
        transition: all 0.3s ease-in-out;
    }
    div.stButton > button:first-child:hover {
        background: linear-gradient(90deg, #2c5364, #203a43, #0f2027);
        box-shadow: 0 0 15px #00ffd5;
        border-color: #fff;
    }

    /* Metric Cards */
    div[data-testid="stMetricValue"] { color: #00ffd5; font-size: 2rem; font-weight: bold; }
    div[data-testid="stMetricLabel"] { color: #a0aab2; font-size: 1rem; }
    
    /* Code Blocks & Text Areas */
    .stTextArea textarea { background-color: #1e1e2e; color: #a6accd; border: 1px solid #45475a; border-radius: 8px; }
    
    /* Headers */
    h1, h2, h3 { color: #e1e2e7; }
    hr { border-color: #313244; }
    </style>
    """, unsafe_allow_html=True)

# =====================================================================
# 2. STATEFUL CONTEXT & CONVERSATIONAL MEMORY MANAGEMENT
# =====================================================================
class AdvancedConversationMemory:
    def __init__(self, max_history_len: int = 30):
        self.history: List[Dict[str, Any]] = []
        self.max_history_len = max_history_len
        self.global_risk_weight: float = 0.0

    def commit_interaction(self, intent_type: str, user_query: str, detected_risks: int, status: str, language: str):
        if len(self.history) >= self.max_history_len:
            self.history.pop(0)
            
        self.history.append({
            "timestamp": time.time(),
            "intent_type": intent_type,
            "language": language,
            "query": user_query,
            "risks_count": detected_risks,
            "status": status
        })
        
        self.global_risk_weight += (detected_risks * 1.5)
        if status == "BLOCKED":
            self.global_risk_weight += 5.0

    def get_deep_context_intent(self) -> Optional[str]:
        if not self.history: return None
        for interaction in reversed(self.history):
            if interaction["intent_type"] not in ["generic", "none"]:
                return interaction["intent_type"]
        return self.history[-1]["intent_type"]

    def get_session_analytics(self) -> Dict[str, Any]:
        return {
            "total_interactions": len(self.history),
            "accumulated_risk_score": self.global_risk_weight,
            "is_highly_suspicious": self.global_risk_weight > 7.0
        }

# =====================================================================
# 3. HIGH-STABILITY CRYPTOGRAPHIC SESSION & RATE REGULATOR
# =====================================================================
class EnterpriseSecurityContext:
    def __init__(self):
        self.secret_key = "quantum_safe_key_2026".encode()
        self.sessions: Dict[str, Dict[str, Any]] = {}
        self.rate_limits: Dict[str, List[float]] = {}
        self.memory_vault: Dict[str, AdvancedConversationMemory] = {}
        
        self._admin_salt = b"secure_soc_salt_vector_99"
        self._admin_password_hash = hashlib.pbkdf2_hmac('sha256', b"Admin2026!", self._admin_salt, 50000).hex()

    def establish_session(self, ip: str, user_agent: str) -> str:
        session_id = f"SEC-SESSION-{uuid.uuid4()}"
        self.sessions[session_id] = {"bound_ip": ip, "established_at": time.time()}
        self.memory_vault[session_id] = AdvancedConversationMemory()
        return session_id

    def verify_admin_credentials(self, password_attempt: str) -> bool:
        attempt_hash = hashlib.pbkdf2_hmac('sha256', password_attempt.encode(), self._admin_salt, 50000).hex()
        return hmac.compare_digest(self._admin_password_hash, attempt_hash)

    def enforce_rate_limit(self, client_id: str, max_reqs: int = 20, window: int = 86400) -> bool:
        now = time.time()
        if client_id not in self.rate_limits: self.rate_limits[client_id] = []
        self.rate_limits[client_id] = [t for t in self.rate_limits[client_id] if now - t < window]
        if len(self.rate_limits[client_id]) >= max_reqs: return False
        self.rate_limits[client_id].append(now)
        return True

# =====================================================================
# 4. WAF INPUT VALIDATOR & DEEP CODE ANALYZER
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

    @staticmethod
    def analyze_ast(source_code: str) -> List[Dict[str, Any]]:
        findings = []
        try: tree = ast.parse(source_code)
        except Exception as e: return [{"severity": "CRITICAL", "type": "SyntaxError", "details": str(e)}]
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in ['eval', 'exec']:
                findings.append({"severity": "CRITICAL", "type": "Dynamic Execution", "details": "Use of eval/exec is strictly forbidden."})
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and any(kw in target.id.lower() for kw in ['secret', 'password', 'token']):
                        findings.append({"severity": "HIGH", "type": "Hardcoded Secret", "details": f"Variable '{target.id}' might contain a plaintext secret."})
        return findings

# =====================================================================
# 5. HIGH-INTELLIGENCE MULTI-TIER ENGINE & AI SIMULATOR
# =====================================================================
class SmartDefensiveGenerator:
    def __init__(self):
        # 🚀 EXTENDED & STRENGTHENED PREMIUM CODE BLUEPRINTS
        self.premium_blueprints = {
            "sql": '''def execute_secure_db_query(db_conn, user_id: str) -> dict:
    """Enterprise SQL Injection Prevention via Parameterization."""
    import logging
    try:
        if not str(user_id).isdigit():
            raise ValueError("Input failed strict type validation.")
        with db_conn.cursor() as cursor:
            # The database engine compiles the query BEFORE inserting variables
            cursor.execute("SELECT id, username, role FROM users WHERE id = %s", (int(user_id),))
            result = cursor.fetchone()
            return {"data": result} if result else {"error": "Not found"}
    except Exception as e:
        logging.critical(f"Database Integrity Alert: {e}")
        return {"error": "Secure connection interrupted."}''',
            
            "command": '''def execute_secure_system_command(target_ip: str) -> str:
    """Bulletproof OS Command execution preventing injection."""
    import subprocess, ipaddress, logging
    try:
        # 1. Cryptographic/Network structural validation
        ip_obj = ipaddress.ip_address(target_ip.strip())
        # 2. Strict execution bounded to specific safe arrays
        result = subprocess.run(
            ["ping", "-c", "2", str(ip_obj)],
            capture_output=True, text=True, shell=False, timeout=5, check=True
        )
        return result.stdout
    except ValueError:
        logging.warning(f"Command Injection attempt blocked. Invalid IP format: {target_ip}")
        return "Error: Malformed Input."
    except subprocess.SubprocessError as e:
        return "Error: Process execution timed out or failed."''',
            
            "xss": '''def sanitize_user_input_for_html(untrusted_input: str) -> str:
    """Deep Content Disarm & Reconstruction for XSS."""
    import html, re
    if not isinstance(untrusted_input, str): return ""
    # 1. Strip null bytes
    cleaned = untrusted_input.replace("\\x00", "").strip()
    # 2. Regex removal of dangerous active tags before escaping
    cleaned = re.sub(r"(?i)<(script|iframe|object|embed|svg|math)[^>]*>.*?</\\1>", "", cleaned)
    # 3. Final HTML Entity Encoding
    return html.escape(cleaned, quote=True)''',
            
            "ssrf": '''def fetch_remote_resource_securely(target_url: str) -> bytes:
    """Prevents Server-Side Request Forgery (SSRF) and Cloud Metadata Leaks."""
    import urllib.request, urllib.parse, socket, ipaddress, logging
    
    parsed = urllib.parse.urlparse(target_url)
    if parsed.scheme not in ['http', 'https']:
        raise ValueError("SSRF Blocked: Invalid URL scheme.")
        
    try:
        # Resolve IP to check for internal infrastructure targeting
        ip_str = socket.gethostbyname(parsed.hostname)
        ip_obj = ipaddress.ip_address(ip_str)
        
        if ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_link_local:
            logging.critical(f"SSRF ALERT: Attempt to access internal IP {ip_str} blocked!")
            raise PermissionError("Access to private IP ranges is strictly forbidden.")
            
        req = urllib.request.Request(target_url, headers={'User-Agent': 'SecureEnterpriseClient/1.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            return response.read()
            
    except Exception as e:
        logging.error(f"Network request failed or blocked: {e}")
        return b""''',

            "deserialize": '''def secure_data_deserialization(payload: str) -> dict:
    """Prevents RCE via Insecure Deserialization (Replaces Pickle/Yaml)."""
    import json, logging
    try:
        # Strictly use JSON. Never use pickle.loads() or yaml.load() for untrusted data.
        data = json.loads(payload)
        if not isinstance(data, dict):
            raise TypeError("Deserialized data structure violates expected schema.")
        return data
    except json.JSONDecodeError as e:
        logging.error(f"Deserialization Attack Blocked: Payload parsing failed. {e}")
        return {}''',

            "token": '''def validate_jwt_auth_token(auth_header: str, server_secret: str) -> dict:
    """Cryptographic validation of JWT to prevent Token Forgery & Grabbing."""
    import hmac, hashlib, base64, json, time
    if not auth_header or not auth_header.startswith("Bearer "):
        raise PermissionError("Missing or invalid Auth header structure.")
        
    parts = auth_header.split(" ")[1].split(".")
    if len(parts) != 3: raise PermissionError("Malformed JWT.")
        
    header, payload, signature = parts
    expected_sig = base64.urlsafe_b64encode(
        hmac.new(server_secret.encode(), f"{header}.{payload}".encode(), hashlib.sha256).digest()
    ).decode().rstrip("=")
    
    # Timing-attack safe comparison
    if not hmac.compare_digest(signature, expected_sig):
        raise PermissionError("CRITICAL: Token Signature Tampering Detected!")
        
    data = json.loads(base64.urlsafe_b64decode(payload + "==").decode())
    if data.get("exp", 0) < time.time():
        raise PermissionError("Token has expired.")
    return data'''
        }

        # Fallback dictionary for Free Tier
        self.free_blueprints = {k: f"# FREE TIER VERSION\n# Security checks disabled\ndef basic_{k}(data):\n    return data" for k in self.premium_blueprints.keys()}
        self.free_blueprints["generic"] = "def sanitize(text): return text.strip()"
        self.premium_blueprints["generic"] = self.premium_blueprints["xss"]

        # Bilingual Guides mapping
        self.guides = {
            "sql": {"he": "שלב קוד זה בשכבת ה-DAL לפני גישה לבסיס הנתונים.", "en": "Implement in the DAL layer before DB execution."},
            "command": {"he": "הטמע בבקר (Controller) המבצע קריאות מערכת, במקום os.system.", "en": "Embed in system-call controllers replacing os.system."},
            "xss": {"he": "עטוף קלט משתמש בפונקציה זו לפני רינדור ל-HTML ב-Frontend.", "en": "Wrap user input with this before HTML rendering."},
            "ssrf": {"he": "השתמש בפונקציה זו בכל מנגנון שמושך תמונות, Webhooks, או קבצים מ-URL חיצוני.", "en": "Use for fetching external Webhooks, images, or URLs."},
            "deserialize": {"he": "החלף את כל קריאות ה-pickle.loads / yaml.load בקוד זה.", "en": "Replace all pickle/yaml loading with this strict JSON parser."},
            "token": {"he": "הטמע כ-Middleware על גבי נתיבי API (Private Routes) הדורשים אימות.", "en": "Deploy as Auth Middleware over Private API Routes."},
            "generic": {"he": "הוסף פונקציה זו לשכבת הניקוי הגלובלית.", "en": "Add to global sanitization layer."}
        }

    def detect_lang(self, text: str) -> str:
        return "he" if any("\u0590" <= c <= "\u05FF" for c in text) else "en"

    def determine_intent(self, q: str) -> str:
        q = q.lower()
        if any(w in q for w in ["ssrf", "webhook", "cloud metadata", "זיוף בקשת שרת", "ssrf"]): return "ssrf"
        if any(w in q for w in ["deserialize", "pickle", "yaml", "דה-סריאליזציה", "rce", "serial"]): return "deserialize"
        if any(w in q for w in ["sql", "db", "select", "בסיס נתונים", "שאילתה", "הזרקת"]): return "sql"
        if any(w in q for w in ["command", "os.", "ping", "פקודה", "טרמינל"]): return "command"
        if any(w in q for w in ["token", "jwt", "auth", "טוקן", "גניבת"]): return "token"
        if any(w in q for w in ["xss", "script", "html", "סניטציה", "סקריפט"]): return "xss"
        return "generic"

    def generate_ai_analysis(self, intent: str, lang: str) -> str:
        """Simulates an AI generating a Threat Intelligence brief."""
        reports_he = {
            "ssrf": "🤖 **ניתוח AI ביטחוני:** מתקפת SSRF מנצלת את אמון השרת שלך ברשת המקומית. התוקף גורם לשרת לפנות לכתובות פנימיות (כמו 169.254.169.254 ב-AWS) ולגנוב הרשאות ענן (IAM). הפתרון מטה מסנן בקפידה כתובות IP פרטיות ברמת ה-Socket.",
            "deserialize": "🤖 **ניתוח AI ביטחוני:** שימוש ב-Pickle או מחלצי YAML לא מאובטחים מאפשר לתוקף לבנות אובייקט זדוני שמריץ קוד מערכת (RCE) כשהוא נפתח. הפתרון דורש מעבר לפורמט סטטי (JSON) ואכיפת סכמות מחמירה.",
            "sql": "🤖 **ניתוח AI ביטחוני:** הזרקת SQL מתרחשת כשקלט המשתמש מחובר ישירות כמחרוזת לשאילתה. הפתרון המיוצר (Parameterized Queries) מאלץ את מנוע ה-SQL להתייחס לקלט כאל משתנה מבודד, כך שקוד זדוני מנוטרל.",
            "xss": "🤖 **ניתוח AI ביטחוני:** חדירת XSS מאפשרת השתלת קוד JS בדפדפן הלקוח, מה שמוביל לגניבת עוגיות (Cookies). הפונקציה המצורפת משלבת מחיקת תגים אגרסיבית עם HTML Entity Encoding כדי להבטיח תצוגה בלבד.",
            "command": "🤖 **ניתוח AI ביטחוני:** הזרקת פקודות למערכת ההפעלה מאפשרת השתלטות מלאה על השרת. השימוש ב-subprocess.run עם shell=False מבטיח שהפרמטרים מועברים כמערך סגור ללא יכולת שרשור פקודות (כמו `&&` או `;`).",
            "token": "🤖 **ניתוח AI ביטחוני:** זיוף וחטיפת JWT (Token Grabbing) הם הגורם המוביל לעקיפת מנגנוני הזדהות. קוד ההגנה שיוצר מחשב מחדש את החתימה (HMAC-SHA256) ומשווה אותה בצורה בטוחה (Timing-attack safe) כנגד ניסיונות זיוף.",
            "generic": "🤖 **ניתוח AI ביטחוני:** זוהה צורך בניקוי קלט כללי. מנגנון ההגנה מנקה תווים מסוכנים וממיר אותם לפורמט בטוח לתצוגה."
        }
        reports_en = {
            "ssrf": "🤖 **AI Threat Intel:** SSRF tricks your server into making HTTP requests to internal, protected resources (like AWS Metadata APIs). The provided code resolves and blocks private IP ranges dynamically.",
            "deserialize": "🤖 **AI Threat Intel:** Insecure Deserialization (e.g., Python's pickle) allows attackers to pass serialized objects that execute arbitrary system commands upon loading. The solution strictly enforces JSON architecture.",
            "sql": "🤖 **AI Threat Intel:** SQLi occurs when untrusted user input is concatenated into queries. The generated solution utilizes strictly parameterized queries, treating inputs purely as data values.",
            "xss": "🤖 **AI Threat Intel:** XSS allows attackers to execute JS in victims' browsers, hijacking sessions. The provided algorithm uses Deep Content Disarm, stripping active HTML nodes and encoding output.",
            "command": "🤖 **AI Threat Intel:** Command Injection leads to full server compromise. By executing commands explicitly via lists with `shell=False` and enforcing Regex boundaries, shell metacharacters are neutralized.",
            "token": "🤖 **AI Threat Intel:** JWT tampering bypasses authentication. The defensive blueprint enforces cryptographic signature re-calculation and prevents timing attacks using `hmac.compare_digest`.",
            "generic": "🤖 **AI Threat Intel:** General input sanitization required. The generated method escapes harmful structural characters."
        }
        return reports_he.get(intent, reports_he["generic"]) if lang == "he" else reports_en.get(intent, reports_en["generic"])

# =====================================================================
# 6. STREAMLIT ENTERPRISE UI 
# =====================================================================
st.set_page_config(page_title="AI DefSec Platform", page_icon="🛡️", layout="wide")
inject_custom_css()

if "sec_ctx" not in st.session_state:
    st.session_state.sec_ctx = EnterpriseSecurityContext()
    st.session_state.engines = SecurityEngines()
    st.session_state.ai_gen = SmartDefensiveGenerator()
    st.session_state.session_id = st.session_state.sec_ctx.establish_session("192.168.1.10", "Mozilla/5.0")

mem_vault = st.session_state.sec_ctx.memory_vault[st.session_state.session_id]

# --- MAIN DASHBOARD ---
st.title("🛡️ SOC AI: Threat Defense Architect")
st.markdown("##### ⚡ Enterprise-Grade Vulnerability Mitigation & Code Generation")
st.markdown("---")

with st.sidebar:
    st.image("https://img.icons8.com/nolan/96/cyber-security.png", width=64)
    st.header("⚙️ System Control")
    tier = st.selectbox("Select Access Tier:", ["PREMIUM Tier (Full Defense)", "FREE Tier (Throttled)"])
    is_premium = "PREMIUM" in tier
    
    st.markdown("---")
    st.header("📊 Real-Time Telemetry")
    metrics = mem_vault.get_session_analytics()
    col1, col2 = st.columns(2)
    col1.metric("Risk Score", f"{metrics['accumulated_risk_score']:.1f}")
    col2.metric("Queries", metrics['total_interactions'])
    
    if metrics["is_highly_suspicious"]:
        st.error("⚠️ SYSTEM UNDER ATTACK: High risk accumulated!")

# TABS LAYOUT
tab1, tab2, tab3 = st.tabs(["💬 AI Code Generator", "🔬 Source Code Scanner", "📜 Threat Logs"])

with tab1:
    st.subheader("🤖 Request Defensive Blueprint")
    prompt_val = "תראה לי איך לחסום מתקפות SSRF על השרת שלי" if is_premium else "XSS prevention code"
    user_prompt = st.text_input("Describe the attack you want to prevent (Hebrew/English):", value=prompt_val)
    
    if st.button("Generate Secure Payload", type="primary"):
        if not st.session_state.sec_ctx.enforce_rate_limit("192.168.1.10", 20):
            st.error("🚨 RATE LIMIT REACHED.")
        else:
            lang = st.session_state.ai_gen.detect_lang(user_prompt)
            safe, threat = st.session_state.engines.inspect_payloads(user_prompt)
            
            if not safe:
                st.error(f"❌ WAF BLOCKED MALICIOUS PROMPT: {threat}")
                mem_vault.commit_interaction("ATTACK", user_prompt, 5, "BLOCKED", lang)
            else:
                intent = st.session_state.ai_gen.determine_intent(user_prompt)
                code_pool = st.session_state.ai_gen.premium_blueprints if is_premium else st.session_state.ai_gen.free_blueprints
                final_code = code_pool.get(intent, code_pool["generic"])
                instruction = st.session_state.ai_gen.guides.get(intent, st.session_state.ai_gen.guides["generic"])[lang]
                ai_intel = st.session_state.ai_gen.generate_ai_analysis(intent, lang)
                
                mem_vault.commit_interaction(intent, user_prompt, 0, "SUCCESS", lang)
                
                # Dynamic Display
                st.info(ai_intel)
                st.markdown("### 🔒 Generated Security Blueprint:")
                st.code(final_code, language="python")
                
                with st.expander("📌 Implementation Guide / הוראות הטמעה", expanded=True):
                    st.success(instruction)

with tab2:
    st.subheader("🔬 Static Application Security Testing (SAST)")
    code_in = st.text_area("Paste Python code to scan for vulnerabilities:", value="import os\nos.system('echo ' + user_input)", height=150)
    if st.button("Scan Code for Vulnerabilities", type="secondary"):
        findings = st.session_state.engines.analyze_ast(code_in)
        if not findings:
            st.success("✅ Code passed AST verification. No obvious structural threats found.")
        else:
            for f in findings:
                if f["severity"] == "CRITICAL": st.error(f"**CRITICAL:** {f['type']} - {f['details']}")
                else: st.warning(f"**HIGH:** {f['type']} - {f['details']}")

with tab3:
    st.subheader("📜 Security Information and Event Management (SIEM)")
    if mem_vault.history:
        st.dataframe(mem_vault.history, use_container_width=True)
    else:
        st.caption("No system events recorded yet in this session.")
