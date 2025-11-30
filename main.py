import pygame
import sys
import os
import math 
import random
import time

# 初始化 Pygame
pygame.init()
pygame.mixer.init() # 初始化混音器

# ==========================================
# 1. 资源配置区
# ==========================================

# --- 窗口设置 ---
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# --- 颜色定义 ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LOW_SAT_WHITE = WHITE
LOW_SAT_RED = (200, 50, 50)
DAMAGE_FILLED_COLOR = (120, 120, 120) # 灰色，用于血条扣除后的背景

# 新增颜色配置
TEXT_COLOR = (248, 224, 171)     # f8e0ab
BOX_COLOR = (84, 68, 52)         # 544434
TEXT_OUTLINE_COLOR = (0, 0, 0)   # 黑色描边
LEVEL_TITLE_OUTLINE = (84, 68, 52) # 关卡标题描边

# --- 字体路径 ---
FONT_PATH = "StoryScript-Regular.ttf" 

# --- 图片路径清单 ---
IMG_PATHS = {
    # 开场动画 (Steps 1-8)
    "1": "images/opening/op1.png",
    "2-1": "images/opening/op2-1.png",
    "2-2": "images/opening/op2-2.png",
    "3-1": "images/opening/op3-1.png",
    "3-2": "images/opening/op3-2.png",
    "4": "images/opening/op4.png",
    "5-1": "images/opening/op5-1.png",
    "5-2": "images/opening/op5-2.png",
    "5-3": "images/opening/op5-3.png",
    "5-4": "images/opening/op5-4.png",
    "5-5": "images/opening/op5-5.png",
    
    # 教学部分 (Steps 9-11)
    "t-1": "images/base.png",
    "t-l": "images/arm_l.png", 
    "t-r": "images/arm_r.png", 
    "t-f": "images/level1sunny/1.png", 
    "t-m": "images/tutorial/mouse.png",  
    "t-a": "images/tutorial/arrow.png",  
    "t-sunny": "images/level1sunny/cover_sunny.png", 
    "t-rainy": "images/level2rainy/cover_rain.png", 
    "t-raindrop": "images/raindrop.png", 
    
    # 第一关新增图片
    "1-sunny": "images/level1sunny/sunny.png",
    "1-rainy": "images/level2rainy/rainy.png",
    "1-baselose": "images/base_lose.png",
    "1-f-l": "images/level1sunny/1_f.png",
    "2-f": "images/level2rainy/2.png",
    
    # 第二关新增图片
    "1-sourrain": "images/level3sourrain/sourrain.png",
    "2-f-l": "images/level2rainy/2_f.png",
    "3-f": "images/level3sourrain/3.png",
    "sourraindrop": "images/sourraindrop.png",

    # 第三关 & 结局新增图片
    "birdshit": "images/birdshit.png",
    "3-f-l": "images/level3sourrain/3_f.png",
    "E-1": "images/ending/happy.png",
    "E-2": "images/ending/ending.png",

    # UI 图标 (新增)
    "icon_sun": "images/sun.png",
    "icon_drop": "images/drop.png",
    "icon_heart": "images/heart.png"
}

# --- 音效路径清单 ---
SOUND_PATHS = {
    "pic1": "music/pic1.mp3",
    "pic2": "music/pic2.mp3",
    "bgm": "music/bgm.mp3",
    "click": "music/click.mp3",
    "countbackward": "music/countbackward.mp3",
    "drop": "music/drop.mp3",
    "water": "music/water.mp3",
    "ending": "music/ending.mp3",
    "fail": "music/fail.mp3",
    "pass": "music/pass.mp3",
    "rainy": "music/rainy.mp3",
    "shit": "music/bird.mp3",
    "sourrain": "music/sourrain.mp3"
}

# --- 教学互动常量 ---
MAX_ARM_SPREAD = 200    
ARM_MOVEMENT_SPEED = 0.5  
MOUSE_MOVE_AMPLITUDE = 50  
MOUSE_MOVE_SPEED = 0.002   
FADE_SPEED = 5 
ARM_CLOSED_THRESHOLD = 50 

SUNLIGHT_REQUIRED = 3.0 
RAIN_PROTECTION_DURATION = 1.0 
RAIN_PHASE_DURATION = 5.0 

RAINDROP_COUNT = 15 
RAINDROP_SPEED_MIN = 3 
RAINDROP_SPEED_MAX = 7 
RAINDROP_SIZE_MIN = 5 
RAINDROP_SIZE_MAX = 15 

# 第一关常量
LEVEL1_SUNLIGHT_REQUIRED = 10.0  
LEVEL1_RAIN_TOLERANCE = 3.0      
LEVEL1_DURATION = 30.0           

# 第二关常量
LEVEL2_SUNLIGHT_REQUIRED = 5.0   
LEVEL2_RAIN_REQUIRED = 5.0       
LEVEL2_SOURRAIN_TOLERANCE = 2.0  
LEVEL2_DURATION = 25.0           

# 第三关常量
LEVEL3_DURATION = 25.0
LEVEL3_SUNLIGHT_REQUIRED = 5.0
LEVEL3_RAIN_REQUIRED = 5.0
LEVEL3_SOURRAIN_TOLERANCE = 1.0 # 小于1秒

# 鸟屎相关常量
BIRD_DROP_SPEED = 10 # 下落速度常量 (intro和gameplay通用)
BIRD_FADE_SPEED = 15 # Intro中鸟屎消失速度
BIRD_CHECK_HEIGHT_RATIO = 0.25 # 判定高度 (1/4屏幕高度) - 可调节常量

# 天气切换常量
WEATHER_MIN_DURATION = 2.0  
WEATHER_MAX_DURATION = 5.0  

# --- 渐变效果常量 ---
FADE_RESTART_SPEED = 10 

# ==========================================
# 2. 系统初始化与资源加载函数
# ==========================================
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game Opening Sequence")
clock = pygame.time.Clock()

try:
    game_font = pygame.font.Font(FONT_PATH, 24)
    ui_big_font = pygame.font.Font(FONT_PATH, 36) # 新增：48号大字体
    level_font = pygame.font.Font(FONT_PATH, 48)
    countdown_font = pygame.font.Font(FONT_PATH, 120) # 倒计时大字体
except:
    print(f"提示: 未找到字体 {FONT_PATH}，使用系统默认字体")
    game_font = pygame.font.Font(None, 24)
    ui_big_font = pygame.font.Font(None, 36) # 新增：默认大字体
    level_font = pygame.font.Font(None, 48)
    countdown_font = pygame.font.Font(None, 120)

def load_img(key, size=None):
    path = IMG_PATHS[key]
    try:
        img = pygame.image.load(path).convert_alpha()
        if size:
            img = pygame.transform.scale(img, size)
    except FileNotFoundError:
        # 默认生成色块逻辑
        if size:
            w, h = size
        else:
            if "icon" in key:
                w, h = 40, 40 # 默认图标大小
            elif "1" in key or "4" in key or "-1" in key or "5-5" in key or key=="t-1" or "E-" in key:
                w, h = SCREEN_WIDTH, SCREEN_HEIGHT
            else:
                w, h = 200, 200
        
        img = pygame.Surface((w, h))
        # 红色或蓝色色块
        color = (50, 50, 150) if "-1" in key or len(key)==1 else (150, 50, 50)
        if "icon_sun" in key: color = (255, 200, 0)
        if "icon_drop" in key: color = (50, 150, 255)
        if "icon_heart" in key: color = (200, 50, 50)
        
        img.fill(color)
        
        if "icon" not in key:
            text = game_font.render(f"IMG {key}", True, WHITE)
            text_rect = text.get_rect(center=(w//2, h//2))
            img.blit(text, text_rect)
    return img

# 加载音效函数
def load_sounds():
    loaded_sounds = {}
    for key, path in SOUND_PATHS.items():
        if key == "bgm":
            # BGM使用music模块加载，这里只检查文件存在性
            if not os.path.exists(path):
                print(f"警告: 音频文件 {path} 未找到")
            continue
        try:
            loaded_sounds[key] = pygame.mixer.Sound(path)
        except FileNotFoundError:
            print(f"警告: 音频文件 {path} 未找到，将静音")
            # 创建一个空声音对象以防报错
            loaded_sounds[key] = pygame.mixer.Sound(buffer=bytearray()) 
    return loaded_sounds

sounds = load_sounds()

def play_bgm():
    if os.path.exists(SOUND_PATHS["bgm"]):
        try:
            pygame.mixer.music.load(SOUND_PATHS["bgm"])
            pygame.mixer.music.play(-1, fade_ms=2000) # 循环播放，2秒淡入
        except:
            pass

def stop_bgm_fadeout():
    pygame.mixer.music.fadeout(2000)

# --------------------------------------------------------------------------
# UI 绘制辅助函数 (修改：增加缓存以解决卡顿)
# --------------------------------------------------------------------------

# 全局文字表面缓存
# Key: (content, style_type)
# Value: Rendered Surface (without alpha)
_text_surface_cache = {}

def get_cached_text_box_surface(content, style, font=None):
    """
    获取缓存的文字框Surface
    增加 font 参数支持自定义字体
    """
    use_font = font if font else game_font

    cache_key = (content, style, use_font)
    if cache_key in _text_surface_cache:
        return _text_surface_cache[cache_key]
    
    # --- 创建新的 Surface ---
    max_text_width = 800 if style == "center_bottom" else 600
    lines = wrap_text(content, use_font, max_text_width)
    
    line_height = use_font.get_height()
    total_text_h = len(lines) * line_height
    total_text_w = 0
    for line in lines:
        w, _ = use_font.size(line)
        total_text_w = max(total_text_w, w)
    
    # === 修改点开始 ===
    # 减小内边距数值 (原为 20 和 15)
    padding_x = 7 
    padding_y = 0
    # === 修改点结束 ===
    
    box_w = total_text_w + padding_x * 2 + 10 
    box_h = total_text_h + padding_y * 2
    
    box_surface = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
    
    bg_rect = pygame.Rect(0, 0, box_w - 10, box_h)
    box_surface.fill(BOX_COLOR, bg_rect)
    
    for i, line in enumerate(lines):
        line_y = padding_y + i * line_height
        line_x = padding_x
        draw_text_with_outline_and_shadow(box_surface, line, use_font, TEXT_COLOR, TEXT_OUTLINE_COLOR, (line_x, line_y), 1)
    
    _text_surface_cache[cache_key] = box_surface
    return box_surface

def draw_text_with_outline_and_shadow(surface, text, font, color, outline_color, pos, outline_width=3):
    """绘制带描边和投影的文字"""
    text_surf = font.render(text, True, color)
    
    # 投影 (Shadow)
    shadow_surf = font.render(text, True, BLACK)
    surface.blit(shadow_surf, (pos[0] + 2, pos[1] + 3))
    
    # 描边 (Outline) - 8方向绘制
    for dx in range(-outline_width, outline_width + 1):
        for dy in range(-outline_width, outline_width + 1):
            if dx != 0 or dy != 0:
                outline_surf = font.render(text, True, outline_color)
                surface.blit(outline_surf, (pos[0] + dx, pos[1] + dy))
    
    # 正常文字
    surface.blit(text_surf, pos)
    return text_surf.get_size()

def wrap_text(text, font, max_width):
    """简单的文字换行处理"""
    words = text.split(' ')
    lines = []
    current_line = []
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        w, h = font.size(test_line)
        if w < max_width:
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
    lines.append(' '.join(current_line))
    return lines

def draw_styled_text_box(content, alpha, style="center_bottom", font=None, offset=(0, 0)):
    """
    绘制带背景框的样式化文字
    新增 font: 指定字体
    新增 offset: (x, y) 坐标偏移量
    """
    if alpha <= 0: return

    # 传递 font 给缓存函数
    box_surface = get_cached_text_box_surface(content, style, font)
    
    box_w = box_surface.get_width()
    box_h = box_surface.get_height()
    
    # 确定绘制位置并应用偏移
    if style == "bottom_left":
        box_x = 40 + offset[0]
        box_y = SCREEN_HEIGHT - box_h - 40 + offset[1]
    else: # center_bottom
        box_x = (SCREEN_WIDTH - box_w) // 2 + offset[0]
        box_y = SCREEN_HEIGHT - box_h - 40 + offset[1] 
    
    box_surface.set_alpha(alpha)
    screen.blit(box_surface, (box_x, box_y))

def draw_level_text(content, alpha):
    """绘制关卡大标题 (Level X)"""
    if alpha <= 0: return
    # 创建临时 surface 以支持透明度
    w, h = level_font.size(content)
    # 留足空间给描边
    surf = pygame.Surface((w + 20, h + 20), pygame.SRCALPHA)
    
    # 修正：颜色强制改为 WHITE
    draw_text_with_outline_and_shadow(surf, content, level_font, WHITE, LEVEL_TITLE_OUTLINE, (10, 10), 3)
    
    surf.set_alpha(alpha)
    rect = surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 180)) # 位置稍微上调避开底部文字框
    screen.blit(surf, rect)

