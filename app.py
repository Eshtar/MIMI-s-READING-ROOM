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

# --- 3. 核心逻辑：监听组件发回的结束信号 ---
# 如果 URL 参数里出现了 finish=true，说明计时器跑完了
if st.query_params.get("finish") == "true":
    st.session_state.page = "reward"
    st.query_params.clear() # 清除参数防止死循环
    st.rerun()

if "page" not in st.session_state: st.session_state.page = "landing"

# --- 4. CSS 样式 ---
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
        padding-top: 10px !important;
        display: flex !important; flex-direction: column !important; align-items: center !important;
    }}
    .mimi-banner {{
        background: #fff; color: #1b4332; width: 95%; max-width: 800px;
        padding: 10px 0; border-radius: 50px;
        font-family: 'ZCOOL KuaiLe', cursive; font-size: clamp(16px, 4.5vw, 32px);
        font-weight: 900; text-align: center; margin: 5px auto 10px auto;
        border: 1px solid #eee; box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }}
    div.stButton > button {{
        background-color: #1b4332 !important; color: white !important;
        border-radius: 40px !important; font-family: 'ZCOOL KuaiLe' !important;
        height: 55px !important; border: 2px solid white !important;
    }}
</style>
""", unsafe_allow_html=True)

# 修复头像显示逻辑
if head_base64:
    st.markdown(f'<div style="text-align:center;"><img src="data:image/png;base64,{head_base64}" style="width:100px; height:100px; border-radius:50%; border:4px solid white; object-fit:cover;"></div>', unsafe_allow_html=True)
st.markdown('<div class="mimi-banner">MIMI IS WATCHING YOU</div>', unsafe_allow_html=True)

# --- 5. 页面路由 ---

if st.session_state.page == "landing":
    col1, col2 = st.columns(2)
    with col1:
        if st.button("咪来了", use_container_width=True): 
            st.session_state.page = "timer"; st.rerun()
    with col2:
        if st.button("咪走了", use_container_width=True): st.stop()

elif st.session_state.page == "timer":
    selected_video = random.choice(videos_list) if videos_list else None
    video_uri = f"data:video/mp4;base64,{get_base64(selected_video)}" if selected_video else ""

    # 手机端终极 HTML 组件
    st.components.v1.html(f"""
    <div id="mimi-container">
        <style>
            @import url('https://fonts.googleapis.com/css2?family=ZCOOL+KuaiLe&display=swap');
            body {{ font-family: 'ZCOOL KuaiLe', sans-serif; margin: 0; background: transparent; overflow: hidden; }}
            .card {{ background: #fff; border-radius: 25px; padding: 15px; width: 92%; margin: 5px auto; box-shadow: 0 5px 20px rgba(0,0,0,0.1); text-align: center; }}
            .track {{ width: 100%; height: 50px; background: #f1f8e9; border-radius: 30px; position: relative; border-bottom: 4px solid #6a994e; margin-top: 10px; overflow: visible; display: flex; align-items: center; }}
            .items {{ position: absolute; width: 88%; left: 6%; display: flex; justify-content: space-between; font-size: 14px; opacity: 0.5; }}
            .mimi-walker {{ position: absolute; bottom: 5px; left: 0%; transition: left 1s linear; z-index: 10; }}
            .mimi-walker img {{ height: 45px; }}
            .time-display {{ font-size: 55px; font-weight: 900; color: #1b4332; text-align: right; margin: 10px 15px 5px 0; font-family: monospace; letter-spacing: -2px; }}
            .mimi-btn {{ background: #1b4332; color: white; border: none; padding: 10px 25px; border-radius: 30px; font-family: 'ZCOOL KuaiLe'; font-size: 16px; margin: 5px; }}
            #mimi-video {{ width: 100%; max-height: 250px; border-radius: 10px; background: #000; margin-top: 5px; }}
        </style>

        <audio id="bgm" autoplay loop><source src="data:audio/mp3;base64,{bgm_base64}" type="audio/mpeg"></audio>

        <div class="card">
            <div id="view-normal">
                <div class="track">
                    <div class="items"><span>🌸</span><span>🌿</span><span>🌼</span><span>🌻</span><span>🌾</span></div>
                    <div class="mimi-walker" id="walker"><img src="data:image/png;base64,{walk_base64}"></div>
                    <div style="position: absolute; right: 10px; font-size: 20px;">🦴</div>
                </div>
                <div id="timer-text" class="time-display">01:00</div>
            </div>

            <div id="view-check" style="display:none; flex-direction:column; align-items:center;">
                <div style="color:#FFD700; font-size:20px; font-weight:900; margin-bottom:5px;">🐾 咪咪突击检查！</div>
                <div id="check-btns">
                    <button class="mimi-btn" onclick="goVideo()">休息看咪</button>
                    <button class="mimi-btn" onclick="goBack()">回去读书</button>
                </div>
                <div id="video-area" style="display:none;">
                    <video id="v-play" controls playsinline><source src="{video_uri}" type="video/mp4"></video><br>
                    <button class="mimi-btn" onclick="goBack()">← 返回读书</button>
                </div>
            </div>
        </div>
    </div>

    <script>
        var timeLeft = 60;
        var paused = false;
        var video = document.getElementById('v-play');

        function goVideo() {{ 
            document.getElementById('check-btns').style.display='none';
            document.getElementById('video-area').style.display='block';
            video.play();
        }}
        function goBack() {{ 
            video.pause(); paused = false;
            document.getElementById('view-check').style.display='none';
            document.getElementById('view-normal').style.display='block';
        }}
        video.onended = goBack;

        var clock = setInterval(function() {{
            if (paused) return;
            timeLeft--;
            
            // 修复补零逻辑，防止乱码
            var m = Math.floor(timeLeft / 60);
            var s = timeLeft % 60;
            document.getElementById('timer-text').innerText = (m < 10 ? "0"+m : m) + ":" + (s < 10 ? "0"+s : s);
            document.getElementById('walker').style.left = ((60 - timeLeft) / 60 * 85) + "%";

            if (timeLeft == 30) {{
                paused = true;
                document.getElementById('view-normal').style.display='none';
                document.getElementById('view-check').style.display='flex';
            }}

            if (timeLeft <= 0) {{
                clearInterval(clock);
                // 终极跳转：修改父窗口 URL 参数触发 Streamlit 后端 rerun
                window.parent.location.href = window.parent.location.origin + window.parent.location.pathname + "?finish=true";
            }}
        }}, 1000);
    </script>
    """, height=420)

elif st.session_state.page == "reward":
    st.balloons()
    st.markdown("<div style='background:#fff; padding:20px; border-radius:30px; text-align:center; width:95%; margin:0 auto; box-shadow:0 5px 20px rgba(0,0,0,0.1);'>", unsafe_allow_html=True)
    st.markdown("<h2 style='font-family:ZCOOL KuaiLe; color:#FFD700;'>🎊 读书完成！</h2>", unsafe_allow_html=True)
    
    if photos_list: st.image(random.choice(photos_list), use_column_width=True)
    
    col_a, col_v = st.columns(2)
    with col_a:
        if music_list: st.audio(random.choice(music_list))
    with col_v:
        if videos_list: st.video(random.choice(videos_list))
        
    if st.button("再读一轮", use_container_width=True):
        st.session_state.page = "timer"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)