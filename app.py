import streamlit as st
import time
import hashlib
import socket
import requests

# ================= 基础配置 =================
SECRET = "LNCHD_PRIVATE_SALT"

st.set_page_config(
    page_title="LNCHD Network Diagnostic",
    page_icon="📡",
    layout="wide"
)

# ================= Token 校验 =================
def verify_token(token: str):
    try:
        uid, expire, sign = token.split(".")
        expire = int(expire)
        if time.time() > expire:
            return False

        raw = f"{uid}:{expire}:{SECRET}"
        check = hashlib.sha256(raw.encode()).hexdigest()[:16]
        return check == sign
    except:
        return False

# ================= 表面测速 / 诊断 =================
def network_diagnostic():
    st.title("📡 Network Diagnostic Tool")

    st.markdown(
        "Analyze your network connectivity, latency and DNS resolution performance."
    )

    col1, col2, col3 = st.columns(3)

    # -------- IP & ISP --------
    with col1:
        st.subheader("Public IP")
        try:
            ip = requests.get("https://api.ipify.org").text
            st.success(ip)
        except:
            st.warning("Unavailable")

    # -------- DNS --------
    with col2:
        st.subheader("DNS Resolution")
        domain = "google.com"
        try:
            ip_dns = socket.gethostbyname(domain)
            st.success(f"{domain} → {ip_dns}")
        except:
            st.error("DNS failed")

    # -------- 延迟模拟 --------
    with col3:
        st.subheader("Latency Test")
        start = time.time()
        try:
            requests.get("https://www.google.com", timeout=3)
            latency = int((time.time() - start) * 1000)
            st.success(f"{latency} ms")
        except:
            st.warning("Timeout")

    st.divider()

    # -------- 测速模拟 --------
    st.subheader("Download Speed Test")

    progress = st.progress(0)
    for i in range(100):
        time.sleep(0.01)
        progress.progress(i + 1)

    st.metric("Estimated Speed", "92 Mbps")
    st.caption("Results may vary depending on network conditions.")

    st.divider()

    st.caption("© 2026 LNCHD Network Diagnostic Service")

# ================= 真正的订阅输出 =================
def subscription_center():
    st.title("Configuration Center")

    st.markdown("Secure configuration access is enabled.")

    sub = """vless://UUID@lnchd.ppwq.us.kg:443?encryption=none&type=ws&path=%2Flnchd&security=tls#LNCHD"""

    st.code(sub, language="text")

    st.download_button(
        label="Download Configuration",
        data=sub,
        file_name="lnchd.conf"
    )

# ================= 主入口 =================
query = st.experimental_get_query_params()
token = query.get("token", [None])[0]

if token and verify_token(token):
    subscription_center()
else:
    network_diagnostic()
