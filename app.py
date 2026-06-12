import ast
import hashlib
import hmac
import time
import uuid
import logging
import re
import html
from typing import Dict, Any, List, Tuple, Optional, Set
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
# 2. STATEFUL CONTEXT & CONVERSATIONAL MEMORY MANAGEMENT
# =====================================================================
class AdvancedConversationMemory:
    def __init__(self, max_history_len: int = 30): # Expanded memory
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
        
        # Smart risk decay/accumulation
        self.global_risk_weight += (detected_risks * 1.5)
        if status == "BLOCKED":
            self.global_risk_weight += 5.0

    def get_deep_context_intent(self) -> Optional[str]:
        if not self.history:
            return None
        # Look for the most severe/recent intents
        for interaction in reversed(self.history):
            intent = interaction["intent_type"]
            if intent in ["sql", "command", "file", "crypto", "xss", "brute", "csrf", "token"]:
                return intent
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
    def __init__(self, secret_key: str = "dynamic_quantum_safe_secret_key_2026"):
        self.secret_key = secret_key.encode()
        self.sessions: Dict[str, Dict[str, Any]] = {}
        self.rate_limits: Dict[str, List[float]] = {}
        self.memory_vault: Dict[str, AdvancedConversationMemory] = {}
        
        self._admin_salt = b"secure_soc_salt_vector_99"
        self._admin_password_hash = hashlib.pbkdf2_hmac('sha256', b"AdminMaster2026!", self._admin_salt, 50000).hex()

    def generate_secure_fingerprint(self, ip: str, user_agent: str) -> str:
        raw_data = f"{ip}|{user_agent}".encode()
        return hmac.new(self.secret_key, raw_data, hashlib.sha256).hexdigest()

    def establish_session(self, ip: str, user_agent: str) -> str:
        session_id = f"SEC-SESSION-{uuid.uuid4()}"
        fp = self.generate_secure_fingerprint(ip, user_agent)
        
        self.sessions[session_id] = {
            "fingerprint": fp,
            "bound_ip": ip,
            "established_at": time.time(),
            "last_seen": time.time()
        }
        self.memory_vault[session_id] = AdvancedConversationMemory()
        return session_id

    def verify_admin_credentials(self, password_attempt: str) -> bool:
        attempt_hash = hashlib.pbkdf2_hmac('sha256', password_attempt.encode(), self._admin_salt, 50000).hex()
        return hmac.compare_digest(self._admin_password_hash, attempt_hash)

    def enforce_sliding_window_rate_limit(self, client_id: str, max_reqs: int = 15, window: int = 86400) -> bool:
        now = time.time()
        if client_id not in self.rate_limits:
            self.rate_limits[client_id] = []
        self.rate_limits[client_id] = [t for t in self.rate_limits[client_id] if now - t < window]
        if len(self.rate_limits[client_id]) >= max_reqs:
            return False
        self.rate_limits[client_id].append(now)
        return True

    def get_memory(self, session_id: str) -> AdvancedConversationMemory:
        return self.memory_vault[session_id]


# =====================================================================
# 4. STRICT MULTI-TIER INPUT VALIDATOR (WAF SIMULATION)
# =====================================================================
class MultiTierInputValidator:
    @staticmethod
    def sanitize_string(text: str, max_chars: int = 5000) -> str:
        if not text or not text.strip():
            raise ValueError("Input data stream is empty or null.")
        if len(text) > max_chars:
            raise ValueError("Input character cap exceeded.")
        return text.replace("\x00", "").replace("\r", "")

    @staticmethod
    def inspect_malicious_payloads(text: str) -> Tuple[bool, str]:
        inspection_rules = {
            r"(?i)UNION\s+ALL\s+SELECT": "SQLi Injection Vector",
            r"(?i)<iframe[^>]*>.*<\/iframe>": "XSS Payload Threat",
            r"(?i)javascript\s*:\s*alert": "DOM XSS Injection",
            r"(?i)document\.cookie": "Session Hijacking Vector",
            r"(__import__\s*\(|os\.system|subprocess\.|getattr\s*\()": "RCE Server Payload",
            r"(?i)(\.\.\/|\.\.\\)": "Path Traversal Vector" # Added Deep Inspection Rule
        }
        for pattern, risk_name in inspection_rules.items():
            if re.search(pattern, text):
                return False, risk_name
        return True, "CLEAN"


