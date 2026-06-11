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
    """Manages multi-layered conversation history to track context, intent shifts, and user risk scores."""
    def __init__(self, max_history_len: int = 10):
        self.history: List[Dict[str, Any]] = []
        self.max_history_len = max_history_len
        self.global_risk_weight: float = 0.0  # Dynamic risk weight aggregated over the session

    def commit_interaction(self, intent_type: str, user_query: str, detected_risks: int, status: str):
        """Appends an interaction to memory and recalculates the session risk profile."""
        if len(self.history) >= self.max_history_len:
            self.history.pop(0)
            
        self.history.append({
            "timestamp": time.time(),
            "intent_type": intent_type,
            "query": user_query,
            "risks_count": detected_risks,
            "status": status
        })
        
        # Increment suspicion index dynamically based on bad inputs or blocked events
        self.global_risk_weight += (detected_risks * 1.5)
        if status == "BLOCKED":
            self.global_risk_weight += 5.0

    def get_last_intent(self) -> Optional[str]:
        """Extracts the immediate previous intent to preserve continuous conversational context."""
        if self.history:
            return self.history[-1]["intent_type"]
        return None

    def get_session_analytics(self) -> Dict[str, Any]:
        """Compiles real-time metrics for the SOC Dashboard."""
        return {
            "total_interactions": len(self.history),
            "accumulated_risk_score": self.global_risk_weight,
            "is_highly_suspicious": self.global_risk_weight > 7.0
        }


# =====================================================================
# 3. HIGH-STABILITY CRYPTOGRAPHIC SESSION & RATE REGULATOR
# =====================================================================
class EnterpriseSecurityContext:
    """Cryptographic session tracker with sliding window rate limiting to block DDoS/Brute-force."""
    def __init__(self, secret_key: str = "dynamic_quantum_safe_secret_key_2026"):
        self.secret_key = secret_key.encode()
        self.sessions: Dict[str, Dict[str, Any]] = {}
        self.rate_limits: Dict[str, List[float]] = {}
        self.memory_vault: Dict[str, AdvancedConversationMemory] = {}

    def generate_secure_fingerprint(self, ip: str, user_agent: str) -> str:
        """Generates a deterministic HMAC-SHA256 signature binding the client parameters."""
        raw_data = f"{ip}|{user_agent}".encode()
        return hmac.new(self.secret_key, raw_data, hashlib.sha256).hexdigest()

    def establish_session(self, ip: str, user_agent: str) -> str:
        """Provisions an isolated enterprise session with a dedicated memory space."""
        session_id = f"SEC-SESSION-{uuid.uuid4()}"
        fp = self.generate_secure_fingerprint(ip, user_agent)
        
        self.sessions[session_id] = {
            "fingerprint": fp,
            "bound_ip": ip,
            "established_at": time.time(),
            "last_seen": time.time()
        }
        self.memory_vault[session_id] = AdvancedConversationMemory()
        logger.info(f"Secure session provisioned: {session_id[:15]}... [FP Signature: {fp[:8]}]")
        return session_id

    def verify_session_integrity(self, session_id: str, ip: str, user_agent: str) -> bool:
        """Validates the session token against the computed cryptographic fingerprint."""
        if session_id not in self.sessions:
            return False
            
        session = self.sessions[session_id]
        current_fp = self.generate_secure_fingerprint(ip, user_agent)
        
        # Security Guardrail: Neutralize Session Hijacking and IP Spoofing
        if not hmac.compare_digest(session["fingerprint"], current_fp) or session["bound_ip"] != ip:
            logger.critical(f"CRITICAL HIJACKING ATTEMPT DETECTED FOR SESSION ID: {session_id}")
            return False
            
        session["last_seen"] = time.time()
        return True

    def enforce_sliding_window_rate_limit(self, client_id: str, max_reqs: int = 5, window: int = 15) -> bool:
        """Tracks incoming requests inside a precise moving time-frame window."""
        now = time.time()
        if client_id not in self.rate_limits:
            self.rate_limits[client_id] = []
            
        self.rate_limits[client_id] = [t for t in self.rate_limits[client_id] if now - t < window]
        
        if len(self.rate_limits[client_id]) >= max_reqs:
            return False
            
        self.rate_limits[client_id].append(now)
        return True

    def get_memory(self, session_id: str) -> AdvancedConversationMemory:
        """Retrieves the context memory mapped to the active session."""
        return self.memory_vault[session_id]