def draw_progress_bar_custom(current, required, alpha, icon_key, x, y, width=350, height=20, is_damage=False):
    """
    绘制带图标的进度条
    x, y: 进度条左上角坐标
    """
    if alpha <= 0: return

    # 绘制图标
    icon = images[icon_key]
    # 图标位置：进度条左侧
    icon_x = x - 50
    icon_y = y + height // 2 - icon.get_height() // 2
    
    # 设置图标透明度
    icon.set_alpha(alpha)
    screen.blit(icon, (icon_x, icon_y))
    
    bar_surf = pygame.Surface((width, height), pygame.SRCALPHA)
    
    if is_damage:
        # --- 血条模式逻辑 ---
        # 1. 绘制全灰背景 (代表已损失的血量/空槽)
        pygame.draw.rect(bar_surf, DAMAGE_FILLED_COLOR, (0, 0, width, height), 0, 5) 
        
        # 2. 计算剩余血量 (红色)
        # current 是 accumulated damage (已受伤害)
        # required 是 tolerance (最大承受伤害)
        damage_ratio = current / required
        remaining_ratio = 1.0 - damage_ratio
        remaining_ratio = max(0.0, min(1.0, remaining_ratio))
        
        red_width = int(width * remaining_ratio)
        
        # 3. 绘制红色条 (靠左对齐，代表剩余生命)
        if red_width > 0:
            pygame.draw.rect(bar_surf, (200, 50, 50), (0, 0, red_width, height), 0, 5)
            
        # 4. 边框
        pygame.draw.rect(bar_surf, (255, 255, 255), (0, 0, width, height), 2, 5)
        
        # 文字时间 (剩余可承受秒数)
        time_left_val = max(0, required - current)
        text_time = f"{time_left_val:.1f}s"
        
    else: # 收集类 (阳光/雨水)
        progress_ratio = current / required
        progress_ratio = min(1.0, progress_ratio)
        fill_width = int(width * progress_ratio)
        
        fill_color = (255, 200, 0) if "sun" in icon_key else (50, 150, 255)
        
        # 背景 (深灰)
        pygame.draw.rect(bar_surf, (70, 70, 70), (0, 0, width, height), 0, 5)
        # 填充
        pygame.draw.rect(bar_surf, fill_color, (0, 0, fill_width, height), 0, 5)
        # 边框
        pygame.draw.rect(bar_surf, (255, 255, 255), (0, 0, width, height), 2, 5)
        
        # 修改：增加 's' 单位
        text_time = f"{current:.1f}s/{required:.0f}s"

    bar_surf.set_alpha(alpha)
    screen.blit(bar_surf, (x, y))

    # 绘制数值文字 (右侧)
    text_surf = game_font.render(text_time, True, WHITE)
    text_surf.set_alpha(alpha)
    screen.blit(text_surf, (x + width + 10, y + height // 2 - text_surf.get_height() // 2))


def draw_game_timer(time_left, alpha):
    text_surf = game_font.render(f"Time: {time_left:.1f}s", True, WHITE)
    text_surf.set_alpha(alpha)
    text_rect = text_surf.get_rect(topright=(SCREEN_WIDTH - 20, 20))
    screen.blit(text_surf, text_rect)

def draw_level_number(level, alpha):
    text_surf = game_font.render(f"Level {level}", True, WHITE)
    text_surf.set_alpha(alpha)
    text_rect = text_surf.get_rect(topleft=(20, 20))
    screen.blit(text_surf, text_rect)

def draw_top_text(content, alpha):
    """专门用于显示在顶部的提示文字 (鸟来了)"""
    draw_styled_text_box(content, alpha, style="center_bottom") # 暂时复用底部样式逻辑，或者单独写

images = {}
GLOBAL_SCALE_FACTOR = 0.5 
all_keys = list(IMG_PATHS.keys())

for key in all_keys:
        img = load_img(key)
        original_width = img.get_width()
        original_height = img.get_height()
        
        # 图标不缩放，其他缩放
        if "icon" in key:
            images[key] = pygame.transform.scale(img, (40, 40))
        else:
            new_width = int(original_width * GLOBAL_SCALE_FACTOR)
            new_height = int(original_height * GLOBAL_SCALE_FACTOR)
            images[key] = pygame.transform.smoothscale(img, (new_width, new_height))
        
        # 如果是鸟屎图片，顺带旋转大约 25 度（逆时针旋转）以匹配斜向右下的轨迹
        if key == "birdshit":
            images[key] = pygame.transform.rotate(images[key], 25)

if "t-f" in images:
    flower_img = images["t-f"]
    original_width = flower_img.get_width()
    original_height = flower_img.get_height()
    
    new_width = int(original_width * (1 + 1/3))
    new_height = int(original_height * (1 + 1/3))
    
    images["t-f"] = pygame.transform.smoothscale(flower_img, (new_width, new_height))
    
    # --- 修复卡顿关键：预先生成 Intro 用的缩放版花朵 ---
    # 在 intro 中会以 2/3 大小显示 t-f (即 "2-f" 等大小)
    # 我们这里提前生成一个 t-f 的缩放副本
    intro_scale_ratio = 2/3
    intro_w = int(images["t-f"].get_width() * intro_scale_ratio)
    intro_h = int(images["t-f"].get_height() * intro_scale_ratio)
    images["t-f-intro-scaled"] = pygame.transform.smoothscale(images["t-f"], (intro_w, intro_h))

# ==========================================
# 3. 游戏状态管理
# ==========================================

step = 1 
timer = 0 
state_start_time = 0 
last_mouse_x = 0 
arm_position_offset = 0 
mouse_anim_offset = 0 
has_slid = False
slide_time = 0

# 新增倒计时相关变量
is_counting_down = False
countdown_start_time = 0

alphas = {k: 0 for k in IMG_PATHS.keys()}
# 初始化所有alpha为0
for k in IMG_PATHS.keys():
    alphas[k] = 0

# 单独添加 level intro text 的 alpha 控制
alphas["text_step1"] = 0 
alphas["prompt_sunlight"] = 0 
alphas["prompt_rain"] = 0 
alphas["prompt_success"] = 0 

# Level 1 Alpha
alphas["level1_text"] = 0
alphas["level1_intro_text"] = 0 # 统一的介绍文字
alphas["level1_number"] = 0
alphas["level1_timer"] = 0

# Level 2 Alpha
alphas["level2_text"] = 0
alphas["level2_intro_text"] = 0 # 统一的介绍文字
alphas["level2_number"] = 0
alphas["level2_timer"] = 0

# Level 3 Alpha
alphas["level3_text"] = 0
alphas["level3_intro_text"] = 0 # 统一的介绍文字
alphas["level3_number"] = 0
alphas["level3_timer"] = 0
alphas["level3_prompt_fail"] = 0
alphas["ending_text_1"] = 0
alphas["ending_text_2"] = 0

# 失败提示单独控制
alphas["prompt_fail_l1"] = 0
alphas["prompt_fail_l2"] = 0

alphas["fade_layer"] = 0 
is_restarting = False

img5_2_offset_y = 0 
is_dropping = False 

sunlight_timer = 0.0 
damage_accumulated = 0.0 
rain_phase_time = 0.0 
raindrops = [] 

# Level 1 Vars
level1_sunlight_collected = 0.0
level1_rain_damage = 0.0
level1_time_left = LEVEL1_DURATION
level1_weather = "sunny" 
level1_weather_timer = 0.0
level1_weather_duration = random.uniform(WEATHER_MIN_DURATION, WEATHER_MAX_DURATION)
level1_game_active = False

# Level 2 Vars
level2_sunlight_collected = 0.0
level2_rain_collected = 0.0
level2_sourrain_damage = 0.0
level2_time_left = LEVEL2_DURATION
level2_weather = "sunny"  
level2_weather_timer = 0.0
level2_weather_duration = random.uniform(WEATHER_MIN_DURATION, WEATHER_MAX_DURATION)
level2_game_active = False
sourraindrops = [] 

# Level 3 Vars
level3_sunlight_collected = 0.0
level3_rain_collected = 0.0
level3_sourrain_damage = 0.0
level3_time_left = LEVEL3_DURATION
level3_weather = "sunny"
level3_weather_timer = 0.0
level3_weather_duration = 5.0 # Initial Sunny fixed 5s
level3_game_active = False
bird_warning_timer = 0.0
bird_warning_duration = 0.0 # 1.0 - 1.5s
bird_active = False
bird_y = 0.0
bird_checked = False
bird_intro_y = 0 # Intro only
bird_intro_active = False # Intro only
bird_intro_state = 0 # 0: text, 1: delay, 2: fall

# New variables for L3 Bird Logic
level3_bird_trigger_time = 0.0
level3_bird_started = False 
level3_bird_finished = False 

# 音频环境管理变量
current_environment_sound = None # 'rainy' or 'sourrain'

def update_environment_sound(weather):
    global current_environment_sound
    
    target_sound = None
    if weather == "rainy":
        target_sound = "rainy"
    elif weather == "sourrain":
        target_sound = "sourrain"
    
    if current_environment_sound != target_sound:
        # 淡出当前声音
        if current_environment_sound == "rainy":
            sounds["rainy"].fadeout(1000)
        elif current_environment_sound == "sourrain":
            sounds["sourrain"].fadeout(1000)
            
        # 淡入新声音
        if target_sound == "rainy":
            sounds["rainy"].play(-1, fade_ms=1000)
        elif target_sound == "sourrain":
            sounds["sourrain"].play(-1, fade_ms=1000)
            
        current_environment_sound = target_sound

def stop_all_environment_sounds():
    global current_environment_sound
    if current_environment_sound == "rainy":
        sounds["rainy"].fadeout(1000)
    elif current_environment_sound == "sourrain":
        sounds["sourrain"].fadeout(1000)
    current_environment_sound = None

def reset_tutorial_state():
    global step, state_start_time, arm_position_offset, mouse_anim_offset, has_slid, slide_time
    global sunlight_timer, damage_accumulated, rain_phase_time, is_restarting, raindrops
    
    step = 9
    state_start_time = pygame.time.get_ticks() 
    
    for k in alphas:
        alphas[k] = 0
        
    alphas["fade_layer"] = 0 
    
    arm_position_offset = 0
    mouse_anim_offset = 0
    has_slid = False
    slide_time = 0
    sunlight_timer = 0.0
    damage_accumulated = 0.0 
    rain_phase_time = 0.0
    is_restarting = False 
    raindrops = []
    stop_all_environment_sounds()

def reset_level1():
    global level1_sunlight_collected, level1_rain_damage, level1_time_left, level1_weather
    global level1_weather_timer, level1_weather_duration, level1_game_active, raindrops
    global is_counting_down
    
    level1_sunlight_collected = 0.0
    level1_rain_damage = 0.0
    level1_time_left = LEVEL1_DURATION
    level1_weather = "sunny"
    level1_weather_timer = 0.0
    level1_weather_duration = random.uniform(WEATHER_MIN_DURATION, WEATHER_MAX_DURATION)
    level1_game_active = False
    is_counting_down = False
    raindrops = []
    stop_all_environment_sounds()

def reset_level2():
    global level2_sunlight_collected, level2_rain_collected, level2_sourrain_damage, level2_time_left
    global level2_weather, level2_weather_timer, level2_weather_duration, level2_game_active
    global raindrops, sourraindrops, is_counting_down
    
    level2_sunlight_collected = 0.0
    level2_rain_collected = 0.0
    level2_sourrain_damage = 0.0
    level2_time_left = LEVEL2_DURATION
    level2_weather = "sunny"
    level2_weather_timer = 0.0
    level2_weather_duration = random.uniform(WEATHER_MIN_DURATION, WEATHER_MAX_DURATION)
    level2_game_active = False
    is_counting_down = False
    raindrops = []
    sourraindrops = []
    stop_all_environment_sounds()

def reset_level3():
    global level3_sunlight_collected, level3_rain_collected, level3_sourrain_damage, level3_time_left
    global level3_weather, level3_weather_timer, level3_weather_duration, level3_game_active
    global raindrops, sourraindrops, bird_active, bird_y, bird_checked, bird_warning_timer
    global level3_bird_finished, is_counting_down
    
    level3_sunlight_collected = 0.0
    level3_rain_collected = 0.0
    level3_sourrain_damage = 0.0
    level3_time_left = LEVEL3_DURATION
    level3_weather = "sunny"
    level3_weather_timer = 0.0
    level3_weather_duration = 6.0 # Initial Sunny fixed 5s
    level3_game_active = False
    is_counting_down = False
    raindrops = []
    sourraindrops = []
    bird_active = False
    bird_y = 0.0
    bird_checked = False
    bird_warning_timer = 0.0
    level3_bird_finished = False 
    stop_all_environment_sounds()

def restart_rain_phase():
    global step, state_start_time, damage_accumulated, rain_phase_time, alphas, is_restarting
    is_restarting = True 
    alphas["fade_layer"] = 255 
    damage_accumulated = 0.0 
    rain_phase_time = 0.0 
    stop_all_environment_sounds()
    
def finalize_restart():
    global step, state_start_time, alphas, is_restarting
    step = 14
    state_start_time = pygame.time.get_ticks() 
    alphas["t-rainy"] = 255
    alphas["t-l"] = 255
    alphas["t-r"] = 255
    alphas["t-f"] = 255
    alphas["prompt_rain"] = 255
    is_restarting = False 
    # 教学关卡14是雨天，开始下雨音效
    update_environment_sound("rainy")

def main():
    global step, timer, state_start_time, img5_2_offset_y, is_dropping, last_mouse_x, arm_position_offset
    global mouse_anim_offset, has_slid, slide_time
    global sunlight_timer, damage_accumulated, rain_phase_time, raindrops, sourraindrops, is_restarting
    global level1_sunlight_collected, level1_rain_damage, level1_time_left, level1_weather
    global level1_weather_timer, level1_weather_duration, level1_game_active
    global level2_sunlight_collected, level2_rain_collected, level2_sourrain_damage, level2_time_left
    global level2_weather, level2_weather_timer, level2_weather_duration, level2_game_active
    global level3_sunlight_collected, level3_rain_collected, level3_sourrain_damage, level3_time_left
    global level3_weather, level3_weather_timer, level3_weather_duration, level3_game_active
    global bird_warning_timer, bird_warning_duration, bird_active, bird_y, bird_checked, bird_intro_y, bird_intro_active, bird_intro_state
    global level3_bird_trigger_time, level3_bird_started, level3_bird_finished
    global is_counting_down, countdown_start_time

    running = True
    state_start_time = pygame.time.get_ticks()
    
    last_mouse_x, _ = pygame.mouse.get_pos() 
    pygame.mouse.set_visible(True) 
    
    # --- 开场播放 pic1 ---
    sounds["pic1"].play()

    while running:
        dt = clock.tick(FPS)
        current_time = pygame.time.get_ticks()
        time_since_step = current_time - state_start_time
        
        current_mouse_x, _ = pygame.mouse.get_pos()
        mouse_dx = current_mouse_x - last_mouse_x

        # 增加判断：只有在不倒计时的时候才允许移动手臂
        if (step >= 11 and step < 33) and not is_restarting and not is_counting_down: 
            arm_position_offset += mouse_dx * ARM_MOVEMENT_SPEED
            arm_position_offset = pygame.math.clamp(arm_position_offset, 0, MAX_ARM_SPREAD)

        click_event = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                reset_tutorial_state()
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                step = 16
                state_start_time = current_time
                reset_level1()
                for key in alphas:
                    alphas[key] = 0
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                step = 21
                state_start_time = current_time
                reset_level2()
                for key in alphas:
                    alphas[key] = 0

            # R 键跳转到第三关
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                step = 27
                state_start_time = current_time
                reset_level3()
                for key in alphas:
                    alphas[key] = 0

            # T 键调试：直接跳转到最终结局
            if event.type == pygame.KEYDOWN and event.key == pygame.K_t:
                print("DEBUG: Jumping to Ending Sequence")
                stop_all_environment_sounds()
                stop_bgm_fadeout()
                sounds["ending"].play(fade_ms=2000)
                
                step = 34
                state_start_time = current_time
                for key in alphas:
                    alphas[key] = 0
                
                # 直接设置结局图片和文字可见
                alphas["E-2"] = 255
                alphas["ending_text_2"] = 255
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: 
                    click_event = True
                    sounds["click"].play() # 鼠标点击音效

        if is_restarting:
            if alphas["fade_layer"] > 0:
                alphas["fade_layer"] = max(0, alphas["fade_layer"] - FADE_RESTART_SPEED)
                
                if alphas["fade_layer"] < 100 and step == 14:
                    finalize_restart() 
            
            if is_restarting:
                last_mouse_x = current_mouse_x 
                screen.fill(BLACK)
                fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                fade_surface.fill(BLACK)
                fade_surface.set_alpha(alphas["fade_layer"])
                screen.blit(fade_surface, (0, 0))
                pygame.display.flip()
                continue 
        
        # 步骤 1-15 逻辑保持不变...
        if step == 1:
            if alphas["1"] < 255:
                alphas["1"] = min(255, alphas["1"] + FADE_SPEED)
            else:
                if alphas["text_step1"] < 255:
                    alphas["text_step1"] = min(255, alphas["text_step1"] + FADE_SPEED)
                if click_event:
                    step = 2
                    state_start_time = current_time
                    alphas["2-1"] = 0
                    alphas["text_step1"] = 0 
                    # 播放 pic2 和 bgm
                    sounds["pic2"].play()
                    play_bgm()

        elif step == 2:
            if alphas["2-1"] < 255:
                alphas["2-1"] = min(255, alphas["2-1"] + FADE_SPEED)
            if time_since_step > 1000:
                if alphas["2-2"] < 255:
                    alphas["2-2"] = min(255, alphas["2-2"] + FADE_SPEED)
                if alphas["2-2"] >= 255 and click_event:
                    step = 3
                    state_start_time = current_time
                    alphas["3-1"] = 0
                    alphas["3-2"] = 0

        elif step == 3:
            if alphas["3-1"] < 255:
                alphas["3-1"] = min(255, alphas["3-1"] + FADE_SPEED)
            if alphas["3-2"] < 255:
                alphas["3-2"] = min(255, alphas["3-2"] + FADE_SPEED)
            if alphas["3-1"] >= 255 and alphas["3-2"] >= 255 and click_event:
                step = 4
                state_start_time = current_time
                alphas["4"] = 0

        elif step == 4:
            if alphas["4"] < 255:
                alphas["4"] = min(255, alphas["4"] + FADE_SPEED)
            if alphas["4"] >= 255 and click_event:
                step = 5
                state_start_time = current_time
                alphas["5-1"] = 0

        elif step == 5:
            if alphas["5-1"] < 255:
                alphas["5-1"] = min(255, alphas["5-1"] + FADE_SPEED)
            if time_since_step > 1000:
                if alphas["5-2"] < 255:
                    alphas["5-2"] = min(255, alphas["5-2"] + FADE_SPEED)
                if alphas["5-3"] < 255:
                    alphas["5-3"] = min(255, alphas["5-3"] + FADE_SPEED)
                if alphas["5-2"] >= 255 and alphas["5-3"] >= 255 and click_event:
                    step = 6
                    state_start_time = current_time
                    is_dropping = True
                    sounds["drop"].play() # 种子下落音效

        elif step == 6:
            drop_duration = 1000
            if time_since_step <= drop_duration:
                progress = time_since_step / drop_duration
                target_drop_distance = 200 
                img5_2_offset_y = target_drop_distance * progress
            else:
                img5_2_offset_y = 200 
                if alphas["5-2"] > 0:
                    alphas["5-2"] = max(0, alphas["5-2"] - FADE_SPEED)
                if alphas["5-3"] > 0:
                    alphas["5-3"] = max(0, alphas["5-3"] - FADE_SPEED)
                if alphas["5-2"] == 0 and alphas["5-3"] == 0 and click_event:
                    step = 7
                    state_start_time = current_time
                    alphas["5-4"] = 0
                    sounds["water"].play() # 浇水音效

        elif step == 7:
            if time_since_step < 500 and alphas["5-4"] < 255: 
                alphas["5-4"] = min(255, alphas["5-4"] + FADE_SPEED)
            if time_since_step > 2500:
                 if alphas["5-4"] > 0:
                    alphas["5-4"] = max(0, alphas["5-4"] - FADE_SPEED)
            if time_since_step > 3000 and alphas["5-4"] == 0 and click_event:
                step = 8
                state_start_time = current_time
                alphas["5-5"] = 0

        if step == 8:
            if alphas["5-5"] < 255:
                alphas["5-5"] = min(255, alphas["5-5"] + FADE_SPEED)
            if alphas["5-5"] >= 255 and click_event:
                reset_tutorial_state()
                pygame.mouse.set_visible(True) 
        
        elif step == 9:
            if alphas["t-1"] < 255:
                for k in ["t-1", "t-l", "t-r", "t-f"]:
                    alphas[k] = min(255, alphas[k] + FADE_SPEED)
            else:
                step = 10
                state_start_time = current_time
                alphas["t-m"] = 0
                alphas["t-a"] = 0
                mouse_anim_offset = 0 

        elif step == 10:
            if time_since_step > 1000:
                if alphas["t-m"] < 255:
                    alphas["t-m"] = min(255, alphas["t-m"] + FADE_SPEED)
                    alphas["t-a"] = min(255, alphas["t-a"] + FADE_SPEED)
                mouse_anim_offset = MOUSE_MOVE_AMPLITUDE * 0.5 * (1 + math.sin(current_time * MOUSE_MOVE_SPEED))
                if alphas["t-m"] >= 255:
                    step = 11
                    state_start_time = current_time
                    arm_position_offset = 0 
        
        elif step == 11:
            if not has_slid: 
                mouse_anim_offset = MOUSE_MOVE_AMPLITUDE * 0.5 * (1 + math.sin(current_time * MOUSE_MOVE_SPEED))
            if abs(mouse_dx) > 0 and not has_slid:
                has_slid = True
                slide_time = current_time
                mouse_anim_offset = 0 
            if has_slid and (current_time - slide_time) > 2000:
                if alphas["t-m"] > 0:
                    alphas["t-m"] = max(0, alphas["t-m"] - FADE_SPEED * 2) 
                    alphas["t-a"] = max(0, alphas["t-a"] - FADE_SPEED * 2)
            if alphas["t-m"] == 0 and alphas["t-a"] == 0:
                step = 11.5
                state_start_time = current_time
        
        elif step == 11.5:
            if time_since_step > 1000:
                step = 12 
                state_start_time = current_time
                alphas["t-sunny"] = 0
                alphas["prompt_sunlight"] = 0

        elif step == 12:
            if alphas["t-sunny"] < 255:
                alphas["t-sunny"] = min(255, alphas["t-sunny"] + FADE_SPEED)
            if alphas["t-sunny"] >= 255:
                if alphas["prompt_sunlight"] < 255:
                    alphas["prompt_sunlight"] = min(255, alphas["prompt_sunlight"] + FADE_SPEED)
                
                is_arms_open = (arm_position_offset > ARM_CLOSED_THRESHOLD)
                
                if alphas["prompt_sunlight"] >= 255:
                    if sunlight_timer < SUNLIGHT_REQUIRED:
                        if is_arms_open:
                            sunlight_timer += dt / 1000
                            alphas["prompt_sunlight"] = max(0, alphas["prompt_sunlight"] - FADE_SPEED * 2)
                        sunlight_timer = min(sunlight_timer, SUNLIGHT_REQUIRED)
                    else:
                        sunlight_timer = SUNLIGHT_REQUIRED
                        step = 13
                        state_start_time = current_time
                        alphas["t-sunny"] = 255
                        alphas["prompt_rain"] = 0

        elif step == 13:
            if alphas["prompt_rain"] < 255:
                alphas["prompt_rain"] = min(255, alphas["prompt_rain"] + FADE_SPEED)
            else:
                if time_since_step > 1000:
                    step = 14
                    state_start_time = current_time
                    alphas["t-rainy"] = 0
                    damage_accumulated = 0.0 
                    rain_phase_time = 0.0 
                    update_environment_sound("rainy") # 开始下雨音效

        elif step == 14:
            rain_phase_time += dt / 1000 

            if alphas["t-sunny"] > 0:
                alphas["t-sunny"] = max(0, alphas["t-sunny"] - FADE_SPEED)
            if alphas["t-rainy"] < 255:
                alphas["t-rainy"] = min(255, alphas["t-rainy"] + FADE_SPEED)
                
            if alphas["t-rainy"] >= 255:
                is_arms_closed = (arm_position_offset <= ARM_CLOSED_THRESHOLD)
                
                if not is_arms_closed:
                    damage_accumulated += dt / 1000
                    damage_accumulated = min(damage_accumulated, RAIN_PROTECTION_DURATION) 
                
                if damage_accumulated >= RAIN_PROTECTION_DURATION:
                    restart_rain_phase() 
                    
                elif rain_phase_time >= RAIN_PHASE_DURATION:
                    step = 15
                    state_start_time = current_time
                    alphas["t-rainy"] = 255 
                    alphas["prompt_success"] = 0 
                    stop_all_environment_sounds() # 停止雨声
                    sounds["pass"].play() # 教程通过音效

        elif step == 15:
            is_fading_out = (alphas["t-rainy"] > 0)
            
            if is_fading_out:
                alphas["t-rainy"] = max(0, alphas["t-rainy"] - FADE_SPEED)
                alphas["prompt_rain"] = max(0, alphas["prompt_rain"] - FADE_SPEED * 2) 
            
            if not is_fading_out:
                if time_since_step < 50: 
                    state_start_time = current_time

                if alphas["prompt_success"] < 255:
                    alphas["prompt_success"] = min(255, alphas["prompt_success"] + FADE_SPEED)
                
                if (current_time - state_start_time) > 4000:
                    if click_event:
                        print("教学流程结束，进入第一关...")
                        step = 16
                        state_start_time = current_time
                        for key in alphas:
                            alphas[key] = 0

        # ====================================================
        # 第一关开场流程 (修改: 自动播放)
        # ====================================================
        elif step == 16:
            if alphas["1-sunny"] < 255:
                alphas["1-sunny"] = min(255, alphas["1-sunny"] + FADE_SPEED)
                alphas["level1_text"] = min(255, alphas["level1_text"] + FADE_SPEED)
            
            if alphas["1-sunny"] >= 255 and alphas["level1_text"] >= 255:
                if alphas["level1_intro_text"] < 255:
                    alphas["level1_intro_text"] = min(255, alphas["level1_intro_text"] + FADE_SPEED)
                
                # 修改：2s 后自动进入下一步
                if alphas["level1_intro_text"] >= 255 and time_since_step > 3000: # 留足淡入时间+2s阅读
                    step = 17
                    state_start_time = current_time
        
        elif step == 17:
            if alphas["1-sunny"] > 0:
                alphas["1-sunny"] = max(0, alphas["1-sunny"] - FADE_SPEED)
            if alphas["1-rainy"] < 255:
                alphas["1-rainy"] = min(255, alphas["1-rainy"] + FADE_SPEED)
                if alphas["1-rainy"] > 50 and current_environment_sound != "rainy":
                     update_environment_sound("rainy") 

            # 修改：停留时间改为 4000 (4s)
            if alphas["1-rainy"] >= 255 and time_since_step > 4000:
                step = 18
                state_start_time = current_time
        
        elif step == 18:
            fade_out_complete = True
            if current_environment_sound is not None:
                stop_all_environment_sounds() 

            for key in ["1-sunny", "1-rainy", "level1_text", "level1_intro_text"]:
                if alphas[key] > 0:
                    alphas[key] = max(0, alphas[key] - FADE_SPEED)
                    fade_out_complete = False
            
            # 修改：淡出完成后自动进入下一步
            if fade_out_complete:
                step = 19
                state_start_time = current_time
                reset_level1()
                is_counting_down = True
                countdown_start_time = current_time
                level1_game_active = False 
                alphas["t-1"] = 0
                alphas["t-l"] = 0
                alphas["t-r"] = 0
                alphas["t-f"] = 0
                alphas["level1_number"] = 0
                alphas["level1_timer"] = 0
                sounds["countbackward"].play() 
        
        # 第一关游戏进行中
        elif step == 19:
            # 基础画面渐显 (背景、花、手)
            if alphas["t-1"] < 255:
                 for k in ["t-1", "t-l", "t-r", "t-f"]:
                     alphas[k] = min(255, alphas[k] + FADE_SPEED)

            # 倒计时逻辑
            if is_counting_down:
                elapsed = current_time - countdown_start_time
                if elapsed > 3000: # 3秒倒计时结束
                    is_counting_down = False
                    level1_game_active = True
                    last_mouse_x = current_mouse_x 
            else:
                # 倒计时结束后，渐显 UI 元素
                for k in ["level1_number", "level1_timer"]:
                    if alphas[k] < 255:
                        alphas[k] = min(255, alphas[k] + FADE_SPEED)
            
                if level1_game_active:
                    # 只有在 active 时才更新天气音效
                    if level1_weather == "rainy":
                        update_environment_sound("rainy")
                    else:
                        stop_all_environment_sounds()

                    level1_time_left -= dt / 1000
                    level1_time_left = max(0, level1_time_left)
                    level1_weather_timer += dt / 1000
                    if level1_weather_timer >= level1_weather_duration:
                        level1_weather_timer = 0
                        level1_weather_duration = random.uniform(WEATHER_MIN_DURATION, WEATHER_MAX_DURATION)
                        
                        if level1_weather == "sunny":
                            level1_weather = "rainy"
                        else:
                            level1_weather = "sunny"
                    
                    is_arms_open = (arm_position_offset > ARM_CLOSED_THRESHOLD)
                    
                    if level1_weather == "sunny":
                        if is_arms_open:
                            level1_sunlight_collected += dt / 1000
                            level1_sunlight_collected = min(level1_sunlight_collected, LEVEL1_SUNLIGHT_REQUIRED)
                    else:
                        if is_arms_open:  
                            level1_rain_damage += dt / 1000
                            level1_rain_damage = min(level1_rain_damage, LEVEL1_RAIN_TOLERANCE)
                    
                    if level1_sunlight_collected >= LEVEL1_SUNLIGHT_REQUIRED:
                        step = 20
                        state_start_time = current_time
                        level1_game_active = False
                        alphas["2-f"] = 0
                        stop_all_environment_sounds()
                        sounds["pass"].play() 
                    elif level1_rain_damage >= LEVEL1_RAIN_TOLERANCE:
                        step = 20
                        state_start_time = current_time
                        level1_game_active = False
                        alphas["1-baselose"] = 0
                        alphas["1-f-l"] = 0
                        stop_all_environment_sounds()
                        sounds["fail"].play() 
                    elif level1_time_left <= 0:
                        step = 20
                        state_start_time = current_time
                        level1_game_active = False
                        alphas["1-baselose"] = 0
                        alphas["1-f-l"] = 0
                        stop_all_environment_sounds()
                        sounds["fail"].play() 
        
        # 第一关结算
        elif step == 20:
            if level1_sunlight_collected >= LEVEL1_SUNLIGHT_REQUIRED:
                alphas["t-l"] = 0
                alphas["t-r"] = 0
                if alphas["2-f"] < 255:
                    alphas["2-f"] = min(255, alphas["2-f"] + FADE_SPEED)
                if alphas["2-f"] >= 255:
                    if alphas["level1_intro_text"] < 255: # 复用介绍变量显示通关文字
                        alphas["level1_intro_text"] = min(255, alphas["level1_intro_text"] + FADE_SPEED)
                if alphas["level1_intro_text"] >= 255 and click_event:
                    step = 21
                    state_start_time = current_time
                    for key in alphas:
                        alphas[key] = 0
            else:
                alphas["t-l"] = 0
                alphas["t-r"] = 0
                alphas["t-1"] = 0
                if alphas["1-baselose"] < 255:
                    alphas["1-baselose"] = min(255, alphas["1-baselose"] + FADE_SPEED)
                if alphas["1-f-l"] < 255:
                    alphas["1-f-l"] = min(255, alphas["1-f-l"] + FADE_SPEED)
                if alphas["1-baselose"] >= 255 and alphas["1-f-l"] >= 255:
                    if alphas["prompt_fail_l1"] < 255:
                        alphas["prompt_fail_l1"] = min(255, alphas["prompt_fail_l1"] + FADE_SPEED)
                if alphas["prompt_fail_l1"] >= 255 and click_event:
                    step = 16
                    state_start_time = current_time
                    for key in alphas:
                        alphas[key] = 0
        
        # ====================================================
        # 第二关开场流程 (修改: 自动播放)
        # ====================================================
        elif step == 21:
            if alphas["1-sunny"] < 255:
                alphas["1-sunny"] = min(255, alphas["1-sunny"] + FADE_SPEED)
                alphas["level2_text"] = min(255, alphas["level2_text"] + FADE_SPEED)
            
            if alphas["1-sunny"] >= 255 and alphas["level2_text"] >= 255:
                if alphas["level2_intro_text"] < 255:
                    alphas["level2_intro_text"] = min(255, alphas["level2_intro_text"] + FADE_SPEED)
                
                # 修改：2s 后自动进入下一步
                if alphas["level2_intro_text"] >= 255 and time_since_step > 3000:
                    step = 22
                    state_start_time = current_time
        
        elif step == 22:
            if alphas["1-sunny"] > 0:
                alphas["1-sunny"] = max(0, alphas["1-sunny"] - FADE_SPEED)
            if alphas["1-rainy"] < 255:
                alphas["1-rainy"] = min(255, alphas["1-rainy"] + FADE_SPEED)
                if alphas["1-rainy"] > 50 and current_environment_sound != "rainy":
                    update_environment_sound("rainy") 
            
            # 修改：停留时间改为 4000 (4s)
            if alphas["1-rainy"] >= 255 and time_since_step > 4000:
                step = 23
                state_start_time = current_time
        
        elif step == 23:
            if alphas["1-rainy"] > 0:
                alphas["1-rainy"] = max(0, alphas["1-rainy"] - FADE_SPEED)
            if alphas["1-sourrain"] < 255:
                alphas["1-sourrain"] = min(255, alphas["1-sourrain"] + FADE_SPEED)
                if alphas["1-sourrain"] > 50 and current_environment_sound != "sourrain":
                    update_environment_sound("sourrain") 
            
            # 修改：停留时间改为 4000 (4s)
            if alphas["1-sourrain"] >= 255 and time_since_step > 4000: 
                step = 24
                state_start_time = current_time
        
        elif step == 24:
            fade_out_complete = True
            if current_environment_sound is not None:
                stop_all_environment_sounds()

            for key in ["1-sunny", "1-rainy", "1-sourrain", "level2_text", "level2_intro_text"]:
                if alphas[key] > 0:
                    alphas[key] = max(0, alphas[key] - FADE_SPEED)
                    fade_out_complete = False
            
            if fade_out_complete:
                step = 25
                state_start_time = current_time
                reset_level2()
                is_counting_down = True
                countdown_start_time = current_time
                level2_game_active = False
                alphas["t-1"] = 0
                alphas["t-l"] = 0
                alphas["t-r"] = 0
                alphas["2-f"] = 0  
                alphas["level2_number"] = 0
                alphas["level2_timer"] = 0
                sounds["countbackward"].play() 
        
        # 第二关游戏进行中
        elif step == 25:
             # 基础画面渐显
            if alphas["t-1"] < 255:
                for k in ["t-1", "t-l", "t-r", "2-f"]:
                    alphas[k] = min(255, alphas[k] + FADE_SPEED)
            
            # 倒计时逻辑
            if is_counting_down:
                elapsed = current_time - countdown_start_time
                if elapsed > 3000: # 3秒倒计时结束
                    is_counting_down = False
                    level2_game_active = True
                    last_mouse_x = current_mouse_x
            else:
                # 倒计时结束后，渐显 UI
                for k in ["level2_number", "level2_timer"]:
                    if alphas[k] < 255:
                        alphas[k] = min(255, alphas[k] + FADE_SPEED)
            
                if level2_game_active:
                    # 天气音效逻辑
                    if level2_weather == "rainy":
                        update_environment_sound("rainy")
                    elif level2_weather == "sourrain":
                        update_environment_sound("sourrain")
                    else:
                        stop_all_environment_sounds()

                    level2_time_left -= dt / 1000
                    level2_time_left = max(0, level2_time_left)
                    level2_weather_timer += dt / 1000
                    if level2_weather_timer >= level2_weather_duration:
                        level2_weather_timer = 0
                        level2_weather_duration = random.uniform(WEATHER_MIN_DURATION, WEATHER_MAX_DURATION)
                        
                        options = ["sunny", "rainy", "sourrain"]
                        if level2_weather in options:
                            options.remove(level2_weather)
                        level2_weather = random.choice(options)
                    
                    is_arms_open = (arm_position_offset > ARM_CLOSED_THRESHOLD)
                    
                    if level2_weather == "sunny":
                        if is_arms_open and level2_sunlight_collected < LEVEL2_SUNLIGHT_REQUIRED:
                            level2_sunlight_collected += dt / 1000
                            level2_sunlight_collected = min(level2_sunlight_collected, LEVEL2_SUNLIGHT_REQUIRED)
                    elif level2_weather == "rainy":
                        if is_arms_open and level2_rain_collected < LEVEL2_RAIN_REQUIRED:
                            level2_rain_collected += dt / 1000
                            level2_rain_collected = min(level2_rain_collected, LEVEL2_RAIN_REQUIRED)
                    else: 
                        if is_arms_open: 
                            level2_sourrain_damage += dt / 1000
                            level2_sourrain_damage = min(level2_sourrain_damage, LEVEL2_SOURRAIN_TOLERANCE)
                    
                    if (level2_sunlight_collected >= LEVEL2_SUNLIGHT_REQUIRED and 
                        level2_rain_collected >= LEVEL2_RAIN_REQUIRED):
                        step = 26
                        state_start_time = current_time
                        level2_game_active = False
                        alphas["3-f"] = 0
                        stop_all_environment_sounds()
                        sounds["pass"].play()
                    elif level2_sourrain_damage >= LEVEL2_SOURRAIN_TOLERANCE:
                        step = 26
                        state_start_time = current_time
                        level2_game_active = False
                        alphas["1-baselose"] = 0
                        alphas["2-f-l"] = 0
                        stop_all_environment_sounds()
                        sounds["fail"].play()
                    elif level2_time_left <= 0:
                        step = 26
                        state_start_time = current_time
                        level2_game_active = False
                        alphas["1-baselose"] = 0
                        alphas["2-f-l"] = 0
                        stop_all_environment_sounds()
                        sounds["fail"].play()
        
        # 第二关结算
        elif step == 26:
            if (level2_sunlight_collected >= LEVEL2_SUNLIGHT_REQUIRED and 
                level2_rain_collected >= LEVEL2_RAIN_REQUIRED):
                alphas["t-l"] = 0
                alphas["t-r"] = 0
                if alphas["3-f"] < 255:
                    alphas["3-f"] = min(255, alphas["3-f"] + FADE_SPEED)
                if alphas["3-f"] >= 255:
                    if alphas["level2_intro_text"] < 255:
                        alphas["level2_intro_text"] = min(255, alphas["level2_intro_text"] + FADE_SPEED)
                if alphas["level2_intro_text"] >= 255 and click_event:
                    # 进入第三关
                    print("第二关完成，进入第三关。")
                    step = 27
                    state_start_time = current_time
                    reset_level3()
                    for key in alphas:
                        alphas[key] = 0
            else:
                alphas["t-l"] = 0
                alphas["t-r"] = 0
                alphas["t-1"] = 0
                if alphas["1-baselose"] < 255:
                    alphas["1-baselose"] = min(255, alphas["1-baselose"] + FADE_SPEED)
                if alphas["2-f-l"] < 255:
                    alphas["2-f-l"] = min(255, alphas["2-f-l"] + FADE_SPEED)
                if alphas["1-baselose"] >= 255 and alphas["2-f-l"] >= 255:
                    if alphas["prompt_fail_l2"] < 255:
                        alphas["prompt_fail_l2"] = min(255, alphas["prompt_fail_l2"] + FADE_SPEED)
                if alphas["prompt_fail_l2"] >= 255 and click_event:
                    step = 21
                    state_start_time = current_time
                    for key in alphas:
                        alphas[key] = 0

        # ====================================================
        # 第三关流程 (修改: 自动播放)
        # ====================================================

        # Step 27: 第三关开场 (Sunny + Text)
        elif step == 27:
            if alphas["1-sunny"] < 255:
                alphas["1-sunny"] = min(255, alphas["1-sunny"] + FADE_SPEED)
                alphas["level3_text"] = min(255, alphas["level3_text"] + FADE_SPEED)
                if alphas["level3_intro_text"] < 255:
                     alphas["level3_intro_text"] = min(255, alphas["level3_intro_text"] + FADE_SPEED)

            # 修改：2s 后自动进入下一步
            if alphas["level3_intro_text"] >= 255 and time_since_step > 3000:
                step = 28
                state_start_time = current_time
                bird_intro_y = -50
                bird_intro_x = (SCREEN_WIDTH // 2) - 200 
                bird_intro_active = False
                alphas["birdshit"] = 0
        
        # Step 28: 鸟屎介绍 (保持原逻辑，鸟屎动画结束后自动跳转)
        elif step == 28:
            if not bird_intro_active:
                 if time_since_step > 500: # 稍微减少等待时间
                    bird_intro_active = True
                    alphas["birdshit"] = 255
            else:
                # 鸟屎下落
                bird_intro_y += BIRD_DROP_SPEED
                bird_intro_x += BIRD_DROP_SPEED * 0.5 
                
                if bird_intro_y > SCREEN_HEIGHT // 2 - 100:
                        if alphas["birdshit"] > 0:
                            alphas["birdshit"] = max(0, alphas["birdshit"] - BIRD_FADE_SPEED)
                
                # 修改：动画结束自动跳转
                if bird_intro_y > SCREEN_HEIGHT or alphas["birdshit"] == 0:
                    step = 29
                    state_start_time = current_time

        # Step 29: 切换到 Rainy
        elif step == 29:
            # Sunny 渐隐
            if alphas["1-sunny"] > 0:
                alphas["1-sunny"] = max(0, alphas["1-sunny"] - FADE_SPEED)

            # Rainy 渐显
            if alphas["1-rainy"] < 255:
                alphas["1-rainy"] = min(255, alphas["1-rainy"] + FADE_SPEED)
                if alphas["1-rainy"] > 50 and current_environment_sound != "rainy":
                    update_environment_sound("rainy")
            
            # 修改：停留时间改为 4000 (4s)
            if alphas["1-rainy"] >= 255 and time_since_step > 4000:
                step = 29.5 
                state_start_time = current_time

        # Step 29.5: 切换到 Sourrain
        elif step == 29.5:
             # Rainy 渐隐, Sourrain 渐显
            if alphas["1-rainy"] > 0:
                 alphas["1-rainy"] = max(0, alphas["1-rainy"] - FADE_SPEED)
            if alphas["1-sourrain"] < 255:
                 alphas["1-sourrain"] = min(255, alphas["1-sourrain"] + FADE_SPEED)
                 if alphas["1-sourrain"] > 50 and current_environment_sound != "sourrain":
                     update_environment_sound("sourrain")
            
            # 修改：停留时间改为 4000 (4s)
            if alphas["1-sourrain"] >= 255 and time_since_step > 4000:
                step = 30
                state_start_time = current_time

        # Step 30: 准备开始
        elif step == 30:
            fade_out_complete = True
            if current_environment_sound is not None:
                stop_all_environment_sounds()

            for key in ["1-sunny", "1-rainy", "1-sourrain", "level3_text", "level3_intro_text"]:
                if alphas[key] > 0:
                    alphas[key] = max(0, alphas[key] - FADE_SPEED)
                    fade_out_complete = False
            
            if fade_out_complete:
                step = 31
                state_start_time = current_time
                reset_level3()
                is_counting_down = True
                countdown_start_time = current_time
                level3_game_active = False
                alphas["t-1"] = 0
                alphas["t-l"] = 0
                alphas["t-r"] = 0
                alphas["3-f"] = 0  
                alphas["level3_number"] = 0
                alphas["level3_timer"] = 0
                sounds["countbackward"].play()
                
                # 初始化 Sunny 鸟屎逻辑
                level3_weather = "sunny"
                level3_weather_duration = 5.0
                level3_weather_timer = 0
                level3_bird_trigger_time = random.uniform(2.0, 3.0)
                level3_bird_started = False
                level3_bird_finished = False # 重置鸟屎状态

        # Step 31: 第三关游戏进行中
        elif step == 31:
             # 基础画面渐显
            if alphas["t-1"] < 255:
                for k in ["t-1", "t-l", "t-r", "3-f"]:
                    alphas[k] = min(255, alphas[k] + FADE_SPEED)

            # 倒计时逻辑
            if is_counting_down:
                elapsed = current_time - countdown_start_time
                if elapsed > 3000: # 3秒倒计时结束
                    is_counting_down = False
                    level3_game_active = True
                    last_mouse_x = current_mouse_x
            else:
                # 倒计时结束后，渐显 UI
                for k in ["level3_number", "level3_timer"]:
                    if alphas[k] < 255:
                        alphas[k] = min(255, alphas[k] + FADE_SPEED)

                if level3_game_active:
                    # 天气音效逻辑
                    if level3_weather == "rainy":
                        update_environment_sound("rainy")
                    elif level3_weather == "sourrain":
                        update_environment_sound("sourrain")
                    else:
                        stop_all_environment_sounds()

                    level3_time_left -= dt / 1000
                    level3_time_left = max(0, level3_time_left)

                    is_arms_open = (arm_position_offset > ARM_CLOSED_THRESHOLD)

                    # --- 天气计时器 ---
                    level3_weather_timer += dt / 1000
                    if level3_weather_timer >= level3_weather_duration:
                        level3_weather_timer = 0
                        
                        # 切换天气
                        options = ["sunny", "rainy", "sourrain"]
                        if level3_weather in options:
                            options.remove(level3_weather)
                        level3_weather = random.choice(options)
                        
                        if level3_weather == "sunny":
                            level3_weather_duration = 7.0
                            # 重置鸟屎逻辑
                            level3_bird_trigger_time = random.uniform(2.0, 3.0)
                            level3_bird_started = False
                            level3_bird_finished = False 
                            bird_warning_timer = 0
                            alphas["level3_intro_text"] = 0 # 确保文字隐藏
                        else:
                            level3_weather_duration = random.uniform(WEATHER_MIN_DURATION, WEATHER_MAX_DURATION)

                    # --- 鸟屎逻辑 ---
                    if level3_weather == "sunny":
                        if not level3_bird_started and level3_weather_timer >= level3_bird_trigger_time:
                            level3_bird_started = True
                            level3_bird_finished = False 
                            bird_warning_timer = 0
                            bird_warning_duration = random.uniform(2.0, 2.5)
                            bird_active = False 
                            alphas["level3_intro_text"] = 0 
                        
                        # 警告阶段 (复用 level3_intro_text 变量显示顶部提示)
                        if level3_bird_started and not bird_active and not level3_bird_finished:
                            if alphas["level3_intro_text"] == 0:
                                sounds["shit"].play()

                            if alphas["level3_intro_text"] < 255:
                                alphas["level3_intro_text"] = min(255, alphas["level3_intro_text"] + FADE_SPEED * 2)
                            
                            bird_warning_timer += dt / 1000
                            if bird_warning_timer >= bird_warning_duration:
                                bird_active = True
                                bird_y = -50
                                bird_x = (SCREEN_WIDTH // 2) - 200
                                bird_checked = False
                                alphas["birdshit"] = 255
                                alphas["level3_intro_text"] = 0 

                    # --- 鸟屎下落逻辑 ---
                    if bird_active:
                        bird_y += BIRD_DROP_SPEED
                        bird_x += BIRD_DROP_SPEED * 0.5
                        check_y = SCREEN_HEIGHT * BIRD_CHECK_HEIGHT_RATIO
                        
                        if bird_y >= check_y and not bird_checked:
                            bird_checked = True
                            if is_arms_open:
                                pass 
                            else:
                                bird_active = False
                                alphas["birdshit"] = 0
                                level3_bird_finished = True 
                        
                        if bird_checked and bird_active:
                            if bird_y >= SCREEN_HEIGHT // 2:
                                level3_game_active = False
                                step = 32
                                state_start_time = current_time
                                alphas["1-baselose"] = 0
                                alphas["3-f-l"] = 0
                                stop_all_environment_sounds()
                                sounds["fail"].play()

                    # --- 资源收集逻辑 ---
                    if level3_weather == "sunny":
                        if is_arms_open:
                            level3_sunlight_collected += dt / 1000
                            level3_sunlight_collected = min(level3_sunlight_collected, LEVEL3_SUNLIGHT_REQUIRED)
                    elif level3_weather == "rainy":
                        if is_arms_open: # 收集雨水
                            level3_rain_collected += dt / 1000
                            level3_rain_collected = min(level3_rain_collected, LEVEL3_RAIN_REQUIRED)
                    elif level3_weather == "sourrain":
                        if is_arms_open: # 酸雨伤害
                            level3_sourrain_damage += dt / 1000
                            level3_sourrain_damage = min(level3_sourrain_damage, LEVEL3_SOURRAIN_TOLERANCE)
                    
                    if (level3_sunlight_collected >= LEVEL3_SUNLIGHT_REQUIRED and 
                        level3_rain_collected >= LEVEL3_RAIN_REQUIRED):
                        # 胜利
                        step = 33
                        state_start_time = current_time
                        level3_game_active = False
                        for k in ["t-1", "t-l", "t-r", "3-f", "level3_number", "level3_timer", "t-sunny", "t-rainy", "1-sourrain", "birdshit", "level3_intro_text"]:
                            alphas[k] = 0
                        stop_all_environment_sounds()
                        sounds["pass"].play()
                    
                    elif level3_sourrain_damage >= LEVEL3_SOURRAIN_TOLERANCE:
                        # 失败
                        step = 32
                        state_start_time = current_time
                        level3_game_active = False
                        alphas["1-baselose"] = 0
                        alphas["3-f-l"] = 0
                        stop_all_environment_sounds()
                        sounds["fail"].play()

                    elif level3_time_left <= 0:
                        # 失败
                        step = 32
                        state_start_time = current_time
                        level3_game_active = False
                        alphas["1-baselose"] = 0
                        alphas["3-f-l"] = 0
                        stop_all_environment_sounds()
                        sounds["fail"].play()
        
        # Step 32: 第三关失败
        elif step == 32:
            alphas["t-l"] = 0
            alphas["t-r"] = 0
            alphas["t-1"] = 0
            alphas["3-f"] = 0
            
            if alphas["1-baselose"] < 255:
                alphas["1-baselose"] = min(255, alphas["1-baselose"] + FADE_SPEED)
            if alphas["3-f-l"] < 255:
                alphas["3-f-l"] = min(255, alphas["3-f-l"] + FADE_SPEED)
            
            if alphas["1-baselose"] >= 255 and alphas["3-f-l"] >= 255:
                 if alphas["level3_prompt_fail"] < 255:
                        alphas["level3_prompt_fail"] = min(255, alphas["level3_prompt_fail"] + FADE_SPEED)

            if alphas["level3_prompt_fail"] >= 255 and click_event:
                step = 27
                state_start_time = current_time
                for key in alphas:
                    alphas[key] = 0

        # Step 33 & 34: 最终结局 Part 1
        elif step == 33:
            if alphas["E-1"] < 255:
                alphas["E-1"] = min(255, alphas["E-1"] + FADE_SPEED)
            
            if alphas["E-1"] >= 255:
                if alphas["ending_text_1"] < 255:
                     alphas["ending_text_1"] = min(255, alphas["ending_text_1"] + FADE_SPEED)
            
            if alphas["ending_text_1"] >= 255 and click_event:
                 step = 34
                 state_start_time = current_time
                 stop_bgm_fadeout() 
                 sounds["ending"].play(fade_ms=2000)
                 
        # Step 34: 最终结局 Part 2
        elif step == 34:
            if alphas["E-1"] > 0:
                alphas["E-1"] = max(0, alphas["E-1"] - FADE_SPEED)
            if alphas["ending_text_1"] > 0:
                 alphas["ending_text_1"] = max(0, alphas["ending_text_1"] - FADE_SPEED)
            
            if alphas["E-2"] < 255:
                alphas["E-2"] = min(255, alphas["E-2"] + FADE_SPEED)
            
            if alphas["E-2"] >= 255:
                 if alphas["ending_text_2"] < 255:
                     alphas["ending_text_2"] = min(255, alphas["ending_text_2"] + FADE_SPEED)
            
            if alphas["ending_text_2"] >= 255 and click_event:
                running = False


        last_mouse_x = current_mouse_x 

        # ==================================================
        # 雨滴更新逻辑
        # ==================================================
        
        should_rain = False
        
        # 教程阶段下雨
        if step >= 14 and step < 16 and alphas["t-rainy"] > 0 and not is_restarting:
            should_rain = True
        # 第一关介绍下雨
        elif step == 17 and alphas["1-rainy"] > 0:
            should_rain = True
        # 第一关游戏下雨
        elif step == 19 and level1_game_active and level1_weather == "rainy":
            should_rain = True
        # 第二关介绍下雨
        elif step == 22 and alphas["1-rainy"] > 0:
            should_rain = True
        # 第二关游戏下雨
        elif step == 25 and level2_game_active and level2_weather == "rainy":
            should_rain = True
        # 第三关介绍下雨
        elif (step == 29 or step == 29.5) and alphas["1-rainy"] > 0:
            should_rain = True
        # 第三关游戏下雨
        elif step == 31 and level3_game_active and level3_weather == "rainy":
             should_rain = True
            
        if should_rain:
            if len(raindrops) < RAINDROP_COUNT:
                for _ in range(RAINDROP_COUNT - len(raindrops)):
                    if random.random() < 0.1:
                        raindrops.append({
                            "x": random.randint(0, SCREEN_WIDTH),
                            "y": random.randint(-SCREEN_HEIGHT // 4, 0),
                            "speed": random.uniform(RAINDROP_SPEED_MIN, RAINDROP_SPEED_MAX),
                        })
            new_raindrops = []
            for drop in raindrops:
                drop["y"] += drop["speed"]
                if drop["y"] < SCREEN_HEIGHT + 20: 
                    new_raindrops.append(drop)
            raindrops = new_raindrops
        else:
            raindrops = []

        # 判断是否下酸雨
        should_sour_rain = False
        # 第二关介绍下酸雨
        if step == 23 and alphas["1-sourrain"] > 0:
            should_sour_rain = True
        # 第二关游戏下酸雨
        elif step == 25 and level2_game_active and level2_weather == "sourrain":
            should_sour_rain = True
        # 第三关介绍下酸雨
        elif (step == 29.5 or step == 30) and alphas["1-sourrain"] > 0:
            should_sour_rain = True
        # 第三关游戏下酸雨
        elif step == 31 and level3_game_active and level3_weather == "sourrain":
             should_sour_rain = True
            
        if should_sour_rain:
            if len(sourraindrops) < RAINDROP_COUNT:
                for _ in range(RAINDROP_COUNT - len(sourraindrops)):
                    if random.random() < 0.1:
                        sourraindrops.append({
                            "x": random.randint(0, SCREEN_WIDTH),
                            "y": random.randint(-SCREEN_HEIGHT // 4, 0),
                            "speed": random.uniform(RAINDROP_SPEED_MIN, RAINDROP_SPEED_MAX),
                        })
            new_sourraindrops = []
            for drop in sourraindrops:
                drop["y"] += drop["speed"]
                if drop["y"] < SCREEN_HEIGHT + 20: 
                    new_sourraindrops.append(drop)
            sourraindrops = new_sourraindrops
        else:
            sourraindrops = []
        
        # ----------------------------------------------------
        # 绘制阶段 (Draw)
        # ----------------------------------------------------

        screen.fill(BLACK) 

        def blit_alpha(key, pos):
            img = images[key]
            alpha = alphas[key]
            if alpha > 0: 
                img.set_alpha(alpha)
                screen.blit(img, pos)

        # 开场绘制逻辑 Step 1-8
        if step >= 1 and step < 16: 
            blit_alpha("1", (0, 0))
            if step == 1 and alphas["text_step1"] > 0:
                draw_styled_text_box("click anywhere to continue", alphas["text_step1"], style="bottom_left", font=ui_big_font)

        if step >= 2 and step < 16: 
            blit_alpha("2-1", (0, 0))
            pos_2_2_x = SCREEN_WIDTH - images["2-2"].get_width()  
            pos_2_2_y = 30 
            blit_alpha("2-2", (pos_2_2_x, pos_2_2_y))

        if step >= 3 and step < 16:
            blit_alpha("3-1", (0, 0))
            pos_3_2_x = SCREEN_WIDTH - images["3-2"].get_width() 
            pos_3_2_y = 30
            blit_alpha("3-2", (pos_3_2_x, pos_3_2_y))

        if step >= 4 and step < 16:
            blit_alpha("4", (0, 0))

        if step >= 5 and step < 16:
            blit_alpha("5-1", (0, 0))
            pos_5_2_x = (SCREEN_WIDTH - images["5-2"].get_width()) // 2 - 15
            pos_5_2_y = 50 + img5_2_offset_y + 165
            blit_alpha("5-2", (pos_5_2_x, pos_5_2_y))
            pos_5_3_x = (SCREEN_WIDTH - images["5-3"].get_width()) // 2 + 25
            pos_5_3_y = 0 
            blit_alpha("5-3", (pos_5_3_x, pos_5_3_y))
        
        if step >= 7 and step < 16:
            pos_5_4_x = (SCREEN_WIDTH - images["5-4"].get_width()) // 2 + 110
            pos_5_4_y = (SCREEN_HEIGHT - images["5-4"].get_height()) // 2 - 140 
            blit_alpha("5-4", (pos_5_4_x, pos_5_4_y))

        if step == 8: 
             blit_alpha("5-5", (0, 0))

        # --- 绘制教学图层 (Step 9-15) ---

        if step >= 9 and step < 16:
            blit_alpha("t-1", (0, 0))

            pos_f_x = (SCREEN_WIDTH - images["t-f"].get_width()) // 2 + 20
            pos_f_y = SCREEN_HEIGHT - images["t-f"].get_height() - 200
            blit_alpha("t-f", (pos_f_x, pos_f_y))
            
            center_x = SCREEN_WIDTH // 2 + 10
            center_y = SCREEN_HEIGHT - images["t-l"].get_height() + 200 
            hand_l_x = center_x - images["t-l"].get_width() - arm_position_offset - 30
            hand_l_y = center_y 
            blit_alpha("t-l", (hand_l_x, hand_l_y))
            hand_r_x = center_x + arm_position_offset + 30
            hand_r_y = center_y 
            blit_alpha("t-r", (hand_r_x, hand_r_y))
            
            if step == 10 or step == 11:
                current_mouse_offset = mouse_anim_offset 
                mouse_base_x = SCREEN_WIDTH * 0.75 - images["t-m"].get_width() // 2 - 100 
                mouse_base_y = SCREEN_HEIGHT * 0.7 - 200
                pos_m_x = mouse_base_x + current_mouse_offset
                pos_m_y = mouse_base_y
                blit_alpha("t-m", (pos_m_x, pos_m_y))
                pos_a_x = mouse_base_x + images["t-m"].get_width() // 2 - 150 
                pos_a_y = mouse_base_y + images["t-m"].get_height() // 2 + 50
                blit_alpha("t-a", (pos_a_x, pos_a_y))
            
            if step == 10 or step == 11:
                if alphas["t-m"] > 0:
                    draw_styled_text_box("Open and close the arms with mouse to raise and protect the flower!", alphas["t-m"])

            if step >= 12 and alphas["t-sunny"] > 0:
                blit_alpha("t-sunny", (0, 0))

            if step >= 14 and alphas["t-rainy"] > 0:
                blit_alpha("t-rainy", (0, 0))

            if step == 12:
                if alphas["prompt_sunlight"] > 0:
                    draw_styled_text_box("Collect sunlight by opening your arms.", alphas["prompt_sunlight"])
                if sunlight_timer > 0 and sunlight_timer < SUNLIGHT_REQUIRED:
                    # 教学阶段进度条
                    draw_progress_bar_custom(sunlight_timer, SUNLIGHT_REQUIRED, 255, "icon_sun", SCREEN_WIDTH//2 - 175, SCREEN_HEIGHT - 120, 350, 20)

            if step == 13 or step == 14 or (step == 15 and alphas["prompt_rain"] > 0): 
                draw_styled_text_box("Block unwanted rain by closing them.", alphas["prompt_rain"])
                
            if step == 14 and alphas["t-rainy"] >= 255:
                # 教学阶段雨天伤害
                draw_progress_bar_custom(damage_accumulated, RAIN_PROTECTION_DURATION, 255, "icon_heart", SCREEN_WIDTH//2 - 175, SCREEN_HEIGHT - 120, 350, 20, is_damage=True)

            if step == 15 and alphas["prompt_success"] > 0:
                text1 = "The flower's needs will change, so watch carefully!"
                text2 = "Now you can focus on truly caring for this flower."
                
                time_since_step_15_start = current_time - state_start_time
                if time_since_step_15_start <= 4000:
                    text_to_draw = text1
                else:
                    text_to_draw = text2
                draw_styled_text_box(text_to_draw, alphas["prompt_success"])

            if step >= 14 and alphas["t-rainy"] > 0 and len(raindrops) > 0:
                raindrop_img = images["t-raindrop"]
                raindrop_img.set_alpha(255)
                for drop in raindrops:
                    screen.blit(raindrop_img, (drop["x"], drop["y"]))
                
        # ====================================================
        # 第一关绘制
        # ====================================================
        
        if step >= 16 and step < 19:
            # --- 背景绘制 ---
            if alphas["1-sunny"] > 0:
                blit_alpha("1-sunny", (0, 0))
                
            if alphas["1-rainy"] > 0:
                blit_alpha("1-rainy", (0, 0))
                if len(raindrops) > 0:
                    raindrop_img = images["t-raindrop"]
                    raindrop_img.set_alpha(alphas["1-rainy"])
                    for drop in raindrops:
                        screen.blit(raindrop_img, (drop["x"], drop["y"]))

            # --- 花朵绘制 ---
            flower_alpha = max(alphas["1-sunny"], alphas["1-rainy"])
            if flower_alpha > 0 and "t-f-intro-scaled" in images:
                # 优化：使用预缩放的图片
                img = images["t-f-intro-scaled"]
                img.set_alpha(flower_alpha)
                pos_f_x = (SCREEN_WIDTH - img.get_width()) // 2 + 10
                pos_f_y = SCREEN_HEIGHT - img.get_height() - 277
                screen.blit(img, (pos_f_x, pos_f_y))
            
            # --- 文字绘制 ---
            if alphas["level1_text"] > 0:
                draw_level_text("Level 1", alphas["level1_text"])
            
            # 统一介绍文字
            if alphas["level1_intro_text"] > 0:
                draw_styled_text_box("The seedling has been watered! Time for some sunlight!", alphas["level1_intro_text"])
        
        elif step == 19:
            blit_alpha("t-1", (0, 0))

            pos_f_x = (SCREEN_WIDTH - images["t-f"].get_width()) // 2 + 20
            pos_f_y = SCREEN_HEIGHT - images["t-f"].get_height() - 200
            blit_alpha("t-f", (pos_f_x, pos_f_y))

            center_x = SCREEN_WIDTH // 2 + 10
            center_y = SCREEN_HEIGHT - images["t-l"].get_height() + 200 
            hand_l_x = center_x - images["t-l"].get_width() - arm_position_offset - 30
            hand_l_y = center_y 
            blit_alpha("t-l", (hand_l_x, hand_l_y))
            hand_r_x = center_x + arm_position_offset + 30
            hand_r_y = center_y 
            blit_alpha("t-r", (hand_r_x, hand_r_y))

            if is_counting_down:
                images["t-sunny"].set_alpha(255)
                screen.blit(images["t-sunny"], (0, 0))
            elif level1_weather == "sunny":
                images["t-sunny"].set_alpha(255)
                screen.blit(images["t-sunny"], (0, 0))
            elif level1_weather == "rainy":
                images["t-rainy"].set_alpha(255)
                screen.blit(images["t-rainy"], (0, 0))
            
            if is_counting_down:
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                overlay.fill((128, 128, 128)) 
                overlay.set_alpha(150) 
                screen.blit(overlay, (0, 0))
                
                time_rem = 3 - int((current_time - countdown_start_time) / 1000)
                if time_rem > 0:
                    count_text = countdown_font.render(str(time_rem), True, WHITE)
                    count_rect = count_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                    screen.blit(count_text, count_rect)
            
            if alphas["level1_number"] > 0:
                draw_level_number(1, alphas["level1_number"])
            
            if alphas["level1_timer"] > 0:
                draw_game_timer(level1_time_left, alphas["level1_timer"])
            
            # --- Level 1 进度条布局 (左右并排) ---
            if level1_game_active:
                bar_width = 350
                # 修改：增加间距，避免遮挡
                spacing = 180 
                total_w = bar_width * 2 + spacing
                start_x = (SCREEN_WIDTH - total_w) // 2
                
                # 左：Sunlight (collected)
                draw_progress_bar_custom(level1_sunlight_collected, LEVEL1_SUNLIGHT_REQUIRED, 255, "icon_sun", start_x, SCREEN_HEIGHT - 100, bar_width, 20)
                
                # 右：Rain Damage
                draw_progress_bar_custom(level1_rain_damage, LEVEL1_RAIN_TOLERANCE, 255, "icon_heart", start_x + bar_width + spacing, SCREEN_HEIGHT - 100, bar_width, 20, is_damage=True)
            
            if level1_weather == "rainy" and len(raindrops) > 0 and not is_counting_down:
                raindrop_img = images["t-raindrop"]
                raindrop_img.set_alpha(255)
                for drop in raindrops:
                    screen.blit(raindrop_img, (drop["x"], drop["y"]))
                
        elif step == 20:
            if level1_sunlight_collected >= LEVEL1_SUNLIGHT_REQUIRED:
                blit_alpha("t-1", (0, 0))
                pos_f_x = (SCREEN_WIDTH - images["2-f"].get_width()) // 2 + 10
                pos_f_y = SCREEN_HEIGHT - images["2-f"].get_height() - 200
                blit_alpha("2-f", (pos_f_x, pos_f_y))
                if alphas["level1_intro_text"] > 0:
                    draw_styled_text_box("The seed has turned into a bud.", alphas["level1_intro_text"])
            else:
                blit_alpha("1-baselose", (0, 0))
                pos_f_x = (SCREEN_WIDTH - images["1-f-l"].get_width()) // 2 + 20
                pos_f_y = SCREEN_HEIGHT - images["1-f-l"].get_height() - 200
                blit_alpha("1-f-l", (pos_f_x, pos_f_y))
                if alphas["prompt_fail_l1"] > 0:
                    draw_styled_text_box("You lost. The seed dies. Click to try again.", alphas["prompt_fail_l1"])

        # ====================================================
        # 第二关绘制
        # ====================================================
        
        if step >= 21 and step < 25:
            # --- 背景绘制 ---
            if alphas["1-sunny"] > 0:
                blit_alpha("1-sunny", (0, 0))
            if alphas["1-rainy"] > 0:
                blit_alpha("1-rainy", (0, 0))
                if len(raindrops) > 0:
                    raindrop_img = images["t-raindrop"]
                    raindrop_img.set_alpha(alphas["1-rainy"])
                    for drop in raindrops:
                        screen.blit(raindrop_img, (drop["x"], drop["y"]))
            if alphas["1-sourrain"] > 0:
                blit_alpha("1-sourrain", (0, 0))
                if len(sourraindrops) > 0:
                    sourraindrop_img = images["sourraindrop"]
                    sourraindrop_img.set_alpha(alphas["1-sourrain"])
                    for drop in sourraindrops:
                        screen.blit(sourraindrop_img, (drop["x"], drop["y"]))
            
            # --- 花朵绘制 ---
            flower_alpha = max(alphas["1-sunny"], alphas["1-rainy"], alphas["1-sourrain"])
            if flower_alpha > 0:
                scale_ratio = 2/3
                orig_w = images["2-f"].get_width()
                orig_h = images["2-f"].get_height()
                scaled_flower = pygame.transform.smoothscale(images["2-f"], (int(orig_w * scale_ratio), int(orig_h * scale_ratio)))
                scaled_flower.set_alpha(flower_alpha)
                pos_f_x = (SCREEN_WIDTH - scaled_flower.get_width()) // 2 - 3
                pos_f_y = SCREEN_HEIGHT - scaled_flower.get_height() - 277
                screen.blit(scaled_flower, (pos_f_x, pos_f_y))

            # --- 文字绘制 ---
            if alphas["level2_text"] > 0:
                draw_level_text("Level 2", alphas["level2_text"])
            
            # 统一介绍文字
            if alphas["level2_intro_text"] > 0:
                draw_styled_text_box("To make it bloom, give it plenty of sun and rain. But watch out for the sourrain!", alphas["level2_intro_text"])
        
        elif step == 25:
            blit_alpha("t-1", (0, 0))

            pos_f_x = (SCREEN_WIDTH - images["2-f"].get_width()) // 2 + 5
            pos_f_y = SCREEN_HEIGHT - images["2-f"].get_height() - 200
            blit_alpha("2-f", (pos_f_x, pos_f_y))

            center_x = SCREEN_WIDTH // 2 + 10
            center_y = SCREEN_HEIGHT - images["t-l"].get_height() + 200 
            hand_l_x = center_x - images["t-l"].get_width() - arm_position_offset - 30
            hand_l_y = center_y 
            blit_alpha("t-l", (hand_l_x, hand_l_y))
            hand_r_x = center_x + arm_position_offset + 30
            hand_r_y = center_y 
            blit_alpha("t-r", (hand_r_x, hand_r_y))

            if is_counting_down:
                 images["t-sunny"].set_alpha(255)
                 screen.blit(images["t-sunny"], (0, 0))
            elif level2_weather == "sunny":
                images["t-sunny"].set_alpha(255)
                screen.blit(images["t-sunny"], (0, 0))
            elif level2_weather == "rainy":
                images["t-rainy"].set_alpha(255)
                screen.blit(images["t-rainy"], (0, 0))
            elif level2_weather == "sourrain":
                sour_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                sour_overlay.fill((140, 160, 60)) 
                sour_overlay.set_alpha(100) 
                screen.blit(sour_overlay, (0, 0))
            
            if is_counting_down:
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                overlay.fill((128, 128, 128))
                overlay.set_alpha(150)
                screen.blit(overlay, (0, 0))
                
                time_rem = 3 - int((current_time - countdown_start_time) / 1000)
                if time_rem > 0:
                    count_text = countdown_font.render(str(time_rem), True, WHITE)
                    count_rect = count_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                    screen.blit(count_text, count_rect)

            if alphas["level2_number"] > 0:
                draw_level_number(2, alphas["level2_number"])
            
            if alphas["level2_timer"] > 0:
                draw_game_timer(level2_time_left, alphas["level2_timer"])
            
            # --- Level 2 进度条布局 (上2 下1) ---
            if level2_game_active:
                bar_width = 350
                # 修改：增加间距，避免遮挡
                spacing = 180
                total_w = bar_width * 2 + spacing
                row1_start_x = (SCREEN_WIDTH - total_w) // 2
                
                # 第一行：Sunlight (Collect) | Rain (Collect)
                draw_progress_bar_custom(level2_sunlight_collected, LEVEL2_SUNLIGHT_REQUIRED, 255, "icon_sun", row1_start_x, SCREEN_HEIGHT - 160, bar_width, 20)
                draw_progress_bar_custom(level2_rain_collected, LEVEL2_RAIN_REQUIRED, 255, "icon_drop", row1_start_x + bar_width + spacing, SCREEN_HEIGHT - 160, bar_width, 20)

                # 第二行：Sourrain (Damage)
                row2_start_x = (SCREEN_WIDTH - bar_width) // 2
                draw_progress_bar_custom(level2_sourrain_damage, LEVEL2_SOURRAIN_TOLERANCE, 255, "icon_heart", row2_start_x, SCREEN_HEIGHT - 100, bar_width, 20, is_damage=True)
            
            if level2_weather == "rainy" and len(raindrops) > 0 and not is_counting_down:
                raindrop_img = images["t-raindrop"]
                raindrop_img.set_alpha(255)
                for drop in raindrops:
                    screen.blit(raindrop_img, (drop["x"], drop["y"]))

            elif level2_weather == "sourrain" and len(sourraindrops) > 0 and not is_counting_down:
                sourraindrop_img = images["sourraindrop"]
                sourraindrop_img.set_alpha(255)
                for drop in sourraindrops:
                    screen.blit(sourraindrop_img, (drop["x"], drop["y"]))
        
        elif step == 26:
            if (level2_sunlight_collected >= LEVEL2_SUNLIGHT_REQUIRED and 
                level2_rain_collected >= LEVEL2_RAIN_REQUIRED):
                blit_alpha("t-1", (0, 0))
                pos_f_x = (SCREEN_WIDTH - images["3-f"].get_width()) // 2 + 20
                pos_f_y = SCREEN_HEIGHT - images["3-f"].get_height() - 200
                blit_alpha("3-f", (pos_f_x, pos_f_y))
                if alphas["level2_intro_text"] > 0:
                    draw_styled_text_box("The bud has turned into a flower.", alphas["level2_intro_text"])
            else:
                blit_alpha("1-baselose", (0, 0))
                pos_f_x = (SCREEN_WIDTH - images["2-f-l"].get_width()) // 2 + 20
                pos_f_y = SCREEN_HEIGHT - images["2-f-l"].get_height() - 200
                blit_alpha("2-f-l", (pos_f_x, pos_f_y))
                if alphas["prompt_fail_l2"] > 0:
                    draw_styled_text_box("You lost. The bud dies. Click to try again.", alphas["prompt_fail_l2"])

        # ====================================================
        # 第三关绘制 (NEW)
        # ====================================================
        
        if step >= 27 and step < 31:
             # --- 背景绘制 ---
            if alphas["1-sunny"] > 0:
                blit_alpha("1-sunny", (0, 0))
            if alphas["1-rainy"] > 0:
                blit_alpha("1-rainy", (0, 0))
                if len(raindrops) > 0:
                    raindrop_img = images["t-raindrop"]
                    raindrop_img.set_alpha(alphas["1-rainy"])
                    for drop in raindrops:
                        screen.blit(raindrop_img, (drop["x"], drop["y"]))
            if alphas["1-sourrain"] > 0:
                blit_alpha("1-sourrain", (0, 0))
                if len(sourraindrops) > 0:
                    sourraindrop_img = images["sourraindrop"]
                    sourraindrop_img.set_alpha(alphas["1-sourrain"])
                    for drop in sourraindrops:
                        screen.blit(sourraindrop_img, (drop["x"], drop["y"]))
            
             # --- 鸟屎 Intro ---
            if alphas["birdshit"] > 0:
                bird_img = images["birdshit"]
                bird_img.set_alpha(alphas["birdshit"])
                screen.blit(bird_img, (bird_intro_x - bird_img.get_width() // 2, bird_intro_y))

            # --- 花朵绘制 ---
            flower_alpha = max(alphas["1-sunny"], alphas["1-rainy"], alphas["1-sourrain"])
            if flower_alpha > 0:
                scale_ratio = 2/3
                orig_w = images["3-f"].get_width()
                orig_h = images["3-f"].get_height()
                scaled_flower = pygame.transform.smoothscale(images["3-f"], (int(orig_w * scale_ratio), int(orig_h * scale_ratio)))
                scaled_flower.set_alpha(flower_alpha)
                pos_f_x = (SCREEN_WIDTH - scaled_flower.get_width()) // 2
                pos_f_y = SCREEN_HEIGHT - scaled_flower.get_height() - 277
                screen.blit(scaled_flower, (pos_f_x, pos_f_y))

            # --- 文字绘制 ---
            if alphas["level3_text"] > 0:
                draw_level_text("Level 3", alphas["level3_text"])
            
            # 统一介绍文字
            if alphas["level3_intro_text"] > 0:
                draw_styled_text_box("The fragile flower needs rain and sun. Protect it from both sourrain and crow droppings — listen for the caw and block quickly!", alphas["level3_intro_text"])

        elif step == 31:
            blit_alpha("t-1", (0, 0))
            
            pos_f_x = (SCREEN_WIDTH - images["3-f"].get_width()) // 2 + 15
            pos_f_y = SCREEN_HEIGHT - images["3-f"].get_height() - 200
            blit_alpha("3-f", (pos_f_x, pos_f_y))

            center_x = SCREEN_WIDTH // 2 + 10
            center_y = SCREEN_HEIGHT - images["t-l"].get_height() + 200 
            hand_l_x = center_x - images["t-l"].get_width() - arm_position_offset - 30
            hand_l_y = center_y 
            blit_alpha("t-l", (hand_l_x, hand_l_y))
            hand_r_x = center_x + arm_position_offset + 30
            hand_r_y = center_y 
            blit_alpha("t-r", (hand_r_x, hand_r_y))

            if is_counting_down:
                 images["t-sunny"].set_alpha(255)
                 screen.blit(images["t-sunny"], (0, 0))
            elif level3_weather == "sunny":
                images["t-sunny"].set_alpha(255)
                screen.blit(images["t-sunny"], (0, 0))
            elif level3_weather == "rainy":
                images["t-rainy"].set_alpha(255)
                screen.blit(images["t-rainy"], (0, 0))
            elif level3_weather == "sourrain":
                sour_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                sour_overlay.fill((140, 160, 60)) 
                sour_overlay.set_alpha(100) 
                screen.blit(sour_overlay, (0, 0))
            
            if is_counting_down:
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                overlay.fill((128, 128, 128))
                overlay.set_alpha(150)
                screen.blit(overlay, (0, 0))
                
                time_rem = 3 - int((current_time - countdown_start_time) / 1000)
                if time_rem > 0:
                    count_text = countdown_font.render(str(time_rem), True, WHITE)
                    count_rect = count_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                    screen.blit(count_text, count_rect)

            # 鸟屎绘制
            if bird_active and alphas["birdshit"] > 0:
                bird_img = images["birdshit"]
                bird_img.set_alpha(alphas["birdshit"])
                screen.blit(bird_img, (bird_x - bird_img.get_width() // 2, bird_y))

            if alphas["level3_number"] > 0:
                draw_level_number(3, alphas["level3_number"])
            
            if alphas["level3_timer"] > 0:
                draw_game_timer(level3_time_left, alphas["level3_timer"])

            # 鸟经过提示文字 (显示在顶部)
            if alphas["level3_intro_text"] > 0:
                draw_top_text("The bird is coming!", alphas["level3_intro_text"])

            # --- Level 3 进度条布局 (上2 下1) ---
            if level3_game_active:
                bar_width = 350
                # 修改：增加间距，避免遮挡
                spacing = 180
                total_w = bar_width * 2 + spacing
                row1_start_x = (SCREEN_WIDTH - total_w) // 2
                
                # 第一行：Sunlight (Collect) | Rain (Collect)
                draw_progress_bar_custom(level3_sunlight_collected, LEVEL3_SUNLIGHT_REQUIRED, 255, "icon_sun", row1_start_x, SCREEN_HEIGHT - 160, bar_width, 20)
                draw_progress_bar_custom(level3_rain_collected, LEVEL3_RAIN_REQUIRED, 255, "icon_drop", row1_start_x + bar_width + spacing, SCREEN_HEIGHT - 160, bar_width, 20)

                # 第二行：Sourrain (Damage)
                row2_start_x = (SCREEN_WIDTH - bar_width) // 2
                draw_progress_bar_custom(level3_sourrain_damage, LEVEL3_SOURRAIN_TOLERANCE, 255, "icon_heart", row2_start_x, SCREEN_HEIGHT - 100, bar_width, 20, is_damage=True)


            if level3_weather == "rainy" and len(raindrops) > 0 and not is_counting_down:
                raindrop_img = images["t-raindrop"]
                raindrop_img.set_alpha(255)
                for drop in raindrops:
                    screen.blit(raindrop_img, (drop["x"], drop["y"]))

            elif level3_weather == "sourrain" and len(sourraindrops) > 0 and not is_counting_down:
                sourraindrop_img = images["sourraindrop"]
                sourraindrop_img.set_alpha(255)
                for drop in sourraindrops:
                    screen.blit(sourraindrop_img, (drop["x"], drop["y"]))

        # Step 32: 第三关失败
        elif step == 32:
            blit_alpha("1-baselose", (0, 0))
            pos_f_x = (SCREEN_WIDTH - images["3-f-l"].get_width()) // 2 + 20
            pos_f_y = SCREEN_HEIGHT - images["3-f-l"].get_height() - 200
            blit_alpha("3-f-l", (pos_f_x, pos_f_y))
            
            if alphas["level3_prompt_fail"] > 0:
                 draw_styled_text_box("You lost. The flower dies. Click to try again.", alphas["level3_prompt_fail"])

        # Step 33 & 34: 最终结局
        elif step == 33 or step == 34:
             if alphas["E-1"] > 0:
                 blit_alpha("E-1", (0, 0))
                 if alphas["ending_text_1"] > 0:
                     draw_styled_text_box("Congratulations, your flower is already in full bloom!", alphas["ending_text_1"])
            
             if alphas["E-2"] > 0:
                 blit_alpha("E-2", (0, 0))
                 if alphas["ending_text_2"] > 0:
                     # 绘制大号 Ending 文字 (左下角框)
                     draw_styled_text_box("Happy Ending", alphas["ending_text_2"], style="bottom_left", font=ui_big_font, offset=(80, -100))
            
        # 点击关闭窗口
        if alphas["ending_text_2"] >= 255 and click_event:
            running = False


        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()