# =====================================================================
# 5. AST STRUCTURAL DEEP CODE ANALYZER (STATIC ANALYSIS)
# =====================================================================
class ASTDeepAnalyzer:
    def analyze(self, source_code: str) -> List[Dict[str, Any]]:
        findings = []
        if not source_code or not source_code.strip():
            return findings
        try:
            tree = ast.parse(source_code)
        except Exception as e:
            return [{"type": "SyntaxError", "severity": "CRITICAL", "details": f"Compile check failed: {str(e)}", "line": 1}]

        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                if node.func.id in ['eval', 'exec']:
                    findings.append({"type": "DynamicExecutionVulnerability", "severity": "HIGH", "details": f"Dangerous primitive '{node.func.id}' detected.", "line": getattr(node, 'lineno', 1)})

            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                if node.func.attr in ['Popen', 'run', 'system', 'call'] or (isinstance(node.func.value, ast.Name) and node.func.value.id == 'os' and node.func.attr in ['system', 'popen']):
                    # Check for shell=True vulnerability
                    has_shell_true = any(isinstance(kw.value, ast.Constant) and kw.value.value is True for kw in node.keywords if kw.arg == 'shell')
                    if has_shell_true:
                         findings.append({"type": "ShellCommandInjection", "severity": "CRITICAL", "details": f"Subprocess invocation via '{node.func.attr}' with shell=True is highly vulnerable.", "line": getattr(node, 'lineno', 1)})
                    else:
                         findings.append({"type": "SubprocessCallWarning", "severity": "MEDIUM", "details": f"Subprocess invocation via '{node.func.attr}'. Ensure inputs are parameterized.", "line": getattr(node, 'lineno', 1)})

            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        variable_name = target.id.lower()
                        if any(kw in variable_name for kw in {'secret', 'password', 'token', 'apikey'}):
                            findings.append({"type": "HardcodedCryptographicSecret", "severity": "HIGH", "details": f"Identifier '{target.id}' stores a plaintext secret.", "line": getattr(node, 'lineno', 1)})
        return findings


# =====================================================================
# 6. STRIDE COMPLIANT DYNAMIC THREAT MODELING ENGINE
# =====================================================================
class DynamicThreatModeler:
    @staticmethod
    def build_matrix(vulnerabilities: List[Dict[str, Any]], conversation_risk_weight: float) -> Dict[str, Any]:
        base_score = 100.0 - min(30.0, conversation_risk_weight)
        attack_vectors = []
        mitigations = []
        
        for v in vulnerabilities:
            if v["type"] == "SyntaxError":
                base_score -= 10
                continue
            base_score -= 25 if v["severity"] == "CRITICAL" else 15 if v["severity"] == "HIGH" else 5
            
            if v["type"] == "ShellCommandInjection":
                attack_vectors.append("STRIDE: Tampering / Elevation of Privilege")
                mitigations.append("Pass parameters as structurally bounded Lists. Enforce shell=False.")
            elif v["type"] == "DynamicExecutionVulnerability":
                attack_vectors.append("STRIDE: Malicious Arbitrary Code Execution")
                mitigations.append("Avoid eval/exec. Use safe parsing filters.")
            elif v["type"] == "HardcodedCryptographicSecret":
                attack_vectors.append("STRIDE: Information Disclosure")
                mitigations.append("Extract secrets out of source code into environment variables.")

        return {
            "resilience_index": max(0.0, min(100.0, base_score)),
            "threat_vectors": list(set(attack_vectors)),
            "remediation_steps": list(set(mitigations))
        }


