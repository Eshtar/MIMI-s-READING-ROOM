import streamlit as st
import time
import os
import base64
import random

# --- 1. 配置与资源 ---
st.set_page_config(page_title="Mimi Reading Room", layout="centered")

# 精准去水印与去控件 CSS
st.markdown("""
<style>
    header, footer, .stDeployButton, #MainMenu { visibility: hidden !important; height: 0px !important; }
    [data-testid="stViewerBadge"] { display: none !important; }
    div[class*="viewerBadge"] { display: none !important; }
    .stAppViewMain { padding-bottom: 0px !important; }
</style>
""", unsafe_allow_html=True)

# 【优化处：添加缓存装饰器，防止重复读取硬盘和重复编码导致卡顿】
@st.cache_data
def get_base64_file(file_path):
    try:
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                return base64.b64encode(f.read()).decode()
    except: pass
    return None

def get_random_from_dir(directory):
    try:
        if os.path.exists(directory):
            files = [f for f in os.listdir(directory) if not f.startswith('.')]
            if files:
                choice = random.choice(files)
                # 随机文件的 Base64 转换不需要缓存，因为每次都要随机，但基础资源必须缓存
                with open(os.path.join(directory, choice), 'rb') as f:
                    return base64.b64encode(f.read()).decode()
    except: pass
    return None

# 加载基础资源 (现在这些只会运行一次，极大提升 rerun 速度)
BG_IMG = get_base64_file("my_card.jpg")
MIMI_HEAD = get_base64_file("mimi_head.png")
MIMI_WALK = get_base64_file("mimi_walk.png")
BG_MUSIC_B64 = get_base64_file("bg_music.mp3") 

VIDEO_DIR = "videos"
PHOTO_DIR = "photos"
MUSIC_DIR = "music"

# --- 2. 状态初始化 ---
if 'ambient_on' not in st.session_state: st.session_state.ambient_on = False
if 'start_time' not in st.session_state: st.session_state.start_time = None
if 'cycle_count' not in st.session_state: st.session_state.cycle_count = 0 
if 'show_mode' not in st.session_state: st.session_state.show_mode = 'idle'
if 'v_trigger_test' not in st.session_state: st.session_state.v_trigger_test = False 
if 'reward_content' not in st.session_state: st.session_state.reward_content = {}
if 'choice_made' not in st.session_state: st.session_state.choice_made = None
if 'muted' not in st.session_state: st.session_state.muted = False 

FOCUS_INTERACT_SEC = 900
FOCUS_TOTAL_SEC = 1800