# =====================================================================
# 4. STRICT MULTI-TIER INPUT VALIDATOR (WAF SIMULATION)
# =====================================================================
class MultiTierInputValidator:
    """Sanitizes conversational inputs and performs deep regex inspections to kill active payloads."""
    
    @staticmethod
    def sanitize_string(text: str, max_chars: int = 5000) -> str:
        """Validates basic sizing and eliminates hidden control elements like Null Bytes."""
        if not text or not text.strip():
            raise ValueError("Input data stream is empty or null.")
        if len(text) > max_chars:
            raise ValueError(f"Input character cap exceeded (Max permitted: {max_chars}).")
            
        cleaned = text.replace("\x00", "").replace("\r", "")
        return cleaned

    @staticmethod
    def inspect_malicious_payloads(text: str) -> Tuple[bool, str]:
        """Scans the runtime prompt strings for malicious injection vectors."""
        inspection_rules = {
            r"(?i)UNION\s+ALL\s+SELECT": "SQLi Injection Vector",
            r"(?i)<iframe[^>]*>.*<\/iframe>": "Stored/Reflected XSS Vector",
            r"(?i)javascript\s*:\s*alert": "DOM XSS Vector",
            r"(__import__\s*\(|os\.system|subprocess\.|getattr\s*\()": "Remote Code Execution Payload"
        }
        
        for pattern, risk_name in inspection_rules.items():
            if re.search(pattern, text):
                return False, risk_name
        return True, "CLEAN"


# =====================================================================
# 5. AST STRUCTURAL DEEP CODE ANALYZER (STATIC ANALYSIS)
# =====================================================================
class ASTDeepAnalyzer:
    """Parses actual syntax tokens via Abstract Syntax Trees to surface concrete application vulnerabilities."""
    
    def analyze(self, source_code: str) -> List[Dict[str, Any]]:
        findings = []
        if not source_code.strip():
            return findings

        try:
            tree = ast.parse(source_code)
        except SyntaxError as e:
            return [{
                "type": "SyntaxError",
                "severity": "CRITICAL",
                "details": f"Source code fails compile check. Syntax trace error: {str(e)}",
                "line": e.lineno
            }]

        for node in ast.walk(tree):
            # Rule 1: Flag dangerous dynamic execution abstractions
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                if node.func.id in ['eval', 'exec']:
                    findings.append({
                        "type": "DynamicExecutionVulnerability",
                        "severity": "HIGH",
                        "details": f"Usage of dangerous primitive '{node.func.id}' enables untrusted code execution strings.",
                        "line": node.lineno
                    })

            # Rule 2: Deep inspect subprocess modules for command shell invocation strings
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                if node.func.attr in ['Popen', 'run', 'system'] or (isinstance(node.func.value, ast.Name) and node.func.value.id == 'os' and node.func.attr == 'system'):
                    is_shell_true = False
                    for keyword in node.keywords:
                        if keyword.arg == 'shell' and isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                            is_shell_true = True
                            
                    if is_shell_true or node.func.attr == 'system':
                        findings.append({
                            "type": "ShellCommandInjection",
                            "severity": "CRITICAL",
                            "details": f"Invoking host sub-processes via execution path '{node.func.attr}' maps directly to hostile command chain injections.",
                            "line": node.lineno
                        })

            # Rule 3: Detect hardcoded configuration secrets and passwords
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        variable_name = target.id.lower()
                        keywords = {'secret', 'password', 'token', 'apikey', 'private_key'}
                        if any(kw in variable_name for kw in keywords):
                            if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                                findings.append({
                                    "type": "HardcodedCryptographicSecret",
                                    "severity": "HIGH",
                                    "details": f"Identifier '{target.id}' stores a plaintext secret. Remediation required.",
                                    "line": node.lineno
                                })
        return findings


