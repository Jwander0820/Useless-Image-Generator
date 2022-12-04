# Useless Image Generator
## 一個無用的圖像生成器

### 1. 生成隨機座標隨機數字圖像

#### a. 座標全隨機
`GenerateDigitalMapGif.random_number_map()`
<div><img src=data/300x300_range_random_number_map.gif></div>

#### b. 座標取固定間格隨機
`GenerateDigitalMapGif.random_number_map()`
<div><img src=data/300x300_same_range_random_number_map.gif></div>

### 2. 生成全區域隨機數字圖像
`GenerateDigitalMapGif.full_random_number_map()`
<div><img src=data/300x300_full_range_random_number_map.gif></div>

### 3. 生成類似The Matrix(駭客任務)風格背景
`GenerateDigitalMapGif.y_flow_random_map`
<div><img src=data/300x300_y_flow_random_map.gif></div>

### 4. 生成類似DVD反彈螢幕保護程式
`GenerateDVDBounceGif.dvd_bounce_by_random_color`  **# 舊版:僅以文字碰撞**

`GenerateDVDBounceGif.dvd_bounce_with_img`  **# 新版:可以替換成自己的圖片!**
<div><img src=data/300x300_DVD_bounce_img_advanced.gif></div>

### 5. 數學幻想(?)，思考時背後運算的數學特效
`GenerateMathFantasyGif.math_fantasy`
<div><img src=data/300x300_math_fantasy.gif></div>

### 6. 數位文字圖像，大文字由隨機不斷變換的小數字構成，亦可以替換成自己的剪影(蒙版)
`GenerateDigitalTextGif.digital_text_mask`
<div><img src=data/300x300_digital_text_mask.gif></div>

### 7. 文字跑馬燈，類似新聞播報的文字跑馬燈效果，可以設定方向、文字大小與顏色、背景顏色、移動速度等
`GenerateMarquee.text_flow`
<div><img src=data/720x150_marquee_example.gif></div>
