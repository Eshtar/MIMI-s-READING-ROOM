import streamlit as st
import base64
import os
import random

# --- 1. 页面配置 ---
st.set_page_config(page_title="MIMI Reading Room", layout="wide", initial_sidebar_state="collapsed")

# --- 2. 资源读取工具 ---
def get_base64(path):
    if path and os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

def get_files_from_dir(directory, exts):
    if not os.path.exists(directory):
        return []
    return [os.path.join(directory, f) for f in os.listdir(directory) if f.split('.')[-1].lower() in exts]

# 加载静态资源
bg_base64 = get_base64("assets/my_card.jpg")
head_base64 = get_base64("assets/mimi_head.png")
walk_base64 = get_base64("assets/mimi_walk.png")
bgm_base64 = get_base64("assets/bg_music.mp3")

photos_list = get_files_from_dir("photos", ['jpg', 'png', 'jpeg'])
music_list = get_files_from_dir("music", ['mp3', 'wav'])
videos_list = get_files_from_dir("videos", ['mp4', 'mov'])

# --- 3. 全局状态 ---
if "page" not in st.session_state: st.session_state.page = "landing"
if "round" not in st.session_state: st.session_state.round = 1

# --- 4. CSS 样式 ---
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=ZCOOL+KuaiLe&display=swap');
    #MainMenu, header, footer {{visibility: hidden;}}
    .stDeployButton {{display:none;}}
    [data-testid="collapsedControl"] {{ display: none !important; }}
    section[data-testid="stSidebar"] {{ display: none !important; width: 0 !important; }}
    
    [data-testid="stAppViewContainer"] {{
        background: url("data:image/jpeg;base64,{bg_base64}") no-repeat center center fixed;
        background-size: cover;
    }}
    .block-container {{
        max-width: 1000px !important; margin: 0 auto !important;
        display: flex !important; flex-direction: column !important;
        align-items: center !important; padding-top: 2rem !important;
    }}
    .mimi-banner {{
        background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(10px); color: #1b4332;
        width: 850px; padding: 20px 0; border-radius: 60px; font-family: 'ZCOOL KuaiLe', cursive;
        font-size: 52px; font-weight: 1000; text-align: center;
        margin: -35px auto 0 auto; letter-spacing: 5px; border: 2px solid #1b4332;
    }}
    div.stButton > button {{
        background-color: #1b4332 !important; color: white !important;
        border-radius: 40px !important; font-family: 'ZCOOL KuaiLe' !important;
        font-weight: 900 !important; font-size: 26px !important;
        min-width: 200px !important; height: 65px !important; border: none !important;
    }}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    if st.button("FINISH_ROUND"):
        st.session_state.page = "reward"
        st.rerun()

# --- 5. 顶栏 ---
st.markdown(f'<div style="text-align:center; z-index:20; position:relative;"><img src="data:image/png;base64,{head_base64}" style="width:190px; border-radius:50%; border:5px solid white; box-shadow: 0 10px 20px rgba(0,0,0,0.1);"></div>', unsafe_allow_html=True)
st.markdown('<div class="mimi-banner">MIMI IS WATCHING YOU</div>', unsafe_allow_html=True)