# =====================================================================
# 6. STRIDE COMPLIANT DYNAMIC THREAT MODELING ENGINE
# =====================================================================
class DynamicThreatModeler:
    """Maps static code findings alongside environmental context to structure an active Threat Matrix."""
    
    @staticmethod
    def build_matrix(vulnerabilities: List[Dict[str, Any]], conversation_risk_weight: float) -> Dict[str, Any]:
        base_score = 100.0
        # Reduce systemic score thresholds if conversational violations are detected
        base_score -= min(30.0, conversation_risk_weight)
        
        attack_vectors = []
        mitigations = []
        
        for v in vulnerabilities:
            v_type = v["type"]
            if v_type == "SyntaxError":
                base_score -= 10
                continue
                
            severity = v["severity"]
            if severity == "CRITICAL":
                base_score -= 25
            elif severity == "HIGH":
                base_score -= 15
            else:
                base_score -= 5

            if v_type == "ShellCommandInjection":
                attack_vectors.append("STRIDE: Tampering / Elevation of Privilege via OS Injection")
                mitigations.append("Pass parameters as structurally bounded Lists. Enforce shell=False.")
            elif v_type == "DynamicExecutionVulnerability":
                attack_vectors.append("STRIDE: Malicious Arbitrary Code Execution via Eval/Exec")
                mitigations.append("Leverage 'ast.literal_eval' strictly to handle structured dictionary strings cleanly.")
            elif v_type == "HardcodedCryptographicSecret":
                attack_vectors.append("STRIDE: Information Disclosure of System Configuration Credentials")
                mitigations.append("Extract secrets out of core source code files. Inject via secure Environment Variables.")

        return {
            "resilience_index": max(0.0, min(100.0, base_score)),
            "threat_vectors": list(set(attack_vectors)),
            "remediation_steps": list(set(mitigations))
        }


# =====================================================================
# 7. BLUEPRINT RULE-BASED DEFENSIVE PYTHON GENERATOR
# =====================================================================
class SmartDefensiveGenerator:
    """Enforces absolute safe-by-design patterns. Selects verified defensive code templates based on context."""
    
    def __init__(self):
        self.defensive_blueprint_rules = {
            "sql": self._blueprint_sql,
            "command": self._blueprint_command,
            "file": self._blueprint_file,
            "crypto": self._blueprint_crypto
        }

    def determine_intent(self, user_query: str, last_intent: Optional[str]) -> str:
        """Parses the current context and fallback states to map the semantic intent profile."""
        query_clean = user_query.lower()
        
        if any(w in query_clean for w in ["sql", "db", "database", "query", "fetch", "select"]):
            return "sql"
        if any(w in query_clean for w in ["command", "os", "subprocess", "ping", "execute", "shell"]):
            return "command"
        if any(w in query_clean for w in ["file", "path", "read", "open", "directory", "traversal"]):
            return "file"
        if any(w in query_clean for w in ["crypto", "hash", "password", "encrypt", "argon2", "pbkdf2", "secret"]):
            return "crypto"
            
        if last_intent:
            return last_intent
        return "generic"

    def synthesize_secure_code(self, determined_intent: str) -> str:
        """Returns the corresponding pre-compiled secure defensive architectural template."""
        generator_fn = self.defensive_blueprint_rules.get(determined_intent, self._blueprint_generic)
        return generator_fn()

    def _blueprint_sql(self) -> str:
        return '''def execute_secure_database_query(db_connection, client_supplied_id: int):
    """
    [DYNAMIC SECURE BLUEPRINT - SQL INJECTION DEFENSE]
    Implements mandatory Parameterized Queries. The database abstraction engine
    strictly decouples processing instructions from untrusted data blocks.
    """
    import logging
    try:
        # Enforce strong typing boundaries explicitly
        sanitized_id = int(client_supplied_id)
        
        with db_connection.cursor() as cursor:
            # Query strings use secure positional markers rather than unsafe string concatenation
            query = "SELECT account_id, balance, owner_name FROM accounts WHERE account_id = ?"
            cursor.execute(query, (sanitized_id,))
            row = cursor.fetchone()
            if row:
                return {"account_id": row[0], "balance": row[1], "owner_name": row[2]}
            return None
    except (ValueError, TypeError) as type_err:
        logging.error(f"Typing anomaly caught handling query initialization: {str(type_err)}")
        return None
    except Exception:
        logging.error("Internal transaction database failure occurred securely shielded.")
        return None
'''

    def _blueprint_command(self) -> str:
        return '''def execute_secure_network_diagnostic(target_destination: str) -> str:
    """
    [DYNAMIC SECURE BLUEPRINT - OS COMMAND INJECTION DEFENSE]
    Completely neutralizes OS Interpreters by dropping system shells and parsing strict input matrices.
    """
    import subprocess
    import re
    
    # Validation Tier: Validate structure against explicit alphanumerics to eliminate piping symbols
    whitelist_pattern = r"^[a-zA-Z0-9.-]+$"
    if not re.match(whitelist_pattern, target_destination):
        raise ValueError("Invalid target syntax: potential command control elements embedded.")
        
    try:
        # Execution Tier: Bounded arrays passed to sub-process tracking with shell context explicitly disabled
        execution_args = ["ping", "-c", "2", target_destination]
        execution_result = subprocess.run(
            execution_args, 
            capture_output=True, 
            text=True, 
            shell=False, 
            timeout=5
        )
        return execution_result.stdout
    except subprocess.TimeoutExpired:
        return "Operational run dropped out: system timeout constraint reached."
    except subprocess.CalledProcessError as err:
        return f"Underlying system failure caught: process returned exit state {err.returncode}"
'''

    def _blueprint_file(self) -> str:
        return '''def secure_file_retrieval(user_requested_path: str, storage_root_directory: str = "/app/user_space") -> str:
    """
    [DYNAMIC SECURE BLUEPRINT - PATH TRAVERSAL DEFENSE]
    Evaluates absolute canonicalized path traces to ensure parameters cannot escape the root boundary.
    """
    import os
    
    # Evaluate explicit resolved and absolute canonicalized path traces
    absolute_base = os.path.abspath(storage_root_directory)
    absolute_target = os.path.abspath(os.path.join(absolute_base, user_requested_path))
    
    # Verification Tier: Assert structural inclusion within the target folder boundary
    if not absolute_target.startswith(absolute_base):
        raise PermissionError("Access Violation: Local file directory escaping sequence identified!")
        
    if not os.path.exists(absolute_target):
        return "The requested filesystem resource cannot be located."
        
    with open(absolute_target, 'r', encoding='utf-8', errors='ignore') as active_file:
        return active_file.read()
'''

    def _blueprint_crypto(self) -> str:
        return '''def hash_password_pbkdf2(password_string: str) -> str:
    """
    [DYNAMIC SECURE BLUEPRINT - CRYPTOGRAPHIC STORAGE DEFENSE]
    Applies an advanced, compute-intensive Key Derivation Function (KDF) to protect against brute-forcing.
    """
    import hashlib
    import os
    
    generated_salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac(
        'sha256', 
        password_string.encode('utf-8'), 
        generated_salt, 
        100000
    )
    return f"{generated_salt.hex()}:{key.hex()}"
'''

    def _blueprint_generic(self) -> str:
        return '''def core_input_sanitizer(raw_data: str) -> str:
    """
    [DYNAMIC SECURE BLUEPRINT - XSS & INJECTION MITIGATION]
    Applies aggressive escaping rules over context strings before handling operations downstream.
    """
    if not raw_data:
        return ""
    import html
    return html.escape(raw_data.strip())[:1000]
'''