# =====================================================================
# 7. HIGH-INTELLIGENCE MULTI-TIER ENGINE (SUPER PREMIUM ENGINE)
# =====================================================================
class SmartDefensiveGenerator:
    def __init__(self):
        # UPGRADED: Stronger Code Blueprints + Added Token Grabbing Defense
        self.premium_blueprints = {
            "sql": '''def execute_secure_database_query(db_connection, client_supplied_id: int) -> dict:
    import logging
    try:
        sanitized_id = int(client_supplied_id)
        with db_connection.cursor() as cursor:
            # Parameterized Query prevents SQLi
            query = "SELECT account_id, balance, owner_name, tier_level FROM accounts WHERE account_id = ?"
            cursor.execute(query, (sanitized_id,))
            row = cursor.fetchone()
            if row: 
                return {"account_id": row[0], "balance": row[1], "owner": row[2], "tier": row[3]}
            return {"status": "Record target identifier not found."}
    except (ValueError, TypeError) as type_err:
        logging.error(f"Security Alert: Data type boundary exception intercepted: {str(type_err)}")
        return {"status": "Error: Invalid parameter syntax provided."}
    except Exception as e:
        logging.critical(f"DB Error: {str(e)}")
        return {"status": "Error: Internal server processing error."}''',
            
            "command": '''def execute_secure_network_diagnostic(target_destination: str) -> str:
    import subprocess, re
    # Strict Regex allowing ONLY valid domain/IP characters
    if not re.match(r"^[a-zA-Z0-9.-]+$", target_destination.strip()):
        raise PermissionError("Security Exception: Malicious command characters detected.")
    try:
        # shell=False and list parameters prevent Command Injection
        result = subprocess.run(
            ["ping", "-c", "2", target_destination.strip()], 
            capture_output=True, text=True, shell=False, timeout=5, check=True
        )
        return result.stdout
    except Exception as e:
        return f"Execution Error: Context unavailable: {str(e)}"''',
            
            "file": '''def secure_file_retrieval(user_requested_path: str, storage_root: str = "/app/user_space") -> str:
    import os
    base_directory = os.path.abspath(storage_root)
    # Compute the absolute path to prevent Directory Traversal
    computed_target_path = os.path.abspath(os.path.join(base_directory, user_requested_path))
    
    if not computed_target_path.startswith(base_directory):
        raise PermissionError("Access Violation Alert: Directory traversal attempt blocked.")
    if not os.path.isfile(computed_target_path):
        raise FileNotFoundError("Requested asset node cannot be located.")
        
    with open(computed_target_path, 'r', encoding='utf-8', errors='ignore') as active_file:
        return active_file.read()''',
            
            "crypto": '''def hash_password_pbkdf2(password_string: str) -> str:
    import hashlib, secrets
    # Use cryptographic secrets module for salt generation
    salt_vector = secrets.token_bytes(32)
    derived_key = hashlib.pbkdf2_hmac(
        hash_name='sha3_256', # Upgraded to SHA-3
        password=password_string.encode('utf-8'),
        salt=salt_vector,
        iterations=210000 # Increased iterations for brute-force resistance
    )
    return f"pbkdf2_sha3_256$210000${salt_vector.hex()}${derived_key.hex()}"''',

            "xss": '''def sanitize_html_output(untrusted_user_input: str) -> str:
    import html, re
    if not untrusted_user_input or not untrusted_user_input.strip():
        return ""
    # Strip null bytes and known malicious tags before escaping
    scrubbed_payload = untrusted_user_input.replace("\\x00", "").strip()
    scrubbed_payload = re.sub(r"(?i)<(script|iframe|object|embed|form)[^>]*>.*?</\\1>", "", scrubbed_payload)
    return html.escape(scrubbed_payload, quote=True)''',

            "brute": '''def verify_login_with_rate_limiting(client_ip: str, redis_cache_connection) -> bool:
    import time
    current_epoch_time = int(time.time())
    tracking_window_key = f"waf:rate_limit:{client_ip}"
    
    # Implementing a secure Token Bucket / Sliding Window via Cache
    attempts = redis_cache_connection.incr(tracking_window_key)
    if attempts == 1:
        redis_cache_connection.expire(tracking_window_key, 300) # 5 minutes lockout window
        
    if attempts > 5:
        raise PermissionError("Access Temporarily Locked: Brute force vector detected.")
    return True''',

            "csrf": '''def generate_and_verify_csrf_token(session_context: dict, client_token: str = None) -> str:
    import secrets, hmac
    if client_token is None:
        cryptographic_token = secrets.token_urlsafe(64)
        session_context["secure_csrf_secret_key"] = cryptographic_token
        return cryptographic_token
        
    server_cached_token = session_context.get("secure_csrf_secret_key", "")
    # Use compare_digest to prevent Timing Attacks
    if not server_cached_token or not hmac.compare_digest(server_cached_token, client_token):
        raise PermissionError("CSRF Attack Vector Triggered: Validation has failed.")
    return "HANDSHAKE_VERIFIED"''',

            # ADDED: Defense against Token Grabbing / Session Hijacking
            "token": '''def validate_secure_jwt_token(auth_header: str, server_secret: str) -> dict:
    import hmac, hashlib, base64, json, time
    if not auth_header.startswith("Bearer "):
        raise ValueError("Invalid Token Structure.")
        
    token_parts = auth_header.split(" ")[1].split(".")
    if len(token_parts) != 3:
        raise ValueError("Malformed Token Data.")
        
    header, payload, signature = token_parts
    expected_signature = base64.urlsafe_b64encode(
        hmac.new(server_secret.encode(), f"{header}.{payload}".encode(), hashlib.sha256).digest()
    ).decode().rstrip("=")
    
    if not hmac.compare_digest(signature, expected_signature):
        raise PermissionError("Token Tampering Detected! Token Grabbing Protection Triggered.")
        
    decoded_payload = json.loads(base64.urlsafe_b64decode(payload + "==").decode())
    if decoded_payload.get("exp", 0) < time.time():
        raise PermissionError("Token has expired.")
        
    return decoded_payload'''
        }
        
        self.free_blueprints = {
            "sql": '''# FREE VERSION:\ndef quick_sql(user_id):\n    return f"SELECT * FROM users WHERE id = {int(user_id)}"''',
            "command": '''# FREE VERSION:\ndef basic_ping(ip):\n    import os\n    os.system("ping -c 1 " + ip)''',
            "file": '''# FREE VERSION:\ndef simple_read(path):\n    return open(path.replace("../", "")).read()''',
            "crypto": '''# FREE VERSION:\ndef weak_md5_hash(password):\n    import hashlib\n    return hashlib.md5(password.encode()).hexdigest()''',
            "xss": '''# FREE VERSION:\ndef raw_replace(text):\n    return text.replace("<script>", "")''',
            "brute": '''# FREE VERSION:\ndef basic_count(user):\n    return True''',
            "csrf": '''# FREE VERSION:\ndef bypass_csrf():\n    return "CSRF disabled in FREE tier"''',
            "token": '''# FREE VERSION:\ndef check_token(t):\n    return True if t else False'''
        }

        # BILINGUAL IMPLEMENTATION GUIDES
        self.implementation_guides = {
            "sql": {
                "he": "יש לשלב את הפונקציה הזו בשכבת הגישה לנתונים (Data Access Layer - DAL) באפליקציה שלך, לפני ביצוע השאילתות במסד הנתונים.",
                "en": "Implement this function in your Data Access Layer (DAL) before executing queries against the database."
            },
            "command": {
                "he": "הטמע את הפונקציה הזו בשכבת הבקר (Controller) שמטפלת בפקודות מערכת, והחלף באמצעותה קריאות ישירות ל-os.system.",
                "en": "Embed this in the Controller layer handling system commands, replacing any direct calls to os.system."
            },
            "file": {
                "he": "שים את הקוד הזה במודול ניהול הקבצים של השרת, למשל בראוט (Route) האחראי על הורדת או הצגת קבצים למשתמשים.",
                "en": "Place this code in your server's file management module, typically in the Route responsible for downloading or serving files."
            },
            "crypto": {
                "he": "יש למקם את הקוד הזה במנגנון ההרשמה (Registration) והאימות (Authentication), ממש לפני שמירת משתמש חדש במסד הנתונים.",
                "en": "Locate this code in your Registration and Authentication flow, right before saving a new user to the database."
            },
            "xss": {
                "he": "יש לקרוא לפונקציה הזו בשכבת התצוגה (View / Frontend render), ממש לפני שאתה מציג טקסט של משתמש אל תוך קוד ה-HTML של האתר.",
                "en": "Call this function in your View/Frontend rendering layer, right before injecting user-supplied text into the DOM/HTML."
            },
            "brute": {
                "he": "הטמע קוד זה כ-Middleware או בשלב הראשון של פונקציית ה-Login שלך, לפני שאתה בודק סיסמאות מול המסד.",
                "en": "Implement this code as Middleware or at the very beginning of your Login function, prior to checking passwords."
            },
            "csrf": {
                "he": "יש לשלב את ייצור הטוקן בעת יצירת ה-Session, ואת האימות להריץ ב-Middleware שיושב על כל בקשות ה-POST/PUT/DELETE.",
                "en": "Integrate token generation during Session creation, and run the validation in a Middleware applied to all POST/PUT/DELETE requests."
            },
            "token": {
                "he": "הדבק את הקוד ב-API Gateway או ב-Middleware שמגן על נתיבים פרטיים (Private Routes) כדי למנוע כניסה עם טוקן גנוב.",
                "en": "Paste this code in your API Gateway or Auth Middleware protecting Private Routes to prevent access via stolen/grabbed tokens."
            },
            "generic": {
                "he": "יש לשלב פונקציה זו כחלק ממנגנון ניקוי הקלט הגלובלי (Sanitization Middleware) של האפליקציה שלך.",
                "en": "Integrate this function as part of your application's global Input Sanitization Middleware."
            }
        }

    # SMART LANGUAGE DETECTOR
    def detect_language(self, text: str) -> str:
        # If text contains Hebrew characters (Unicode range \u0590-\u05FF), treat as Hebrew
        if any("\u0590" <= c <= "\u05FF" for c in text):
            return "he"
        return "en"

    def determine_intent(self, user_query: str, last_intent: Optional[str], plan_tier: str) -> str:
        query_clean = user_query.lower().strip()
        if plan_tier == "FREE":
            if "xss" in query_clean: return "xss"
            if "brute" in query_clean or "limit" in query_clean: return "brute"
            if "csrf" in query_clean: return "csrf"
            if "sql" in query_clean or "db" in query_clean: return "sql"
            if "command" in query_clean or "ping" in query_clean: return "command"
            if "file" in query_clean or "path" in query_clean: return "file"
            if "crypto" in query_clean or "hash" in query_clean or "password" in query_clean: return "crypto"
            if "token" in query_clean or "jwt" in query_clean: return "token"
            return "generic"
        else:
            xss_keywords = ["xss", "cross-site scripting", "script injection", "html escape", "sanitize input", "גניבת עוגיות", "הזרקת סקריפט", "עוגיות", "סניטציה"]
            if any(w in query_clean for w in xss_keywords): return "xss"
            
            brute_keywords = ["brute force", "rate limit", "ddos", "login block", "attempts", "הצפה", "חסימת משתמש", "ניחוש סיסמה", "מגבלת בקשות", "ברוט פורס"]
            if any(w in query_clean for w in brute_keywords): return "brute"
            
            csrf_keywords = ["csrf", "cross-site request forgery", "xsrf", "form token", "זיוף בקשה", "טוקן טופס", "טפסים מאובטחים"]
            if any(w in query_clean for w in csrf_keywords): return "csrf"
            
            sql_keywords = ["sql", "db", "database", "query", "select", "בסיס נתונים", "שאילתה", "מסד", "נתונים"]
            if any(w in query_clean for w in sql_keywords): return "sql"
            
            command_keywords = ["command", "os", "subprocess", "ping", "terminal", "run", "טרמינל", "פקודה", "פינג", "להריץ"]
            if any(w in query_clean for w in command_keywords): return "command"
            
            file_keywords = ["file", "path", "read", "open", "directory", "קובץ", "לקרוא קובץ", "נתיב", "תיקייה"]
            if any(w in query_clean for w in file_keywords): return "file"
            
            crypto_keywords = ["crypto", "hash", "password", "encrypt", "sha", "md5", "salt", "הצפנה", "סיסמה", "האש", "להצפין"]
            if any(w in query_clean for w in crypto_keywords): return "crypto"
            
            token_keywords = ["token", "jwt", "grabber", "session hijack", "auth header", "טוקן", "חטיפת טוקן", "גניבת זהות"]
            if any(w in query_clean for w in token_keywords): return "token"
            
            return last_intent if last_intent else "generic"

    def synthesize_secure_code(self, determined_intent: str, plan_tier: str, language: str) -> Tuple[str, str]:
        active_blueprint_pool = self.premium_blueprints if plan_tier == "PREMIUM" else self.free_blueprints
        
        generated_code = active_blueprint_pool.get(determined_intent, '''def core_input_sanitizer(raw_data: str) -> str:\n    import html\n    return html.escape(raw_data.strip())[:1000]''')
        
        # Pull correct language string
        instruction_dict = self.implementation_guides.get(determined_intent, self.implementation_guides["generic"])
        instruction_text = instruction_dict.get(language, instruction_dict["en"])
        
        return generated_code, instruction_text