# --- 6. 路由逻辑 ---
if st.session_state.page == "landing":
    st.markdown('<div style="height: 60px;"></div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns([1, 1.2, 1.2, 1])
    with c2:
        if st.button("咪来了"):
            st.session_state.page = "timer"
            st.rerun()
    with c3:
        if st.button("咪走了"): st.stop()

elif st.session_state.page == "timer":
    selected_video = random.choice(videos_list) if videos_list else None
    video_base64 = get_base64(selected_video)
    video_data_uri = f"data:video/mp4;base64,{video_base64}" if video_base64 else ""

    st.components.v1.html(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=ZCOOL+KuaiLe&display=swap');
        body {{ font-family: 'ZCOOL KuaiLe', sans-serif; overflow: hidden; margin: 0; }}
        .container {{ 
            background: rgba(255,255,255,0.85); border-radius: 30px; padding: 40px; 
            width: 850px; border: 3px solid #1b4332; margin: 20px auto; 
            position: relative; box-sizing: border-box; 
        }}
        #interact-overlay {{
            display: none; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(255,255,255,0.98); border-radius: 30px; z-index: 200;
            flex-direction: column; align-items: center; justify-content: center;
        }}
        .interact-title {{ color: #FFD700; -webkit-text-stroke: 1.5px #1b4332; font-size: 40px; margin-bottom: 25px; }}
        .btn-group {{ display: flex; gap: 20px; }}
        .action-btn {{ background: #1b4332; color: white; border: none; padding: 15px 40px; border-radius: 40px; font-family: 'ZCOOL KuaiLe'; font-size: 24px; cursor: pointer; }}
        .duck-btn {{ position: absolute; top: 15px; right: 20px; font-size: 45px; cursor: pointer; background: transparent; border: none; z-index: 100; }}
        .bar-bg {{ width: 100%; height: 80px; background: #f1f8e9; border-radius: 40px; position: relative; border-bottom: 6px solid #6a994e; margin-top: 60px; display: flex; align-items: center; }}
        .walker {{ position: absolute; bottom: 18px; left: 0%; transition: left 1s linear; z-index: 90; height: 65px; }}
        .bone {{ position: absolute; right: 20px; font-size: 45px; top: 10px; }}
        .bubble {{ 
            position: absolute; background: white; border-radius: 20px; padding: 8px 15px; 
            color: #1b4332; font-size: 18px; border: 2px solid #1b4332; 
            top: -65px; left: 50%; transform: translateX(-50%); white-space: nowrap; display: none; 
        }}
        .bubble::after {{ content: ''; position: absolute; bottom: -10px; left: 50%; margin-left: -10px; border-width: 10px 10px 0; border-style: solid; border-color: white transparent; }}
        .timer-text {{ font-size: 75px; font-weight: 900; color: #1b4332; text-align: right; font-family: 'Courier New', monospace; margin-top: 10px; }}
        #video-wrap {{ display: none; width: 80%; margin-top: 15px; text-align: center; }}
        video {{ width: 100%; border-radius: 15px; border: 3px solid #1b4332; max-height: 250px; }}
    </style>

    <audio id="bgm" autoplay loop><source src="data:audio/mp3;base64,{bgm_base64}" type="audio/mpeg"></audio>

    <div class="container">
        <div id="interact-overlay">
            <div class="interact-title">🐾 咪咪的检查时刻！你在看书吗？</div>
            <div id="btn-group" class="btn-group">
                <button class="action-btn" onclick="watchMimi()">看咪</button>
                <button class="action-btn" onclick="backToRead()">看书</button>
            </div>
            <div id="video-wrap">
                <video id="mimi-video" controls><source src="{video_data_uri}" type="video/mp4"></video>
                <br>
                <button class="action-btn" style="margin-top:10px" onclick="backToRead()">看完了</button>
            </div>
        </div>

        <button class="duck-btn" id="mute-btn" onclick="toggleMute()">🦆</button>
        <div class="bar-bg">
            <div class="walker" id="walker">
                <div class="bubble" id="bubble"></div>
                <img src="data:image/png;base64,{walk_base64}" style="height:65px; width:auto;">
            </div>
            <div class="bone">🦴</div>
        </div>
        <div class="timer-text" id="timer-val"></div>
    </div>

    <script>
        var audio = document.getElementById("bgm");
        audio.volume = 0.3;
        function toggleMute() {{ 
            audio.muted = !audio.muted; 
            document.getElementById("mute-btn").style.opacity = audio.muted ? "0.3" : "1"; 
        }}

        // --- 正式时间设置 ---
        var total = 1800; // 30分钟
        var totalTime = 1800;
        var isPaused = false;
        var autoTimer;

        var msgs = {{ 
            2: "咪在看你哦 👁️", 4: "要喝点水吗？☕", 6: "咪伸个懒腰 🐈", 8: "进度条在动耶 🦴",
            10: "咪要睡觉了 💤", 12: "书好点心好 📖", 14: "咪想抓蝴蝶 🦋", 16: "咪在陪着你 🐾",
            18: "还要多久呀？⌛", 20: "咪要喝水 💧", 22: "快读完啦！🚀", 24: "咪要吃罐罐 🍱",
            26: "你是最棒的 🌟", 28: "准备领奖励吧 🎁"
        }};

        function watchMimi() {{
            document.getElementById('btn-group').style.display = 'none';
            document.getElementById('video-wrap').style.display = 'block';
            var v = document.getElementById('mimi-video');
            v.load();
            v.play();
            clearTimeout(autoTimer);
        }}

        function backToRead() {{
            isPaused = false;
            document.getElementById('interact-overlay').style.display = 'none';
            document.getElementById('mimi-video').pause();
            document.getElementById('video-wrap').style.display = 'none';
            document.getElementById('btn-group').style.display = 'flex';
            clearTimeout(autoTimer);
        }}

        setInterval(function() {{
            if (isPaused) return;
            total--;
            
            var m = Math.floor(total / 60); var s = total % 60;
            document.getElementById('timer-val').innerHTML = (m < 10 ? "0" + m : m) + ":" + (s < 10 ? "0" + s : s);
            document.getElementById('walker').style.left = ((totalTime - total) / totalTime * 85) + "%";

            var elapsedMin = Math.floor((totalTime - total) / 60);
            var currentSec = total % 60;
            var bubble = document.getElementById('bubble');
            if (msgs[elapsedMin] && currentSec >= 50) {{
                bubble.innerHTML = msgs[elapsedMin]; bubble.style.display = 'block';
            }} else {{
                bubble.style.display = 'none';
            }}

            if (total == 900) {{ // 15分钟互动点
                isPaused = true;
                document.getElementById('interact-overlay').style.display = 'flex';
                autoTimer = setTimeout(backToRead, 120000); // 2分钟无操作自动返回
            }}

            if (total <= 0) {{
                window.parent.document.querySelectorAll('button').forEach(b => {{
                    if (b.innerText === "FINISH_ROUND") b.click();
                }});
            }}
        }}, 1000);
    </script>
    """, height=450)

elif st.session_state.page == "reward":
    st.balloons()
    r = st.session_state.round
    st.markdown("<div style='background:rgba(255,255,255,0.95); padding:40px; border-radius:30px; border:4px solid #1b4332; text-align:center; width: 850px; margin: 20px auto;'>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='font-family:ZCOOL KuaiLe; color:#FFD700;'>🎉 第 {r} 轮阅读达成！</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    col_p, col_v = st.columns(2)
    with col_p:
        st.write("📷 **咪咪写真**")
        if photos_list: st.image(random.choice(photos_list))
    with col_v:
        st.write("🎵 **专注音乐**")
        if music_list: st.audio(random.choice(music_list))
        st.write("🎬 **治愈视频**")
        if videos_list: st.video(random.choice(videos_list))

    if st.button("再来一轮"):
        st.session_state.round += 1
        st.session_state.page = "timer"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)