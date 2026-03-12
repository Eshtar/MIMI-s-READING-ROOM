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

# --- 3. CSS 样式 ---
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=ZCOOL+KuaiLe&display=swap');
    #MainMenu, header, footer {{visibility: hidden;}}
    .stDeployButton {{display:none;}}
    [data-testid="collapsedControl"] {{ display: none !important; }}
    
    [data-testid="stAppViewContainer"] {{
        background: url("data:image/jpeg;base64,{bg_base64}") no-repeat center center fixed !important;
        background-size: cover !important;
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
        z-index: 10; position: relative;
    }}
    div.stButton > button {{
        background-color: #1b4332 !important; color: white !important;
        border-radius: 40px !important; font-family: 'ZCOOL KuaiLe' !important;
        font-weight: 800 !important; font-size: 22px !important;
        width: 100% !important; height: 65px !important;
        border: 2px solid white !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
    }}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    if st.button("FINISH_ROUND"): st.session_state.page = "reward"; st.rerun()

# 顶部头像和横幅
st.markdown(f'<div style="text-align:center; z-index:20; position:relative;"><img src="data:image/png;base64,{head_base64}" style="width:160px; height:160px; border-radius:50%; border:6px solid white; object-fit: cover;"></div>', unsafe_allow_html=True)
st.markdown('<div class="mimi-banner">MIMI IS WATCHING YOU</div>', unsafe_allow_html=True)

# --- 4. 页面路由 ---
if st.session_state.page == "landing":
    st.markdown('<div style="height: 40px;"></div>', unsafe_allow_html=True)
    
    # [1, 1, 1, 1] 四等分，完美居中对称
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    with col2:
        if st.button("咪来了", use_container_width=True): 
            st.session_state.page = "timer"
            st.rerun()
    with col3:
        if st.button("咪走了", use_container_width=True): 
            st.stop()