# =====================================================================
# 8. AUTONOMOUS DOUBLE SELF-CHECK COMPLIANCE ENGINE
# =====================================================================
class AutonomousSelfChecker:
    """An autonomous validation gate that verifies the safety of generated code before returning it."""
    
    @staticmethod
    def verify_safety_compliance(generated_python_code: str) -> bool:
        """Enforces a strict check over systemic safety rules inside generated scripts."""
        prohibited_indicators = [
            r"shell\s*=\s*True",
            r"eval\s*\(",
            r"exec\s*\(",
            r"os\.system\(",
            r"verify\s*=\s*False"
        ]
        
        for indicator in prohibited_indicators:
            if re.search(indicator, generated_python_code):
                return False
        return True


# =====================================================================
# 9. STREAMLIT ENTERPRISE UI & GRAPHICAL SOC ORCHESTRATOR
# =====================================================================

# Layout Initialization
st.set_page_config(page_title="Defensive AI Web Platform", page_icon="🛡️", layout="wide")

# Persistent Engine Allocation via Streamlit Session State
if "security_context" not in st.session_state:
    st.session_state.security_context = EnterpriseSecurityContext()
    st.session_state.code_analyzer = ASTDeepAnalyzer()
    st.session_state.generator = SmartDefensiveGenerator()
    st.session_state.session_id = None
    st.session_state.client_ip = "192.168.1.104"
    st.session_state.client_ua = "Mozilla/5.0 (X11; Linux x86_64) EnterpriseSecureAI/3.2"

