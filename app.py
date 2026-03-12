import streamlit as st
import base64
import os
import random

# --- 1. 页面配置与初始化 ---
st.set_page_config(page_title="MIMI Reading Room", layout="wide", initial_sidebar_state="collapsed")

if "page" not in st.session_state: st.session_state.page = "landing"
if "round_count" not in st.session_state: st.session_state.round_count = 1

# --- 2. 资源加载函数 ---
@st.cache_data
def get_base64(path):
    try:
        if path and os.path.exists(path):
            with open(path, "rb") as f:
                return base64.b64encode(f.read()).decode()
    except: pass
    return ""

def get_files(directory, exts):
    if not os.path.exists(directory): return []
    return [os.path.join(directory, f) for f in os.listdir(directory) if f.split('.')[-1].lower() in exts]

# 加载核心素材
bg_base64 = get_base64("assets/my_card.jpg")
head_base64 = get_base64("assets/mimi_head.png")
walk_base64 = get_base64("assets/mimi_walk.png")
bgm_base64 = get_base64("assets/bg_music.mp3")

# --- 3. 手机端跳转监听 ---
if st.query_params.get("finish") == "true":
    st.session_state.page = "reward"
    st.query_params.clear() 
    st.rerun()

# --- 4. CSS 样式 (完全恢复大气风格，增加气泡样式) ---
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
        padding-top: 20px !important;
        display: flex !important; flex-direction: column !important; align-items: center !important;
    }}
    /* 白色 Banner */
    .mimi-banner {{
        background: #fff; color: #1b4332; width: 92%; max-width: 820px;
        padding: 20px 0; border-radius: 60px;
        font-family: 'ZCOOL KuaiLe', cursive; font-size: clamp(24px, 5vw, 48px);
        font-weight: 900; text-align: center; margin: -20px auto 10px auto;
        letter-spacing: 4px; border: 1px solid #eee;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        z-index: 10; position: relative;
    }}
    /* 咪咪气泡文案样式 */
    .speech-bubble {{
        position: relative; background: #ffffff; border: 3px solid #1b4332;
        border-radius: 20px; padding: 10px 20px; margin: 5px 0 20px 0;
        font-family: 'ZCOOL KuaiLe'; font-size: 20px; color: #1b4332;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }}
    .speech-bubble:after {{
        content: ''; position: absolute; top: -15px; left: 50%; transform: translateX(-50%);
        border-width: 0 15px 15px; border-style: solid; border-color: #1b4332 transparent;
        display: block; width: 0;
    }}
    div.stButton > button {{
        background-color: #1b4332 !important; color: white !important;
        border-radius: 40px !important; font-family: 'ZCOOL KuaiLe' !important;
        font-weight: 800 !important; font-size: 22px !important;
        width: 100% !important; height: 65px !important;
        border: 2px solid white !important;
    }}
</style>
""", unsafe_allow_html=True)

# 顶部渲染
st.markdown(f'<div style="text-align:center; z-index:20; position:relative;"><img src="data:image/png;base64,{head_base64}" style="width:150px; height:150px; border-radius:50%; border:6px solid white; object-fit: cover;"></div>', unsafe_allow_html=True)
st.markdown('<div class="mimi-banner">MIMI IS WATCHING YOU</div>', unsafe_allow_html=True)

# 随机气泡文案显示
if st.session_state.page != "landing":
    bubbles = ["咪在睡觉 💤", "咪在看你 👀", "咪饿了 🦴", "专注！咪命令你", "再等一会就有惊喜 ✨"]
    selected_bubble = random.choice(bubbles)
    st.markdown(f'<div class="speech-bubble">{selected_bubble}</div>', unsafe_allow_html=True)

# --- 5. 页面路由 ---

if st.session_state.page == "landing":
    st.markdown('<div style="height: 30px;"></div>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    with col2:
        if st.button("咪来了", use_container_width=True): 
            st.session_state.page = "timer"; st.rerun()
    with col3:
        if st.button("咪走了", use_container_width=True): st.stop()

elif st.session_state.page == "timer":
    v_list = get_files("videos", ['mp4', 'mov'])
    video_uri = f"data:video/mp4;base64,{get_base64(random.choice(v_list))}" if v_list else ""

    st.components.v1.html(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=ZCOOL+KuaiLe&display=swap');
        body {{ font-family: 'ZCOOL KuaiLe', sans-serif; margin: 0; background: transparent; overflow: hidden; }}
        .container {{ background: #fff; border-radius: 35px; border: 1px solid #eee; padding: 20px; width: 90%; max-width: 800px; margin: 10px auto; position: relative; box-shadow: 0 10px 40px rgba(0,0,0,0.08); }}
        .bar-bg {{ width: 100%; height: 75px; background: #f1f8e9; border-radius: 50px; position: relative; border-bottom: 6px solid #6a994e; display: flex; align-items: center; overflow: visible; }}
        .decorations {{ position: absolute; width: 85%; left: 5%; display: flex; justify-content: space-between; font-size: 18px; bottom: 8px; opacity: 0.6; }}
        .walker {{ position: absolute; bottom: 8px; left: 0%; transition: left 1s linear; z-index: 90; }}
        .walker img {{ height: 60px; }}
        .timer-text {{ font-size: 60px; font-weight: 900; color: #1b4332; text-align: right; font-family: 'Courier New', monospace; margin: 10px 10px 5px 0; }}
        #duck-btn {{ position: absolute; top: 15px; right: 20px; font-size: 28px; background: none; border: none; cursor: pointer; z-index: 100; }}
        .mimi-btn {{ background: #1b4332; color: white; border: none; padding: 12px 30px; border-radius: 35px; font-family: 'ZCOOL KuaiLe'; font-size: 18px; cursor: pointer; margin: 8px 0; }}
        #mimi-video {{ width: 100%; height: auto; max-height: 380px; border-radius: 15px; background: #000; object-fit: contain; }}
    </style>

    <audio id="bgm" autoplay loop><source src="data:audio/mp3;base64,{bgm_base64}" type="audio/mpeg"></audio>

    <div class="container">
        <button id="duck-btn" onclick="toggleMute()">🦆</button>
        <div id="main-view">
            <div class="bar-bg">
                <div class="decorations"><span>🌸</span><span>🌿</span><span>🌼</span><span>🌻</span><span>🌾</span></div>
                <div class="walker" id="walker"><img src="data:image/png;base64,{walk_base64}"></div>
                <div style="position: absolute; right: 15px; font-size: 35px;">🦴</div>
            </div>
            <div id="timer-val" class="timer-text">30:00</div>
        </div>

        <div id="interact-view" style="display:none; flex-direction:column; align-items:center;">
            <div id="check-title" style="color: #FFD700; -webkit-text-stroke: 1.2px #1b4332; font-size: 24px; margin-bottom: 10px; font-weight:900;">🐾 咪咪突击检查！</div>
            <div id="btn-group" style="display:flex; flex-direction:column; align-items:center;">
                <button class="mimi-btn" onclick="watchMimi()">休息看咪</button>
                <button class="mimi-btn" onclick="backToRead()">回去读书</button>
            </div>
            <div id="video-area" style="display:none; width:100%; text-align:center;">
                <video id="mimi-video" controls playsinline><source src="{video_uri}" type="video/mp4"></video><br>
                <button class="mimi-btn" onclick="backToRead()" style="margin-top:10px;">← 返回读书</button>
            </div>
        </div>
        
        <div id="finish-view" style="display:none; text-align:center;">
            <button class="mimi-btn" style="background:#FFD700; color:#1b4332; font-size:24px; padding:15px 45px;" onclick="triggerFinish()">🎁 领取奖励</button>
        </div>
    </div>

    <script>
        var audio = document.getElementById("bgm"); audio.volume = 0.3;
        var video = document.getElementById("mimi-video");
        function toggleMute() {{ 
            if (audio.muted) {{ audio.muted = false; audio.play(); document.getElementById('duck-btn').innerText = "🦆"; }}
            else {{ audio.muted = true; audio.pause(); document.getElementById('duck-btn').innerText = "🔇"; }}
        }}

        function triggerFinish() {{ window.parent.location.href = window.parent.location.origin + window.parent.location.pathname + "?finish=true"; }}

        var total = 1800; // 正式 30分钟
        var isPaused = false;

        function watchMimi() {{ 
            document.getElementById('check-title').style.display='none';
            document.getElementById('btn-group').style.display='none'; 
            document.getElementById('video-area').style.display='block'; 
            video.play(); 
        }}

        function backToRead() {{ 
            isPaused = false; video.pause();
            document.getElementById('interact-view').style.display='none'; 
            document.getElementById('main-view').style.display='block'; 
        }}

        var clock = setInterval(function() {{
            if (isPaused) return;
            total--;
            var m = Math.floor(total / 60); var s = total % 60;
            document.getElementById('timer-val').innerText = (m < 10 ? "0"+m : m) + ":" + (s < 10 ? "0"+s : s);
            document.getElementById('walker').style.left = ((1800 - total) / 1800 * 84) + "%";
            
            if (total == 900) {{ // 15分钟突击检查
                isPaused = true; 
                document.getElementById('main-view').style.display = 'none'; 
                document.getElementById('interact-view').style.display = 'flex'; 
            }}

            if (total <= 0) {{
                clearInterval(clock);
                document.getElementById('main-view').style.display = 'none';
                document.getElementById('interact-view').style.display = 'none';
                document.getElementById('finish-view').style.display = 'block';
                triggerFinish();
            }}
        }}, 1000);
    </script>
    """, height=650)

elif st.session_state.page == "reward":
    st.balloons()
    st.markdown("<div style='background:#fff; padding:30px; border-radius:35px; border:1px solid #eee; text-align:center; width: 92%; max-width: 850px; margin: 0 auto; box-shadow: 0 12px 45px rgba(0,0,0,0.08);'>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='font-family:ZCOOL KuaiLe; color:#FFD700; font-size:38px; -webkit-text-stroke:1.2px #1b4332;'>🎊 读书完成！</h1>", unsafe_allow_html=True)
    
    cur_round = st.session_state.round_count
    # 奖励配置：第一轮(1,1,1), 第二轮(2,3,2), 第三轮+(3,4,3)
    if cur_round == 1: n_p, n_v, n_m = 1, 1, 1
    elif cur_round == 2: n_p, n_v, n_m = 2, 3, 2
    else: n_p, n_v, n_m = 3, 4, 3

    p_pool = get_files("photos", ['jpg', 'png', 'jpeg'])
    v_pool = get_files("videos", ['mp4', 'mov'])
    m_pool = get_files("music", ['mp3', 'wav'])

    # 抽取奖励
    selected_p = random.sample(p_pool, min(n_p, len(p_pool)))
    selected_v = random.sample(v_pool, min(n_v, len(v_pool)))
    selected_m = random.sample(m_pool, min(n_m, len(m_pool)))

    st.markdown(f"#### 第 {cur_round} 轮：这是咪给你的专属奖励")
    
    # 按照照片、视频、音频顺序排列显示
    for p in selected_p: st.image(p, use_column_width=True)
    
    c_v, c_m = st.columns(2)
    with c_v:
        for v in selected_v: st.video(v)
    with c_m:
        for m in selected_m: st.audio(m)
        
    st.markdown("<div style='height:30px;'></div>", unsafe_allow_html=True)
    if st.button("人还能学", use_container_width=True):
        st.session_state.round_count += 1
        st.session_state.page = "timer"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)