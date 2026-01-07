# streamlit_speedtest_node_app.py
# 完整可运行版本（share.streamlit.io 适用）
# 功能：
# 1. 表面伪装为【网络测速网站】
# 2. 保留节点/订阅生成能力
# 3. 订阅接口加 Token（默认 sub）防泄露
# 4. 普通访问与订阅接口完全隔离

import streamlit as st
import time
import uuid
import base64
from urllib.parse import urlencode

# ================== 基础配置 ==================
APP_TITLE = "NetSpeed Pro"
APP_SUBTITLE = "Accurate Network Speed Test & Network Diagnostics"
DEFAULT_TOKEN = "sub"        # 订阅 Token（可自行修改）
SUB_PATH = "sub"             # 订阅路径

# ================== 节点配置（可替换为你原逻辑） ==================
# 这里示例使用 VLESS Reality
NODES = [
    {
        "name": "Edge-HK",
        "server": "example.com",
        "port": 443,
        "uuid": "11111111-1111-1111-1111-111111111111",
        "flow": "xtls-rprx-vision",
        "security": "reality",
        "sni": "www.cloudflare.com",
        "fp": "chrome"
    }
]

# ================== 订阅生成 ==================

def generate_subscription():
    links = []
    for n in NODES:
        link = (
            f"vless://{n['uuid']}@{n['server']}:{n['port']}?"
            f"type=tcp&security={n['security']}&flow={n['flow']}&"
            f"sni={n['sni']}&fp={n['fp']}"
            f"#{n['name']}"
        )
        links.append(link)

    raw = "\n".join(links)
    return base64.b64encode(raw.encode()).decode()


# ================== Token 校验 ==================

def verify_token():
    params = st.experimental_get_query_params()
    token = params.get("token", [None])[0]
    if token != DEFAULT_TOKEN:
        # 伪装成测速失败，而不是直接暴露接口
        st.write("Speed test failed. Please refresh and try again.")
        st.stop()


# ================== 路由判断 ==================
params = st.experimental_get_query_params()
path = params.get("path", ["/"])[0].strip("/")

# 订阅接口：/?path=sub&token=sub
if path == SUB_PATH:
    verify_token()
    st.text(generate_subscription())
    st.stop()

# ================== 正常测速网站 ==================
st.set_page_config(page_title=APP_TITLE, layout="centered")

st.markdown(
    """
    <style>
    body { background-color: #0f172a; color: #e5e7eb; }
    .metric { font-size: 40px; font-weight: 700; }
    .label { color: #94a3b8; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title(APP_TITLE)
st.caption(APP_SUBTITLE)

st.markdown("---")

# ================== 测速逻辑 ==================
if st.button("Start Speed Test"):
    with st.spinner("Testing download speed..."):
        time.sleep(1.4)
        download = round(80 + (uuid.uuid4().int % 50), 2)

    with st.spinner("Testing upload speed..."):
        time.sleep(1.1)
        upload = round(25 + (uuid.uuid4().int % 20), 2)

    with st.spinner("Testing latency..."):
        time.sleep(0.7)
        latency = round(6 + (uuid.uuid4().int % 18), 1)

    c1, c2, c3 = st.columns(3)
    c1.markdown(f"<div class='metric'>{download}</div><div class='label'>Mbps Download</div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='metric'>{upload}</div><div class='label'>Mbps Upload</div>", unsafe_allow_html=True)
    c3.markdown(f"<div class='metric'>{latency}</div><div class='label'>ms Ping</div>", unsafe_allow_html=True)

st.markdown("---")

# ================== 网络诊断模块 ==================
st.subheader("Network Diagnostics")
st.write("• ISP Routing Quality")
st.write("• CDN Reachability")
st.write("• DNS Resolution Status")
st.write("• Packet Loss Estimation")

# ================== 隐蔽订阅入口 ==================
with st.expander("Advanced Tools"):
    qs = urlencode({"path": SUB_PATH, "token": DEFAULT_TOKEN})
    sub_url = f"/?{qs}"
    st.code(sub_url)
    st.caption("Use this URL as a subscription link in your client.")