# Ensure active session token registration
if not st.session_state.session_id:
    st.session_state.session_id = st.session_state.security_context.establish_session(
        st.session_state.client_ip, st.session_state.client_ua
    )

# Retrieve active memory tracking module bound to this cryptographic session
memory_vault = st.session_state.security_context.get_memory(st.session_state.session_id)

# --- Graphical Header Layout ---
st.title("🛡️ Enterprise Defensive AI Hub & SOC Radar Dashboard")
st.caption("Production Grade Monolith Implementation — Fully Standardized for Python 2026 Architectures")
st.markdown("---")

# --- Sidebar Control Center Panel ---
with st.sidebar:
    st.header("⚡ Live SIEM Infrastructure")
    st.text_input("Tracked Client IP", value=st.session_state.client_ip, disabled=True)
    st.text_input("Cryptographic Session ID", value=st.session_state.session_id, disabled=True)
    
    # Compute active signature footprint bindings
    signature_fp = st.session_state.security_context.generate_secure_fingerprint(
        st.session_state.client_ip, st.session_state.client_ua
    )
    st.text_input("Computed Token Fingerprint Signature", value=signature_fp[:32] + "...", disabled=True)
    
    st.markdown("---")
    st.subheader("📊 Dynamic Session Metrics")
    
    analytics = memory_vault.get_session_analytics()
    st.metric(label="Total Interaction History Nodes", value=analytics["total_interactions"])
    
    risk_score = analytics["accumulated_risk_score"]
    if analytics["is_highly_suspicious"] or risk_score > 7.0:
        st.error(f"🔴 System State: HIGH RISK SUSPICION ({risk_score:.2f})")
    elif risk_score > 0.0:
        st.warning(f"🟡 System State: MONITORING ELEVATED RISK ({risk_score:.2f})")
    else:
        st.success(f"🟢 System State: FULLY NOMINAL SECURE (0.00)")
        
    st.markdown("---")
    if st.sidebar.button("Flush Session & Clear State Parameters", type="secondary"):
        st.session_state.session_id = st.session_state.security_context.establish_session(
            st.session_state.client_ip, st.session_state.client_ua
        )
        st.rerun()

# --- Main Functional Columns Splits ---
col_workspace, col_siem_dashboard = st.columns([1, 1])

with col_workspace:
    st.header("🧠 Conversational Prompt Processing")
    user_prompt = st.text_input(
        "Enter your required execution request (Context-Aware Memory Active):", 
        value="Show me a secure strategy to parse structural user IDs out of a SQL data cluster."
    )
    
    st.header("🔬 Code Asset Structural Vulnerability Simulator")
    st.markdown("Paste source scripts here. The system parses them into abstract syntax blocks to calculate threat metrics.")
    
    default_flawed_script = '''def fragile_networking_utility(untrusted_user_payload):
    # Hardcoded sensitive parameter configuration string
    vault_access_key = "Secret_Token_Master_Pass_2026"
    
    import os
    # Dangerous host invocation vulnerability
    os.system("ping -c 1 " + untrusted_user_payload)
'''
    code_input_area = st.text_area("Source Code Input Workspace (Python Only):", value=default_flawed_script, height=220)
    
    execute_pipeline_trigger = st.button("Execute Secure Pipeline Optimization", type="primary")

