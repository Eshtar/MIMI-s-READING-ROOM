import streamlit as st
import base64
import os
import random

# --- 1. 页面配置 ---
st.set_page_config(page_title="MIMI Reading Room", layout="wide", initial_sidebar_state="collapsed")

# --- 2. 资源加载 ---
@st.cache_data
def get_base64(path):
    try:
        if path and os.path.exists(path):
            with open(path, "rb") as f:
                return base64.b64encode(f.read()).decode()
    except: pass
    return ""

def get_files_from_dir(directory, exts):
    if not os.path.exists(directory): return []
    return [os.path.join(directory, f) for f in os.listdir(directory) if f.split('.')[-1].lower() in exts]

bg_base64 = get_base64("assets/my_card.jpg")
head_base64 = get_base64("assets/mimi_head.png")
walk_base64 = get_base64("assets/mimi_walk.png")
bgm_base64 = get_base64("assets/bg_music.mp3")
photos_list = get_files_from_dir("photos", ['jpg', 'png', 'jpeg'])
music_list = get_files_from_dir("music", ['mp3', 'wav'])
videos_list = get_files_from_dir("videos", ['mp4', 'mov'])

if "page" not in st.session_state: st.session_state.page = "landing"

# --- 3. CSS (浅灰细框风格) ---
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=ZCOOL+KuaiLe&display=swap');
    #MainMenu, header, footer {{visibility: hidden;}}
    .stDeployButton {{display:none;}}
    [data-testid="collapsedControl"] {{ display: none !important; }}
    
    [data-testid="stAppViewContainer"] {{
        background: url("data:image/jpeg;base64,{bg_base64}") no-repeat center center fixed;
        background-size: cover;
    }}
    .block-container {{
        max-width: 1000px !important; margin: 0 auto !important;
        padding-top: clamp(1.5rem, 6vh, 4rem) !important;
        display: flex !important; flex-direction: column !important; align-items: center !important;
    }}
    .mimi-banner {{
        background: #fff; color: #1b4332; width: 92%; max-width: 820px;
        padding: 20px 0; border-radius: 60px;
        font-family: 'ZCOOL KuaiLe', cursive; font-size: clamp(24px, 5vw, 48px);
        font-weight: 900; text-align: center; margin: -30px auto 20px auto;
        letter-spacing: 4px; border: 1px solid #eee;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }}
    div.stButton > button {{
        background-color: #1b4332 !important; color: white !important;
        border-radius: 40px !important; font-family: 'ZCOOL KuaiLe' !important;
        font-weight: 800 !important; font-size: 22px !important;
        width: 100% !important; max-width: 240px !important; height: 60px !important;
        border: none !important;
    }}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    if st.button("FINISH_ROUND"): st.session_state.page = "reward"; st.rerun()

st.markdown(f'<div style="text-align:center; z-index:20; position:relative;"><img src="data:image/png;base64,{head_base64}" style="width:160px; border-radius:50%; border:6px solid white;"></div>', unsafe_allow_html=True)
st.markdown('<div class="mimi-banner">MIMI IS WATCHING YOU</div>', unsafe_allow_html=True)

# --- 4. 路由逻辑 ---
if st.session_state.page == "landing":
    st.markdown('<div style="height: 40px;"></div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns([1, 1.2, 1.2, 1])
    with c2: 
        if st.button("咪来了"): st.session_state.page = "timer"; st.rerun()
    with c3:
        if st.button("咪走了"): st.stop()

elif st.session_state.page == "timer":
    selected_video = random.choice(videos_list) if videos_list else None
    video_uri = f"data:video/mp4;base64,{get_base64(selected_video)}" if selected_video else ""

    st.components.v1.html(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=ZCOOL+KuaiLe&display=swap');
        body {{ font-family: 'ZCOOL KuaiLe', sans-serif; margin: 0; background: transparent; overflow: hidden; }}
        .container {{ 
            background: #fff; border-radius: 35px; border: 1px solid #eee; 
            padding: 35px; width: 92%; max-width: 850px;
            margin: 40px auto 10px auto; position: relative;
            box-shadow: 0 12px 45px rgba(0,0,0,0.08);
        }}
        .bar-bg {{ width: 100%; height: 85px; background: #f1f8e9; border-radius: 50px; position: relative; border-bottom: 6px solid #6a994e; margin-top: 25px; display: flex; align-items: center; overflow: visible; }}
        
        .decorations {{ position: absolute; width: 85%; left: 4%; display: flex; justify-content: space-between; font-size: 22px; bottom: 8px; z-index: 5; opacity: 0.6; }}
        
        .walker {{ position: absolute; bottom: 10px; left: 0%; transition: left 1s linear; z-index: 90; display: flex; align-items: center; }}
        .walker img {{ height: 75px; }}
        .bubble {{ 
            position: absolute; background: white; border-radius: 12px; padding: 5px 14px; color: #1b4332; 
            font-size: 15px; font-weight: 800; border: 1px solid #eee;
            top: 2px; left: 65px; white-space: nowrap; display: none; z-index: 999;
            box-shadow: 0 3px 8px rgba(0,0,0,0.06); 
        }}
        #interact-overlay {{ display: none; position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: #fff; border-radius: 32px; z-index: 5000; flex-direction: column; align-items: center; justify-content: center; }}
        .timer-text {{ font-size: 80px; font-weight: 900; color: #1b4332; text-align: right; font-family: 'Courier New', monospace; margin-top: 15px; }}
        
        #duck-btn {{ position: absolute; top: 15px; right: 25px; font-size: 30px; background: none; border: none; cursor: pointer; z-index: 100; }}
        
        .mimi-btn {{ background: #1b4332; color: white; border: none; padding: 14px 40px; border-radius: 35px; font-family: 'ZCOOL KuaiLe'; font-size: 20px; cursor: pointer; margin-top: 18px; }}
    </style>

    <audio id="bgm" autoplay loop><source src="data:audio/mp3;base64,{bgm_base64}" type="audio/mpeg"></audio>

    <div class="container">
        <button id="duck-btn" onclick="toggleMute()">🦆</button>
        
        <div id="interact-overlay">
            <div style="color: #FFD700; -webkit-text-stroke: 1.5px #1b4332; font-size: 32px; margin-bottom: 25px; font-weight:900;">🐾 咪咪突击检查！</div>
            <div id="btn-group" style="display:flex; flex-direction:column; align-items:center; gap:12px;">
                <button class="mimi-btn" onclick="watchMimi()">休息看咪</button>
                <button class="mimi-btn" onclick="backToRead()">回去读书</button>
            </div>
            <div id="video-wrap" style="display:none; width:95%; text-align:center;">
                <video id="mimi-video" width="85%" controls playsinline style="border-radius:18px;"><source src="{video_uri}" type="video/mp4"></video><br>
                <button class="mimi-btn" onclick="backToRead()">回去读书</button>
            </div>
            <div id="auto-msg" style="margin-top:20px; font-size:15px; color:#1b4332; opacity:0.7; font-weight:bold;"></div>
        </div>

        <div class="bar-bg">
            <div class="decorations"><span>🌸</span><span>🌿</span><span>🌼</span><span>🌻</span><span>🌾</span><span>🌺</span></div>
            <div class="walker" id="walker">
                <img src="data:image/png;base64,{walk_base64}">
                <div class="bubble" id="bubble"></div>
            </div>
            <div style="position: absolute; right: 18px; font-size: 45px;">🦴</div>
        </div>
        <div class="timer-text" id="timer-val">30:00</div>
    </div>

    <script>
        var audio = document.getElementById("bgm"); audio.volume = 0.3;
        function toggleMute() {{ 
            audio.muted = !audio.muted; 
            document.getElementById('duck-btn').innerText = audio.muted ? "🔇" : "🦆";
        }}

        var total = 1800; // 正式版 30分钟
        var isPaused = false;
        var autoInterval;
        var msgs = {{ 15: "咪来陪你啦！🐾", 300: "汪汪汪嗷嗷 🦴", 600: "咪今天很高兴 ✨", 900: "一半啦，加油！🔥", 1200: "咪有点困了...💤", 1500: "咪想出去玩 🪁", 1760: "马上有骨头啦！🎁" }};

        function watchMimi() {{ clearInterval(autoInterval); document.getElementById('auto-msg').innerText = ""; document.getElementById('btn-group').style.display='none'; document.getElementById('video-wrap').style.display='block'; document.getElementById('mimi-video').play(); }}
        function backToRead() {{ clearInterval(autoInterval); isPaused = false; document.getElementById('interact-overlay').style.display='none'; document.getElementById('mimi-video').pause(); document.getElementById('btn-group').style.display='flex'; document.getElementById('video-wrap').style.display='none'; document.getElementById('auto-msg').innerText = ""; }}

        setInterval(function() {{
            if (isPaused) return;
            total--;
            var m = Math.floor(total/60); var s = total%60;
            document.getElementById('timer-val').innerHTML = (m<10?"0"+m:m)+":"+(s<10?"0"+s:s);
            document.getElementById('walker').style.left = ((1800-total)/1800*84) + "%";
            
            var elapsed = 1800 - total;
            var bubble = document.getElementById('bubble');
            if(msgs[elapsed]) {{ 
                bubble.innerText = msgs[elapsed]; 
                bubble.style.display='block'; 
                setTimeout(() => {{ bubble.style.display='none'; }}, 6000); 
            }}

            if (total == 900) {{ 
                isPaused = true; 
                document.getElementById('interact-overlay').style.display = 'flex'; 
                var remain = 120; 
                document.getElementById('auto-msg').innerText = remain + "秒无动作将默认回去读书...";
                autoInterval = setInterval(function() {{
                    remain--;
                    document.getElementById('auto-msg').innerText = remain + "秒无动作将默认回去读书...";
                    if(remain <= 0) backToRead();
                }}, 1000);
            }}
            if (total <= 0) {{ window.parent.document.querySelectorAll('button').forEach(b => {{ if(b.innerText.includes("FINISH_ROUND")) b.click(); }}); }}
        }}, 1000);
    </script>
    """, height=580)

elif st.session_state.page == "reward":
    st.balloons()
    st.markdown("<div style='background:#fff; padding:40px; border-radius:35px; border:1px solid #eee; text-align:center; width: 92%; max-width: 850px; margin: 20px auto; box-shadow: 0 12px 45px rgba(0,0,0,0.08);'>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='font-family:ZCOOL KuaiLe; color:#FFD700; font-size:45px; -webkit-text-stroke:1.5px #1b4332;'>🎊 读书完成！</h1>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: 
        if photos_list: st.image(random.choice(photos_list), use_column_width=True) 
    with c2:
        if music_list: st.audio(random.choice(music_list))
        if videos_list: st.video(random.choice(videos_list))
    if st.button("再读一轮"):
        st.session_state.page = "timer"; st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)