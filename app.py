import streamlit as st
import time
import random
import os

# 1. 基础配置：设置网页标题和图标
st.set_page_config(page_title="MIMI's Reading Room", page_icon="🐾", layout="centered")

# 2. 强效去水印 CSS：隐藏红色纸船、菜单栏和顶部线条
hide_st_style = """
            <style>
            /* 隐藏顶部导航和装饰线 */
            header {visibility: hidden; height: 0px !important;}
            [data-testid="stHeader"] {display: none !important;}
            
            /* 隐藏底部水印和红色的 Viewer Badge (纸船) */
            footer {visibility: hidden;}
            [data-testid="stViewerBadge"] {display: none !important;}
            div[class*="viewerBadge"] {display: none !important;}
            
            /* 隐藏右下角菜单按钮 */
            #MainMenu {visibility: hidden;}
            
            /* 优化整体布局空间 */
            .main .block-container {
                padding-top: 2rem;
                padding-bottom: 0rem;
            }
            
            /* 按钮样式美化 */
            .stButton>button {
                width: 100%;
                border-radius: 20px;
                border: 1px solid #ddd;
                background-color: transparent;
                transition: all 0.3s;
            }
            .stButton>button:hover {
                border-color: #999;
                background-color: #f9f9f9;
            }
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# 3. 初始化会话状态 (Session State)
if 'phase' not in st.session_state:
    st.session_state.phase = 'start'  # start, phase1, choice, phase2, reward

# 4. 辅助函数：随机获取文件
def get_random_file(folder):
    files = [f for f in os.listdir(folder) if not f.startswith('.')]
    return os.path.join(folder, random.choice(files)) if files else None

# --- 页面逻辑开始 ---

# A. 初始界面
if st.session_state.phase == 'start':
    st.image("my_card.jpg", use_column_width=True)
    st.title("MIMI's Reading Room")
    st.write("“在山间的呼吸中，和咪一起专注 30 分钟。”")
    
    if st.button("开始专注"):
        st.session_state.phase = 'phase1'
        st.rerun()

# B. 第一阶段：前 15 分钟
elif st.session_state.phase == 'phase1':
    st.image("mimi_walk.png", width=100)
    st.subheader("第一阶段：深度阅读中...")
    st.audio("bg_music.mp3", format="audio/mp3", loop=True)
    
    progress_bar = st.progress(0)
    # 模拟 15 分钟 (900秒)
    status_text = st.empty()
    for i in range(100):
        time.sleep(9) # 9秒 * 100 = 900秒 (15min)
        progress_bar.progress(i + 1)
        status_text.text(f"已专注 {int((i+1)*0.15)} 分钟...")
    
    st.session_state.phase = 'choice'
    st.rerun()

# C. 15 分钟转折点：A/B 选择
elif st.session_state.phase == 'choice':
    st.image("mimi_head.png", width=150)
    st.title("咪来查岗了！")
    st.write("你已经坚持了 15 分钟，现在的选择是：")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("看一会儿咪 (休息)"):
            st.session_state.choice = 'video'
            st.session_state.phase = 'phase2'
            st.rerun()
    with col2:
        if st.button("继续努力工作"):
            st.session_state.choice = 'keep_going'
            st.session_state.phase = 'phase2'
            st.rerun()

# D. 第二阶段：后 15 分钟
elif st.session_state.phase == 'phase2':
    if st.session_state.choice == 'video':
        video_file = get_random_file("videos")
        if video_file:
            st.video(video_file)
    else:
        st.info("咪在门缝里偷偷看你，加油，还有 15 分钟！")
        st.image("mimi_walk.png", width=100)
    
    st.audio("bg_music.mp3", format="audio/mp3", loop=True)
    progress_bar = st.progress(0)
    # 模拟第二个 15 分钟
    for i in range(100):
        time.sleep(9)
        progress_bar.progress(i + 1)
    
    st.session_state.phase = 'reward'
    st.rerun()

# E. 最终奖励界面
elif st.session_state.phase == 'reward':
    st.balloons()
    st.title("🏆 专注达成！")
    st.write("这是给你的专属奖励：")
    
    # 随机展示一张照片
    photo_file = get_random_file("photos")
    if photo_file:
        st.image(photo_file, caption="今日份的惊喜")
    
    # 随机播放一段奖励音乐
    reward_music = get_random_file("music")
    if reward_music:
        st.write("🎧 奖励曲目播放中...")
        st.audio(reward_music, format="audio/mp3")
    
    if st.button("再次开启专注"):
        st.session_state.phase = 'start'
        st.rerun()