elif st.session_state.page == "timer":
    selected_video = random.choice(videos_list) if videos_list else None
    video_uri = f"data:video/mp4;base64,{get_base64(selected_video)}" if selected_video else ""

    # 正式版 HTML (30分钟总长，15分钟突击检查，明黄色提示字)
    st.components.v1.html(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=ZCOOL+KuaiLe&display=swap');
        body {{ font-family: 'ZCOOL KuaiLe', sans-serif; margin: 0; background: transparent; overflow: hidden; }}
        .container {{ background: #fff; border-radius: 35px; border: 1px solid #eee; padding: 35px; width: 92%; max-width: 850px; margin: 40px auto 10px auto; position: relative; box-shadow: 0 12px 45px rgba(0,0,0,0.08); }}
        .bar-bg {{ width: 100%; height: 85px; background: #f1f8e9; border-radius: 50px; position: relative; border-bottom: 6px solid #6a994e; margin-top: 25px; display: flex; align-items: center; overflow: visible; }}
        .decorations {{ position: absolute; width: 85%; left: 4%; display: flex; justify-content: space-between; font-size: 22px; bottom: 8px; z-index: 5; opacity: 0.6; }}
        .walker {{ position: absolute; bottom: 10px; left: 0%; transition: left 1s linear; z-index: 90; display: flex; align-items: center; }}
        .walker img {{ height: 75px; }}
        .bubble {{ position: absolute; background: white; border-radius: 12px; padding: 5px 14px; color: #1b4332; font-size: 15px; font-weight: 800; border: 1px solid #eee; top: 2px; left: 65px; white-space: nowrap; display: none; z-index: 999; box-shadow: 0 3px 8px rgba(0,0,0,0.06); }}
        #interact-overlay {{ display: none; position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: #fff; border-radius: 32px; z-index: 5000; flex-direction: column; align-items: center; justify-content: center; }}
        .timer-text {{ font-size: 80px; font-weight: 900; color: #1b4332; text-align: right; font-family: 'Courier New', monospace; margin-top: 15px; }}
        #duck-btn {{ position: absolute; top: 15px; right: 25px; font-size: 30px; background: none; border: none; cursor: pointer; z-index: 100; }}
        .mimi-btn {{ background: #1b4332; color: white; border: none; padding: 14px 40px; border-radius: 35px; font-family: 'ZCOOL KuaiLe'; font-size: 20px; cursor: pointer; margin-top: 18px; }}
        /* 明黄色的倒计时提示语，增加了轻微阴影保证白底可见度 */
        #auto-msg {{ margin-top: 20px; font-size: 16px; color: #FFD700; font-weight: 900; opacity: 1; text-shadow: 1px 1px 2px rgba(0,0,0,0.2); letter-spacing: 1px; }}
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
                <video id="mimi-video" width="85%" controls playsinline style="border-radius:18px; margin-bottom: 15px;"><source src="{video_uri}" type="video/mp4"></video><br>
                <button class="mimi-btn" onclick="backToRead()">继续看书</button>
            </div>
            <div id="auto-msg"></div>
        </div>
        <div class="bar-bg">
            <div class="decorations"><span>🌸</span><span>🌿</span><span>🌼</span><span>🌻</span><span>🌾</span><span>🌺</span></div>
            <div class="walker" id="walker">
                <img src="data:image/png;base64,{walk_base64}">
                <div class="bubble" id="bubble"></div>
            </div>
            <div style="position: absolute; right: 18px; font-size: 45px;">🦴</div>
        </div>
        <div id="timer-val" class="timer-text">30:00</div>
    </div>

    <script>
        var audio = document.getElementById("bgm"); audio.volume = 0.3;
        function toggleMute() {{ audio.muted = !audio.muted; document.getElementById('duck-btn').innerText = audio.muted ? "🔇" : "🦆"; }}

        // 正式版：总长 1800 秒 (30分钟)
        var total = 1800; 
        var isPaused = false;
        var autoInterval;
        var msgs = {{ 15: "咪来陪你啦！🐾", 300: "汪汪汪嗷嗷 🦴", 600: "咪今天很高兴 ✨", 900: "一半啦，加油！🔥", 1200: "咪有点困了...💤", 1500: "咪想出去玩 🪁", 1760: "马上有骨头啦！🎁" }};

        function watchMimi() {{ clearInterval(autoInterval); document.getElementById('btn-group').style.display='none'; document.getElementById('video-wrap').style.display='block'; document.getElementById('mimi-video').play(); }}
        function backToRead() {{ clearInterval(autoInterval); isPaused = false; document.getElementById('interact-overlay').style.display='none'; document.getElementById('mimi-video').pause(); document.getElementById('btn-group').style.display='flex'; document.getElementById('video-wrap').style.display='none'; }}

        setInterval(function() {{
            if (isPaused) return;
            total--;
            var m = Math.floor(total/60); var s = total%60;
            document.getElementById('timer-val').innerHTML = (m<10?"0"+m:m)+":"+(s<10?"0"+s:s);
            document.getElementById('walker').style.left = ((1800-total)/1800*84) + "%";
            
            var elapsed = 1800 - total;
            var b = document.getElementById('bubble');
            if(msgs[elapsed]) {{ 
                b.innerText = msgs[elapsed]; b.style.display='block'; 
                setTimeout(() => {{ b.style.display='none'; }}, 5000); 
            }}
            
            // 正式版：900 秒 (15分钟) 时突击检查
            if (total == 900) {{ 
                isPaused = true; document.getElementById('interact-overlay').style.display = 'flex'; 
                var rem = 15; // 15秒无动作自动返回
                autoInterval = setInterval(function() {{
                    rem--; 
                    document.getElementById('auto-msg').innerText = rem + "秒无动作将默认回去读书...";
                    if(rem <= 0) backToRead();
                }}, 1000);
            }}
            
            if (total <= 0) {{ window.parent.document.querySelectorAll('button').forEach(btn => {{ if(btn.innerText.includes("FINISH_ROUND")) btn.click(); }}); }}
        }}, 1000);
    </script>
    """, height=600)

elif st.session_state.page == "reward":
    st.balloons()
    st.markdown("<div style='background:#fff; padding:40px; border-radius:35px; border:1px solid #eee; text-align:center; width: 92%; max-width: 850px; margin: 20px auto; box-shadow: 0 12px 45px rgba(0,0,0,0.08);'>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='font-family:ZCOOL KuaiLe; color:#FFD700; font-size:45px; -webkit-text-stroke:1.5px #1b4332;'>🎊 读书完成！</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    # 防报错机制保留
    with col1:
        if photos_list:
            try:
                st.image(random.choice(photos_list), use_column_width=True)
            except Exception:
                pass
    with col2:
        if music_list:
            try:
                st.audio(random.choice(music_list))
            except Exception:
                pass
        if videos_list:
            try:
                st.video(random.choice(videos_list))
            except Exception:
                pass
    
    if st.button("再读一轮", use_container_width=True):
        st.session_state.page = "timer"; st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)