# =====================================================================
# 8. STREAMLIT ENTERPRISE UI & GRAPHICAL SOC ORCHESTRATOR
# =====================================================================
st.set_page_config(page_title="Defensive AI Web Platform", page_icon="🛡️", layout="wide")

if "security_context" not in st.session_state:
    st.session_state.security_context = EnterpriseSecurityContext()
    st.session_state.code_analyzer = ASTDeepAnalyzer()
    st.session_state.generator = SmartDefensiveGenerator()
    st.session_state.session_id = None
    st.session_state.client_ip = "192.168.1.104"
    st.session_state.client_ua = "Mozilla/5.0 EnterpriseSecureAI/4.0"
    st.session_state.is_admin = False  
    st.session_state.rate_limiting_enabled = True  

if not st.session_state.session_id:
    st.session_state.session_id = st.session_state.security_context.establish_session(
        st.session_state.client_ip, st.session_state.client_ua
    )

memory_vault = st.session_state.security_context.get_memory(st.session_state.session_id)

url_parameters = st.query_params
is_url_admin_mode = url_parameters.get("page") == "admin"

# --- ADMIN ROUTING INTERFACE ---
if is_url_admin_mode:
    st.title("🔑 Secret Admin Gate — Identity Verification")
    st.markdown("---")
    if not st.session_state.is_admin:
        col_auth, _ = st.columns([1, 2])
        with col_auth:
            admin_input = st.text_input("Enter Admin Cryptographic Passcode:", type="password")
            if st.button("Verify Identity and Open Console", type="primary"):
                if st.session_state.security_context.verify_admin_credentials(admin_input):
                    st.session_state.is_admin = True
                    st.success("Access Granted! Master Session Initialized.")
                    st.rerun()
                else: st.error("Authentication Failure: Invalid Secret Signatures.")
            if st.button("← Return to Public Main Site"):
                st.query_params.clear() 
                st.rerun()
    else:
        st.header("👑 WELCOME BACK MASTER ADMIN")
        if st.button("🚪 Logout & Return to Main Site", type="secondary"):
            st.session_state.is_admin = False
            st.query_params.clear()
            st.rerun()
        st.markdown("---")
        st.subheader("🖥️ Dynamic System Overrides & Master Telemetry")
        adm_col1, adm_col2, adm_col3 = st.columns(3)
        with adm_col1:
            st.markdown("**Infrastructure Overrides**")
            st.session_state.rate_limiting_enabled = st.checkbox("Enable Global Rate Limiter", value=st.session_state.rate_limiting_enabled)
        with adm_col2:
            st.markdown("**Risk Score Management**")
            if st.button("Force Clear User Risk Weight", type="primary"):
                memory_vault.global_risk_weight = 0.0
                st.success("Global user risk index reset to zero.")
                st.rerun()
        with adm_col3:
            st.markdown("**Encrypted Memory Buffers**")
            st.json({
                "Active_Vault_Sessions": len(st.session_state.security_context.memory_vault),
                "Rate_Limit_Trackers": len(st.session_state.security_context.rate_limits),
                "Client_IP_Signature": st.session_state.client_ip
            })
        st.markdown("---")
        st.subheader("📋 SIEM Global Master Logs Feed")
        historical_log_nodes = memory_vault.history
        if historical_log_nodes: st.dataframe(historical_log_nodes, use_container_width=True)
        else: st.caption("No transaction nodes captured inside current session pipeline.")