with col_siem_dashboard:
    st.header("🖥️ Central SOC Telemetry Radar")
    
    if execute_pipeline_trigger:
        # Pipeline State 1: Enforce Active Sliding Window Checking Boundaries
        if not st.session_state.security_context.enforce_sliding_window_rate_limit(st.session_state.client_ip):
            st.error("🚨 CRITICAL RATE LIMIT BREACH: Excessive calls observed inside window timeframe. Operations suspended.")
            logger.warning(f"Rate limiting activated for resource: {st.session_state.client_ip}")
        else:
            # Pipeline State 2: Execute Input Vector Validation Checks
            try:
                sanitized_prompt = MultiTierInputValidator.sanitize_string(user_prompt)
                is_input_safe, attack_payload_vector = MultiTierInputValidator.inspect_malicious_payloads(sanitized_prompt)
                
                if not is_input_safe:
                    st.error(f"❌ MALICIOUS PAYLOAD INTERCEPTED BY WAF: [{attack_payload_vector}]")
                    memory_vault.commit_interaction("ATTACK", user_prompt, 5, "BLOCKED")
                    st.sidebar.error("ALERT: Malicious execution attempt flagged.")
                else:
                    # Pipeline State 3: Structural Logic AST Tree Code Analysis
                    findings_report = st.session_state.code_analyzer.analyze(code_input_area)
                    
                    # Pipeline State 4: Build Dynamic Threat Modeling Profiles
                    threat_matrix_profile = DynamicThreatModeler.build_matrix(findings_report, memory_vault.global_risk_weight)
                    
                    # Pipeline State 5: Context-Aware Safe-by-Design Synthesis
                    historical_intent_node = memory_vault.get_last_intent()
                    derived_intent = st.session_state.generator.determine_intent(sanitized_prompt, historical_intent_node)
                    secured_output_blueprint = st.session_state.generator.synthesize_secure_code(derived_intent)
                    
                    # Pipeline State 6: Run Autonomous Output Evaluation Loop Check
                    if not AutonomousSelfChecker.verify_safety_compliance(secured_output_blueprint):
                        st.warning("⚠️ Internal verification failure triggered on compiled output string! Rolling back to absolute generic sanitizer.")
                        secured_output_blueprint = st.session_state.generator.synthesize_secure_code("generic")
                    
                    # Commit successful workflow tracking node to Session Memory
                    memory_vault.commit_interaction(derived_intent, sanitized_prompt, len(findings_report), "SUCCESS")
                    
                    # RENDER RADAR GRAPHICAL DISPLAY BLOCKS
                    st.subheader("📈 STRIDE Resilience Matrix Calculation Score")
                    resilience_metric = threat_matrix_profile["resilience_index"]
                    
                    if resilience_metric >= 85.0:
                        st.success(f"Application Security Health Index Score: {resilience_metric:.1f} / 100.0")
                    elif resilience_metric >= 50.0:
                        st.warning(f"Application Security Health Index Score: {resilience_metric:.1f} / 100.0 (Attention Necessary)")
                    else:
                        st.error(f"Application Security Health Index Score: {resilience_metric:.1f} / 100.0 (Critical System Risks Present)")
                        
                    # Output Static Findings Logs
                    if findings_report:
                        st.markdown("### ⚠️ Active Vulnerability Matrix Findings")
                        for element in findings_report:
                            severity_badge = "🔴 CRITICAL" if element.get("severity") == "CRITICAL" else "🟡 HIGH"
                            st.markdown(f"**{severity_badge} - {element['type']}** (Detected on Line {element.get('line', 'N/A')})")
                            st.caption(element["details"])
                        
                        st.markdown("### 🛠️ Required Architectural Remediation Guidance Plan")
                        for step in threat_matrix_profile["remediation_steps"]:
                            st.info(step)
                    else:
                        st.success("✅ Abstract Syntax Tree Evaluation Complete: No security flaw signatures located in the analyzed code fragment.")
                        
                    # Output Secure Synthesized Asset Output
                    st.markdown("### 🛡️ Hardened Safe-by-Design Python Implementation Output")
                    st.caption(f"Synthesized matching current intent context: [**{derived_intent.upper()}**]")
                    st.code(secured_output_blueprint, language="python")
                    
            except ValueError as validation_error:
                st.error(f"Input Validation Invalidation Flag Tripped: {str(validation_error)}")
    else:
        st.info("Awaiting input data transmission. Press 'Execute Secure Pipeline Optimization' to pass metrics through the cognitive security stack layers.")

# --- Real-Time Historical SIEM Log Audit Feed Display ---
st.markdown("---")
st.subheader("📋 Session SIEM Internal Logs Audit Trail")
historical_log_nodes = memory_vault.history

if historical_log_nodes:
    for idx, log_entry in enumerate(reversed(historical_log_nodes)):
        timestamp_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(log_entry['timestamp']))
        status_color = "🟢 SUCCESS" if log_entry['status'] == "SUCCESS" else "🔴 BLOCKED"
        st.text(f"[{timestamp_str}] [NODE-{idx+1}] Intent: {log_entry['intent_type'].upper()} | Status: {status_color} | Analytical Flaws Logged: {log_entry['risks_count']}")
        st.caption(f"Query Fragment Logged: \"{html.escape(log_entry['query'])}\"")
else:
    st.caption("No historical transaction data points recorded inside current active session lifecycle parameters yet.")