# --- 3. CSS 样式 ---
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@500&family=ZCOOL+KuaiLe&display=swap');
    .stApp {{ background-color: transparent !important; }}
    .mountain-breath {{
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: -999;
        background-image: url("data:image/jpeg;base64,{BG_IMG}") !important;
        background-size: cover; background-position: center;
        animation: mountain-haze 8s ease-in-out infinite;
    }}
    @keyframes mountain-haze {{ 0%, 100% {{ filter: brightness(0.2) blur(8px); }} 50% {{ filter: brightness(0.28) blur(6px); }} }}
    .mimi-slogan {{ color: #9cad9c; font-family: 'Noto Serif SC', serif; font-size: 1.85rem; letter-spacing: 0.2em; margin: 25px 0; text-align: center; }}
    div.stButton > button {{
        background: rgba(255, 255, 255, 0.03) !important; 
        color: #9cad9c !important; 
        border-radius: 20px !important;
        border: 1px solid rgba(156, 173, 156, 0.2) !important;
        font-family: 'ZCOOL KuaiLe', sans-serif !important;
        box-shadow: none !important; outline: none !important;
    }}
    div.stButton > button:hover {{ border-color: #436b43 !important; color: #c2a64d !important; }}
    .grass-track {{
        width: 100%; height: 26px; background: rgba(15, 20, 15, 0.7);
        border-radius: 20px; position: relative; margin: 110px 0 50px 0;
        border: 1px solid rgba(156, 173, 156, 0.15);
    }}
</style>
<div class="mountain-breath"></div>
""", unsafe_allow_html=True)

# --- 4. 背景音乐逻辑 ---
if st.session_state.ambient_on and not st.session_state.muted and st.session_state.show_mode != 'video':
    if BG_MUSIC_B64:
        st.markdown(f'<audio autoplay loop><source src="data:audio/mp3;base64,{BG_MUSIC_B64}" type="audio/mp3"></audio>', unsafe_allow_html=True)

# --- 5. 逻辑引擎 ---
if st.session_state.ambient_on:
    elapsed = int(time.time() - st.session_state.start_time)
    remaining = max(0, FOCUS_TOTAL_SEC - elapsed)
    if elapsed >= FOCUS_INTERACT_SEC and not st.session_state.v_trigger_test:
        st.session_state.show_mode = 'choice'
        st.session_state.v_trigger_test = True
        st.rerun()
    if remaining <= 0:
        st.session_state.ambient_on = False
        st.session_state.cycle_count += 1
        st.session_state.reward_content['music'] = get_random_from_dir(MUSIC_DIR)
        st.session_state.reward_content['photo'] = get_random_from_dir(PHOTO_DIR)
        st.session_state.show_mode = 'selection'
        st.rerun()

# --- 6. 渲染层 ---
if st.session_state.show_mode == 'choice':
    st.markdown('<p class="mimi-slogan">咪在看你，你也要看咪吗？</p>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("（A）看咪", use_container_width=True):
            st.session_state.reward_content['video'] = get_random_from_dir(VIDEO_DIR)
            st.session_state.choice_made, st.session_state.show_mode = 'A', 'video'
            st.rerun()
    with c2:
        if st.button("（B）看书", use_container_width=True):
            st.session_state.choice_made, st.session_state.show_mode = 'timing'
            st.rerun()

elif st.session_state.show_mode == 'video':
    v_base = st.session_state.reward_content.get('video')
    if v_base: st.video(f"data:video/mp4;base64,{v_base}")
    if st.button("✕ 关闭视频，继续专注"):
        st.session_state.show_mode = 'timing'
        st.rerun()

elif st.session_state.show_mode == 'selection':
    if st.session_state.choice_made == 'B':
        video_b = get_random_from_dir(VIDEO_DIR)
        if video_b: st.video(f"data:video/mp4;base64,{video_b}")
    st.balloons()
    st.markdown('<p class="mimi-slogan">专注达成</p>', unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        p_data = st.session_state.reward_content.get('photo')
        if p_data: st.image(f"data:image/jpeg;base64,{p_data}", caption="咪的照片奖励")
    with col_b:
        st.write(f"今日已累计: {st.session_state.cycle_count} 轮")
        m_reward = st.session_state.reward_content.get('music')
        if m_reward: 
            st.write("🎵 奖励音乐：")
            st.audio(f"data:audio/mp3;base64,{m_reward}")
    st.markdown("---")
    res1, res2 = st.columns(2)
    with res1:
        if st.button("人还能再读", use_container_width=True):
            st.session_state.ambient_on, st.session_state.start_time = True, time.time()
            st.session_state.v_trigger_test, st.session_state.show_mode = False, 'timing'
            st.session_state.choice_made = None
            st.rerun()
    with res2:
        if st.button("人要休息了", use_container_width=True):
            st.session_state.ambient_on, st.session_state.show_mode = False, 'idle'
            st.rerun()

elif st.session_state.ambient_on and st.session_state.show_mode == 'timing':
    cm1, _ = st.columns([1, 10])
    with cm1:
        if st.button("🔇" if st.session_state.muted else "🔊"):
            st.session_state.muted = not st.session_state.muted
            st.rerun()
    st.markdown(f'<div style="text-align: center;"><img src="data:image/png;base64,{MIMI_HEAD}" style="width:52px; opacity:0.65;"><p class="mimi-slogan">MIMI IS WATCHING YOU</p></div>', unsafe_allow_html=True)
    elapsed = int(time.time() - st.session_state.start_time)
    remaining = max(0, FOCUS_TOTAL_SEC - elapsed)
    mins, secs = divmod(remaining, 60)
    mimi_pos = min(1.0, elapsed / FOCUS_TOTAL_SEC) * 88
    st.markdown(f"""
        <div class="grass-track">
            <div style="position:absolute; left:0; top:0; height:100%; width:{mimi_pos+5}%; background:linear-gradient(90deg, #2d4f2d 0%, #436b43 100%); border-radius:20px;"></div>
            <div style="position:absolute; top:-65px; left:{mimi_pos}%; width:70px; height:70px; transform:scaleX(-1);">
                <img src="data:image/png;base64,{MIMI_WALK}" style="width:70px; height:70px; object-fit:contain;">
            </div>
            <div style="position:relative; z-index:5; color:#c2a64d; font-family:monospace; text-align:center; line-height:26px;">{mins:02d}:{secs:02d}</div>
        </div>
    """, unsafe_allow_html=True)
    if st.button("人要休息了", use_container_width=True):
        st.session_state.ambient_on, st.session_state.show_mode = False, 'idle'
        st.rerun()
    time.sleep(1)
    st.rerun()
else:
    st.markdown(f'<div style="text-align: center; padding-top: 40px;"><img src="data:image/png;base64,{MIMI_HEAD}" style="width:52px; opacity:0.65;"><p class="mimi-slogan">MIMI IS WATCHING YOU</p></div>', unsafe_allow_html=True)
    if st.button("和咪一起读", use_container_width=True):
        st.session_state.ambient_on, st.session_state.start_time = True, time.time()
        st.session_state.v_trigger_test, st.session_state.show_mode = False, 'timing'
        st.rerun()