# --- STANDARD PUBLIC WORKSPACE INTERFACE ---
else:
    st.title("🛡️ Enterprise Defensive AI Hub & SOC Radar Dashboard")
    st.caption("Production Grade Monolith Implementation — Public User Workspace")
    st.markdown("---")

    with st.sidebar:
        st.header("💎 Subscription Plan")
        selected_plan = st.radio(
            "Select Account Tier Level:",
            ["FREE Tier (Throttled Model)", "PREMIUM Tier ($10/Mo - Full Access)"],
            index=0
        )
        current_tier = "FREE" if "FREE" in selected_plan else "PREMIUM"
        
        st.markdown("---")
        st.header("📊 Threat State Monitor")
        analytics = memory_vault.get_session_analytics()
        risk_score = analytics["accumulated_risk_score"]
        if risk_score > 7.0: st.error(f"🔴 STATE: CRITICAL RISK ({risk_score:.2f})")
        elif risk_score > 0.0: st.warning(f"🟡 STATE: ELEVATED RISK ({risk_score:.2f})")
        else: st.success(f"🟢 STATE: NOMINAL SECURE")

    col_workspace, col_siem_dashboard = st.columns([1, 1])

    with col_workspace:
        if current_tier == "PREMIUM":
            st.success("""
            ### 🌟 PREMIUM MODEL FEATURES UNLOCKED
            * 🧠 **Deep Memory Vault** (Context loops & Language tracking)
            * 🛡️ **Bilingual AI Processing** (Native Hebrew & English Auto-Detect)
            * 📦 **Production Blueprints** (Advanced Token Grabbing, JWT validation, SQLi defenses)
            """)
        else:
            st.info("ℹ️ Running on FREE Tier. Multi-turn context history, bilingual auto-detect, and high-tier code generation are currently disabled.")

        st.header("🧠 Conversational Prompt Processing")
        default_prompt = "Give me code to prevent XSS attacks." if current_tier == "FREE" else "תראה לי קוד מאובטח שמנטרל תקיפות XSS"
        user_prompt = st.text_input("Enter your request (Hebrew/English):", value=default_prompt)
        
        st.header("🔬 Code Asset Vulnerability Simulator")
        default_flawed_script = 'def unsafe_utility(payload):\n    import os\n    db_pass = "Secret123"\n    os.system("ping -c 1 " + payload)'
        code_input_area = st.text_area("Source Code Input Workspace (Python Only):", value=default_flawed_script, height=180)
        
        execute_pipeline_trigger = st.button("Execute Secure Pipeline Optimization", type="primary")

    with col_siem_dashboard:
        st.header("🖥️ Central SOC Telemetry Radar")
        
        if execute_pipeline_trigger:
            rate_limit_passed = True
            if st.session_state.rate_limiting_enabled:
                rate_limit_passed = st.session_state.security_context.enforce_sliding_window_rate_limit(
                    st.session_state.client_ip, max_reqs=15, window=86400
                )
                
            if not rate_limit_passed:
                st.error("🚨 CRITICAL RATE LIMIT BREACH: [Daily limit of 15 requests reached for this IP address]. Please wait or reset context to restore operational bandwidth.")
            else:
                try:
                    # Pipeline Execution
                    sanitized_prompt = MultiTierInputValidator.sanitize_string(user_prompt)
                    is_input_safe, attack_vector = MultiTierInputValidator.inspect_malicious_payloads(sanitized_prompt)
                    
                    # Detect Language dynamically
                    detected_lang = st.session_state.generator.detect_language(sanitized_prompt)
                    lang_label = "עברית" if detected_lang == "he" else "English"
                    
                    if not is_input_safe:
                        st.error(f"❌ MALICIOUS PAYLOAD INTERCEPTED BY WAF: [{attack_vector}]")
                        memory_vault.commit_interaction("ATTACK", user_prompt, 5, "BLOCKED", detected_lang)
                    else:
                        findings_report = st.session_state.code_analyzer.analyze(code_input_area)
                        threat_matrix_profile = DynamicThreatModeler.build_matrix(findings_report, memory_vault.global_risk_weight)
                        
                        historical_intent_node = memory_vault.get_deep_context_intent() if current_tier == "PREMIUM" else None
                        derived_intent = st.session_state.generator.determine_intent(sanitized_prompt, historical_intent_node, current_tier)
                        
                        # Get Code & Bilingual Instructions
                        secured_output_blueprint, implementation_instructions = st.session_state.generator.synthesize_secure_code(derived_intent, current_tier, detected_lang)
                        
                        memory_vault.commit_interaction(derived_intent, sanitized_prompt, len(findings_report), "SUCCESS", detected_lang)
                        
                        st.subheader("📈 STRIDE Resilience Calculation Score")
                        resilience_metric = threat_matrix_profile["resilience_index"]
                        if resilience_metric >= 85.0: st.success(f"Security Health Index Score: {resilience_metric:.1f} / 100.0")
                        else: st.error(f"Security Health Index Score: {resilience_metric:.1f} / 100.0 (Risks Found)")
                            
                        if findings_report:
                            st.markdown("### ⚠️ Active Vulnerabilities Detected")
                            for element in findings_report:
                                st.markdown(f"**[{element['severity']}]** {element['type']}")
                                st.caption(element["details"])
                        else: st.success("✅ No structural vulnerabilities found in code fragment.")
                            
                        st.markdown(f"### 🛡️ קוד הגנתי מאובטח (Tier: {current_tier} | Language Detected: {lang_label})")
                        
                        st.code(secured_output_blueprint, language="python")
                        
                        # Dynamic Implementation Guide rendering
                        guide_title = "היכן להדביק את הקוד?" if detected_lang == "he" else "Where should I paste this code?"
                        st.info(f"📌 **{guide_title}**\n\n{implementation_instructions}")
                        
                except ValueError as val_err: st.error(f"Validation Error: {str(val_err)}")
        else: st.info("Awaiting execution data trigger. Press the button to pass variables through the security layers.")
