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
    def __init__(self, max_history_len: int = 10):
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

    def get_last_intent(self) -> Optional[str]:
        if self.history:
            return self.history[-1]["intent_type"]
        return None

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
            raise ValueError(f"Input character cap exceeded.")
        return text.replace("\x00", "").replace("\r", "")

    @staticmethod
    def inspect_malicious_payloads(text: str) -> Tuple[bool, str]:
        inspection_rules = {
            r"(?i)UNION\s+ALL\s+SELECT": "SQLi Injection Vector",
            r"(?i)<iframe[^>]*>.*<\/iframe>": "XSS Vector",
            r"(?i)javascript\s*:\s*alert": "DOM XSS Vector",
            r"(__import__\s*\(|os\.system|subprocess\.|getattr\s*\()": "RCE Payload"
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
                                is_shell_true = True
                    if is_shell_true or node.func.attr == 'system':
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
# 7. BLUEPRINT RULE-BASED DEFENSIVE PYTHON GENERATOR
# =====================================================================
class SmartDefensiveGenerator:
    def __init__(self):
        self.blueprints = {
            "sql": '''def execute_secure_database_query(db_connection, client_supplied_id: int):\n    import logging\n    try:\n        sanitized_id = int(client_supplied_id)\n        with db_connection.cursor() as cursor:\n            query = "SELECT account_id, balance FROM accounts WHERE account_id = ?"\n            cursor.execute(query, (sanitized_id,))\n            return cursor.fetchone()\n    except Exception:\n        logging.error("Database transaction masked.")\n        return None''',
            "command": '''def execute_secure_network_diagnostic(target_destination: str) -> str:\n    import subprocess, re\n    if not re.match(r"^[a-zA-Z0-9.-]+$", target_destination):\n        raise ValueError("Invalid diagnostic target syntax.")\n    result = subprocess.run(["ping", "-c", "2", target_destination], capture_output=True, text=True, shell=False, timeout=5)\n    return result.stdout''',
            "file": '''def secure_file_retrieval(user_requested_path: str, storage_root: str = "/app/user_space") -> str:\n    import os\n    base = os.path.abspath(storage_root)\n    target = os.path.abspath(os.path.join(base, user_requested_path))\n    if not target.startswith(base):\n        raise PermissionError("Path Traversal Escape Blocked!")\n    with open(target, 'r', encoding='utf-8') as f:\n        return f.read()''',
            "crypto": '''def hash_password_pbkdf2(password_string: str) -> str:\n    import hashlib, os\n    salt = os.urandom(32)\n    key = hashlib.pbkdf2_hmac('sha256', password_string.encode(), salt, 100000)\n    return f"{salt.hex()}:{key.hex()}"'''
        }

    def determine_intent(self, user_query: str, last_intent: Optional[str]) -> str:
        query_clean = user_query.lower()
        if any(w in query_clean for w in ["sql", "db", "database", "query"]): return "sql"
        if any(w in query_clean for w in ["command", "os", "subprocess", "ping"]): return "command"
        if any(w in query_clean for w in ["file", "path", "read", "open"]): return "file"
        if any(w in query_clean for w in ["crypto", "hash", "password"]): return "crypto"
        return last_intent if last_intent else "generic"

    def synthesize_secure_code(self, determined_intent: str) -> str:
        return self.blueprints.get(determined_intent, '''def core_input_sanitizer(raw_data: str) -> str:\n    import html\n    return html.escape(raw_data.strip())[:1000]''')


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

# 🌐 בדיקת כתובת ה-URL: האם המשתמש ביקש את דף האדמין הסודי?
url_parameters = st.query_params
is_url_admin_mode = url_parameters.get("page") == "admin"

# --- אפשרות 1: המשתמש נמצא בנתיב האדמין הסודי ---
if is_url_admin_mode:
    st.title("🔑 Secret Admin Gate — Identity Verification")
    st.caption("Privileged routing detected via URL parameters. Cryptographic handshake required.")
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
                else:
                    st.error("Authentication Failure: Invalid Secret Signatures.")
            
            if st.button("← Return to Public Main Site"):
                st.query_params.clear() # מוחק את ה-admin מהכתובת ומחזיר לאתר הרגיל
                st.rerun()
    else:
        # פאנל האדמין המלא והסודי (נחשף רק אחרי סיסמה נכונה בכתובת הנכונה)
        st.header("👑 WELCOME BACK MASTER ADMIN")
        st.success("RBAC Status: FULL PRIVILEGED AUTHORIZATION ACTIVE")
        
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
        if historical_log_nodes:
            st.dataframe(historical_log_nodes, use_container_width=True)
        else:
            st.caption("No transaction nodes captured inside current session pipeline.")

# --- אפשרות 2: האתר הציבורי הרגיל (לא כתוב admin בכתובת) ---
else:
    st.title("🛡️ Enterprise Defensive AI Hub & SOC Radar Dashboard")
    st.caption("Production Grade Monolith Implementation — Public User Workspace")
    st.markdown("---")

    with st.sidebar:
        st.header("⚡ Live SIEM Infrastructure")
        st.text_input("Tracked Client IP", value=st.session_state.client_ip, disabled=True)
        st.text_input("Cryptographic Session ID", value=st.session_state.session_id[:20] + "...", disabled=True)
        
        analytics = memory_vault.get_session_analytics()
        st.metric(label="Total Interaction History Nodes", value=analytics["total_interactions"])
        risk_score = analytics["accumulated_risk_score"]
        
        if risk_score > 7.0:
            st.error(f"🔴 System State: HIGH RISK ({risk_score:.2f})")
        elif risk_score > 0.0:
            st.warning(f"🟡 System State: ELEVATED RISK ({risk_score:.2f})")
        else:
            st.success(f"🟢 System State: NOMINAL SECURE (0.00)")
            
        if st.button("Flush Session & Clear State", type="secondary"):
            st.session_state.session_id = st.session_state.security_context.establish_session(
                st.session_state.client_ip, st.session_state.client_ua
            )
            st.rerun()

    col_workspace, col_siem_dashboard = st.columns([1, 1])

    with col_workspace:
        st.header("🧠 Conversational Prompt Processing")
        user_prompt = st.text_input("Enter your request:", value="Show me a secure strategy to query user data.")
        
        st.header("🔬 Code Asset Vulnerability Simulator")
        default_flawed_script = 'def unsafe_utility(payload):\n    import os\n    db_pass = "Secret123"\n    os.system("ping -c 1 " + payload)'
        code_input_area = st.text_area("Source Code Input Workspace (Python Only):", value=default_flawed_script, height=180)
        
        execute_pipeline_trigger = st.button("Execute Secure Pipeline Optimization", type="primary")

    with col_siem_dashboard:
        st.header("🖥️ Central SOC Telemetry Radar")
        
        if execute_pipeline_trigger:
            rate_limit_passed = True
            if st.session_state.rate_limiting_enabled:
                rate_limit_passed = st.session_state.security_context.enforce_sliding_window_rate_limit(st.session_state.client_ip)
                
            if not rate_limit_passed:
                st.error("🚨 CRITICAL RATE LIMIT BREACH: Operations suspended inside window timeframe.")
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
                        
                        historical_intent_node = memory_vault.get_last_intent()
                        derived_intent = st.session_state.generator.determine_intent(sanitized_prompt, historical_intent_node)
                        secured_output_blueprint = st.session_state.generator.synthesize_secure_code(derived_intent)
                        
                        memory_vault.commit_interaction(derived_intent, sanitized_prompt, len(findings_report), "SUCCESS")
                        
                        st.subheader("📈 STRIDE Resilience Calculation Score")
                        resilience_metric = threat_matrix_profile["resilience_index"]
                        if resilience_metric >= 85.0:
                            st.success(f"Security Health Index Score: {resilience_metric:.1f} / 100.0")
                        else:
                            st.error(f"Security Health Index Score: {resilience_metric:.1f} / 100.0 (Risks Found)")
                            
                        if findings_report:
                            st.markdown("### ⚠️ Active Vulnerabilities Detected")
                            for element in findings_report:
                                st.markdown(f"**[{element['severity']}]** {element['type']}")
                                st.caption(element["details"])
                        else:
                            st.success("✅ No structural vulnerabilities found in code fragment.")
                            
                        st.markdown("### 🛡️ Hardened Safe-by-Design Python Implementation")
                        st.code(secured_output_blueprint, language="python")
                        
                except ValueError as val_err:
                    st.error(f"Validation Error: {str(val_err)}")
        else:
            st.info("Awaiting execution data trigger. Press the button to pass variables through the security layers.")
