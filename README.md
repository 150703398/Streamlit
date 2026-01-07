# Streamlit APP 命令窗口

frok本仓库到你自己仓库

登陆https://share.streamlit.io/ ，选择carete app→Deploy a public app from GitHub→选择 Fork 后的仓库，然后部署就可以

如果要创建节点，使用以下命令cd ~ &&   curl -fsSL https://raw.githubusercontent.com/150703398/Streamlit/refs/heads/main/agsb.py | python3 - install  --uuid 自己uuid --port 自己cloudflare Tunnel端口  --agk 自己cloudflare Tunne令牌  --domain cloudflare Tunnel域名（如果不使用固定Tunnel，port、agk、domain后面留空）。
