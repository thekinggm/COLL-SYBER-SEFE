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
    def __init__(self, max_history_len: int = 20):  # Increased memory to 20 nodes
        self.history: List[Dict[str, Any]] = []
        self.max_history_len = max_history_len
        self.global_risk_weight: float = 0.0

    def commit_interaction(self, intent_type: str, user_query: str, detected_risks: int, status: str):
        if len(self.history) >= self.max_history_len:
            self.history.pop(0)
            
        self.history.append({
            "timestamp": time.time(),
            "intent_type": intent_type,
            "query": user_query,
            "risks_count": detected_risks,
            "status": status
        })
        
        self.global_risk_weight += (detected_risks * 1.5)
        if status == "BLOCKED":
            self.global_risk_weight += 5.0

    def get_deep_context_intent(self) -> Optional[str]:
        """
        PREMIUM FEATURE: Scans the extended interaction history to find the most 
        relevant security context, ensuring maximum contextual intelligence.
        """
        if not self.history:
            return None
        for interaction in reversed(self.history):
            intent = interaction["intent_type"]
            if intent in ["sql", "command", "file", "crypto", "xss", "brute", "csrf"]:
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
        
        # Admin Hash Configuration - Password: "AdminMaster2026!"
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

    def enforce_sliding_window_rate_limit(self, client_id: str, max_reqs: int = 5, window: int = 15) -> bool:
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
            r"(__import__\s*\(|os\.system|subprocess\.|getattr\s*\()": "RCE Server Payload"
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
                if node.func.attr in ['Popen', 'run', 'system'] or (isinstance(node.func.value, ast.Name) and node.func.value.id == 'os' and node.func.attr == 'system'):
                    is_shell_true = False
                    for keyword in getattr(node, 'keywords', []):
                        if keyword.arg == 'shell':
                            if isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                                import_shell_true = True
                    findings.append({"type": "ShellCommandInjection", "severity": "CRITICAL", "details": f"Subprocess invocation via '{node.func.attr}' allows host injection.", "line": getattr(node, 'lineno', 1)})

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
        # Ultra Hardened Premium Blueprints (Enterprise Production Architecture)
        self.premium_blueprints = {
            "sql": '''def execute_secure_database_query(db_connection, client_supplied_id: int) -> dict:
    """
    [ULTRA PREMIUM BLUEPRINT - SQL INJECTION DEFENSE]
    Enforces strict typing constraint validation combined with full cryptographic 
    abstraction layer using isolated Parameterized Queries bind arrays.
    """
    import logging
    try:
        sanitized_id = int(client_supplied_id)
        with db_connection.cursor() as cursor:
            query = "SELECT account_id, balance, owner_name, tier_level FROM accounts WHERE account_id = ?"
            cursor.execute(query, (sanitized_id,))
            row = cursor.fetchone()
            if row: 
                return {"account_id": row[0], "balance": row[1], "owner": row[2], "tier": row[3]}
            return {"status": "Record target identifier not found."}
    except (ValueError, TypeError) as type_err:
        logging.error(f"Security Alert: Data type boundary exception intercepted: {str(type_err)}")
        return {"status": "Error: Invalid parameter syntax provided."}
    except Exception:
        logging.critical("Fatal Database Abstract Intercept triggered securely.")
        return {"status": "Error: Internal server processing error."}''',
            
            "command": '''def execute_secure_network_diagnostic(target_destination: str) -> str:
    """
    [ULTRA PREMIUM BLUEPRINT - COMMAND INJECTION PROTECTION]
    Neutralizes remote host shell code interpolation threats via input alphanumeric regex whitelisting 
    and complete programmatic removal of system execution interpreter layers.
    """
    import subprocess, re
    if not re.match(r"^[a-zA-Z0-9.-]+$", target_destination.strip()):
        raise PermissionError("Security Exception: Malicious command characters detected inside sequence payload.")
    
    try:
        result = subprocess.run(
            ["ping", "-c", "2", target_destination.strip()], 
            capture_output=True, text=True, shell=False, timeout=5, check=True
        )
        return result.stdout
    except subprocess.TimeoutExpired:
        return "Diagnostic Error: Operation execution window timed out."
    except subprocess.CalledProcessError as cmd_err:
        return f"Execution Error Code [{cmd_err.returncode}]: Output terminal context unavailable."''',
            
            "file": '''def secure_file_retrieval(user_requested_path: str, storage_root: str = "/app/user_space") -> str:
    """
    [ULTRA PREMIUM BLUEPRINT - DIRECTORY TRAVERSAL SANITIZATION]
    Mitigates dynamic file retrieval path escaping sequences (../) by enforcing runtime 
    canonical absolute directory layout mapping checks.
    """
    import os
    base_directory = os.path.abspath(storage_root)
    computed_target_path = os.path.abspath(os.path.join(base_directory, user_requested_path))
    
    if not computed_target_path.startswith(base_directory):
        raise PermissionError("Access Violation Alert: Virtual machine sandbox traversal container escape blocked.")
        
    if not os.path.exists(computed_target_path):
        raise FileNotFoundError("Requested asset node cannot be located inside server storage index.")
        
    with open(computed_target_path, 'r', encoding='utf-8', errors='ignore') as active_file:
        return active_file.read()''',
            
            "crypto": '''def hash_password_pbkdf2(password_string: str) -> str:
    """
    [ULTRA PREMIUM BLUEPRINT - CRYPTOGRAPHIC HASH DERIVATION]
    Utilizes advanced high-entropy PBKDF2-HMAC-SHA256 computational derivation matrices.
    Applies dedicated pseudo-random salts to completely eliminate rainbow-table attack profiles.
    """
    import hashlib, os, secrets
    salt_vector = secrets.token_bytes(32)
    derived_key = hashlib.pbkdf2_hmac(
        hash_name='sha256',
        password=password_string.encode('utf-8'),
        salt=salt_vector,
        iterations=100000
    )
    return f"pbkdf2_sha256$100000${salt_vector.hex()}${derived_key.hex()}"''',

            "xss": '''def sanitize_html_output(untrusted_user_input: str) -> str:
    """
    [ULTRA PREMIUM BLUEPRINT - REFLECTED & STORED XSS BLOCKER]
    Deconstructs dangerous client payload injections using multi-layered null-byte scrubbing
    and context-aware strict HTML entity encoding matrices.
    """
    import html, re
    if not untrusted_user_input or not untrusted_user_input.strip():
        return ""
        
    scrubbed_payload = untrusted_user_input.replace("\\x00", "").strip()
    scrubbed_payload = re.sub(r"(?i)<script[^>]*>.*?</script>", "", scrubbed_payload)
    return html.escape(scrubbed_payload, quote=True)''',

            "brute": '''def verify_login_with_rate_limiting(username: str, client_ip: str, cache_connection) -> bool:
    """
    [ULTRA PREMIUM BLUEPRINT - BRUTE FORCE RATE CONTROLLER]
    Deploys a robust time-series ledger sliding-window mechanism tracking login authorization pipelines.
    Guards authentication routes against high-velocity automated account takeover scripts.
    """
    import time, logging
    current_epoch_time = time.time()
    tracking_window_key = f"auth_rate_limit:ip:{client_ip}"
    historical_attempts_ledger = cache_connection.get_attempts(tracking_window_key, since=current_epoch_time - 60)
    
    if len(historical_attempts_ledger) >= 5:
        logging.warning(f"Security Alert: Excessive authentication attempts blocked from Client IP {client_ip}")
        raise PermissionError("Access Temporarily Locked: Too many consecutive request parameters within 60s window.")
        
    return True''',

            "csrf": '''def generate_and_verify_csrf_token(session_context: dict, client_token: str = None) -> str:
    """
    [ULTRA PREMIUM BLUEPRINT - CROSS-SITE REQUEST FORGERY SHIELD]
    Generates and maps high-entropy anti-forgery request signature tokens tied directly to cryptographic session contexts.
    Utilizes constant-time token verification matrices to block side-channel comparison attacks.
    """
    import secrets, hmac
    if client_token is None:
        cryptographic_token = secrets.token_hex(32)
        session_context["secure_csrf_secret_key"] = cryptographic_token
        return cryptographic_token
        
    server_cached_token = session_context.get("secure_csrf_secret_key", "")
    if not server_cached_token:
        raise PermissionError("Security Handshake Refused: Context session token signature is missing.")
        
    if not hmac.compare_digest(server_cached_token, client_token):
        raise PermissionError("CSRF Attack Vector Triggered: Form challenge response validation has failed.")
        
    return "HANDSHAKE_VERIFIED"'''
        }
        
        # Free Grade Blueprints (Low Accuracy, Bad Formatting, Raw/Unfinished Scripts)
        self.free_blueprints = {
            "sql": '''# FREE VERSION: Basic casting. Might crash or fail under edge cases.\ndef quick_sql(user_id):\n    # Alert: Upgrade to Premium for parameterized query protection\n    return f"SELECT * FROM users WHERE id = {int(user_id)}"''',
            "command": '''# FREE VERSION: Incomplete regex checker. Dangerous primitive bypasses possible.\ndef basic_ping(ip):\n    import os\n    # Highly unrecommended. Premium subscription replaces os.system completely.\n    os.system("ping -c 1 " + ip)''',
            "file": '''# FREE VERSION: Only strips simple dots. Vulnerable to nested traversal attacks.\ndef simple_read(path):\n    # Upgrade to Premium to block advanced directory traversal validation\n    clean_path = path.replace("../", "")\n    return open(clean_path).read()''',
            "crypto": '''# FREE VERSION: Obsolete cryptography algorithm standard.\ndef weak_md5_hash(password):\n    import hashlib\n    # WARNING: MD5 has critical structural cryptographic collision bugs!\n    return hashlib.md5(password.encode()).hexdigest()''',
            "xss": '''# FREE VERSION: Basic tag replacement filter.\ndef raw_replace(text):\n    # Flawed. Does not neutralize advanced nested XSS vectors\n    return text.replace("<script>", "")''',
            "brute": '''# FREE VERSION: Inefficient counter tracking logic\ndef basic_count(user):\n    print("Log: checking attempts without distributed cluster cache sync.")\n    return True''',
            "csrf": '''# FREE VERSION: Dummy placeholder structure\ndef bypass_csrf():\n    return "CSRF verification disabled in FREE tier"'''
        }

    def determine_intent(self, user_query: str, last_intent: Optional[str], plan_tier: str) -> str:
        query_clean = user_query.lower().strip()
        
        # Free Tier ignores Hebrew entirely (simulating lower model capabilities)
        if plan_tier == "FREE":
            if "xss" in query_clean: return "xss"
            if "brute" in query_clean or "limit" in query_clean: return "brute"
            if "csrf" in query_clean: return "csrf"
            if "sql" in query_clean or "db" in query_clean: return "sql"
            if "command" in query_clean or "ping" in query_clean: return "command"
            if "file" in query_clean or "path" in query_clean: return "file"
            if "crypto" in query_clean or "hash" in query_clean or "password" in query_clean: return "crypto"
            return "generic"
            
        # Premium Tier has high-brainpower bilingual mapping dictionary
        else:
            xss_keywords = ["xss", "cross-site scripting", "script injection", "html escape", "sanitize input", "גניבת עוגיות", "הזרקת סקריפט", "עוגיות", "סניטציה"]
            if any(w in query_clean for w in xss_keywords): return "xss"
            brute_keywords = ["brute force", "rate limit", "ddos", "login block", "attempts", "הצפה", "חסימת משתמש", "ניחוש סיסמה", "מגבלת בקשות", "ברוט פורס"]
            if any(w in query_clean for w in brute_keywords): return "brute"
            csrf_keywords = ["csrf", "cross-site request forgery", "xsrf", "form token", "זיוף בקשה", "טוקן", "טפסים מאובטחים"]
            if any(w in query_clean for w in csrf_keywords): return "csrf"
            sql_keywords = ["sql", "db", "database", "query", "select", "בסיס נתונים", "שאילתה", "מסד", "נתונים"]
            if any(w in query_clean for w in sql_keywords): return "sql"
            command_keywords = ["command", "os", "subprocess", "ping", "terminal", "run", "טרמינל", "פקודה", "פינג", "להריץ"]
            if any(w in query_clean for w in command_keywords): return "command"
            file_keywords = ["file", "path", "read", "open", "directory", "קובץ", "לקרוא קובץ", "נתיב", "תיקייה"]
            if any(w in query_clean for w in file_keywords): return "file"
            crypto_keywords = ["crypto", "hash", "password", "encrypt", "sha", "md5", "salt", "הצפנה", "סיסמה", "האש", "להצפין"]
            if any(w in query_clean for w in crypto_keywords): return "crypto"
            
            return last_intent if last_intent else "generic"

    def synthesize_secure_code(self, determined_intent: str, plan_tier: str) -> str:
        active_blueprint_pool = self.premium_blueprints if plan_tier == "PREMIUM" else self.free_blueprints
        return active_blueprint_pool.get(determined_intent, '''def core_input_sanitizer(raw_data: str) -> str:\n    import html\n    return html.escape(raw_data.strip())[:1000]''')


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
    st.session_state.client_ua = "Mozilla/5.0 EnterpriseSecureAI/3.2"
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

    # Cleaned and streamlined sidebar layout
    with st.sidebar:
        st.header("💎 Subscription Account Plan")
        selected_plan = st.radio(
            "Select Account Tier Level:",
            ["FREE Tier (Throttled & Limited Model)", "PREMIUM Tier ($10/Mo - Full Core Vault)"],
            index=0
        )
        current_tier = "FREE" if "FREE" in selected_plan else "PREMIUM"
        
        st.markdown("---")
        if current_tier == "FREE":
            st.info("ℹ️ FREE Account Active: Bandwidth limits are tightly throttled. Hebrew parsing and multi-turn conversational memory are restricted.")
        else:
            st.success("🌟 PREMIUM Mode Active: Accessing multi-turn deep memory vaults and cryptographic production blueprints.")
            st.markdown("---")
            st.markdown("### 💳 Quick-Checkout Gateway")
            if st.button("🚀 UNLOCK PRODUCTION LICENSE — $10.00", type="primary"):
                st.toast("Opening Secure Checkout Handshake Encryption...", icon="⚡")
                time.sleep(0.4)
                
                # Highly aesthetic and professionally formatted checkout modal description box
                st.success("""
                ### 🔒 ENTERPRISE LICENSING GATEWAY OPENED
                
                Thank you for choosing our **Premium Defensive AI Engine**. Your license structure key is ready to deploy.
                
                **💎 Premium Architecture Features Included:**
                * 🧠 **Deep Context Memory Vault** — Tracks up to 20 conversation sessions.
                * ⚡ **Zero-Throttling Execution** — Unlocks full network pipeline limits.
                * 🛡️ **Bilingual Cognitive Analysis** — Complete native English & Hebrew support.
                * 📦 **Enterprise Grade Blueprints** — High-security code snippets with full error-handling frameworks.
                
                ---
                *To settle the payment ledger invoice safely via PayPal or secure Wire Transfer, please contact the founder and Lead Software Architect (Age 12) via corporate direct channels.*
                """)

        st.markdown("---")
        st.header("📊 Threat State Monitor")
        analytics = memory_vault.get_session_analytics()
        risk_score = analytics["accumulated_risk_score"]
        if risk_score > 7.0: st.error(f"🔴 STATE: HIGH CRITICAL RISK ({risk_score:.2f})")
        elif risk_score > 0.0: st.warning(f"🟡 STATE: ELEVATED RISK ({risk_score:.2f})")
        else: st.success(f"🟢 STATE: NOMINAL SECURE (0.00)")

    col_workspace, col_siem_dashboard = st.columns([1, 1])

    with col_workspace:
        st.header("🧠 Conversational Prompt Processing")
        default_prompt = "Give me code to prevent XSS attacks." if current_tier == "FREE" else "תראה לי קוד מאובטח שמנטרל תקיפות XSS"
        user_prompt = st.text_input("Enter your request:", value=default_prompt)
        
        st.header("🔬 Code Asset Vulnerability Simulator")
        default_flawed_script = 'def unsafe_utility(payload):\n    import os\n    db_pass = "Secret123"\n    os.system("ping -c 1 " + payload)'
        code_input_area = st.text_area("Source Code Input Workspace (Python Only):", value=default_flawed_script, height=180)
        
        execute_pipeline_trigger = st.button("Execute Secure Pipeline Optimization", type="primary")

    with col_siem_dashboard:
        st.header("🖥️ Central SOC Telemetry Radar")
        
        if execute_pipeline_trigger:
            rate_limit_passed = True
            if st.session_state.rate_limiting_enabled:
                max_allowed_requests = 2 if current_tier == "FREE" else 5
                rate_limit_passed = st.session_state.security_context.enforce_sliding_window_rate_limit(
                    st.session_state.client_ip, max_reqs=max_allowed_requests, window=20
                )
                
            if not rate_limit_passed:
                st.error(f"🚨 CRITICAL RATE LIMIT BREACH: [{current_tier} TIER CAP REACHED]. Upgrade to premium to restore transaction bandwidth.")
            else:
                try:
                    sanitized_prompt = MultiTierInputValidator.sanitize_string(user_prompt)
                    is_input_safe, attack_vector = MultiTierInputValidator.inspect_malicious_payloads(sanitized_prompt)
                    
                    if not is_input_safe:
                        st.error(f"❌ MALICIOUS PAYLOAD INTERCEPTED BY WAF: [{attack_vector}]")
                        memory_vault.commit_interaction("ATTACK", user_prompt, 5, "BLOCKED")
                    else:
                        findings_report = st.session_state.code_analyzer.analyze(code_input_area)
                        threat_matrix_profile = DynamicThreatModeler.build_matrix(findings_report, memory_vault.global_risk_weight)
                        
                        # PREMIUM tier triggers the new multi-turn deep scan search algorithm
                        historical_intent_node = memory_vault.get_deep_context_intent() if current_tier == "PREMIUM" else None
                        derived_intent = st.session_state.generator.determine_intent(sanitized_prompt, historical_intent_node, current_tier)
                        secured_output_blueprint = st.session_state.generator.synthesize_secure_code(derived_intent, current_tier)
                        
                        memory_vault.commit_interaction(derived_intent, sanitized_prompt, len(findings_report), "SUCCESS")
                        
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
                            
                        st.markdown(f"### 🛡️ Hardened [{current_tier} TIER] Python Implementation")
                        st.code(secured_output_blueprint, language="python")
                        
                except ValueError as val_err: st.error(f"Validation Error: {str(val_err)}")
        else: st.info("Awaiting execution data trigger. Press the button to pass variables through the security layers.")
