from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

# --- HTML TEMPLATES ---

BASE_STYLE = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=Poppins:wght@300;400;500&display=swap');

    body {
        background-color: #fce4ec; /* Soft pink background */
        font-family: 'Poppins', sans-serif;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        margin: 0;
        color: #4a4a4a;
    }
    .card {
        background: #fdfbf7;
        padding: 40px 30px;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        text-align: center;
        width: 350px;
        position: relative;
        transition: all 0.3s ease;
    }
    h1, h2 {
        font-family: 'Playfair Display', serif;
        color: #b33951;
        margin-bottom: 20px;
        font-size: 24px;
    }
    p {
        font-size: 14px;
        color: #888;
        margin-bottom: 25px;
    }
    .profile-pic {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        object-fit: cover;
        border: 3px solid #fff;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        margin-bottom: 15px;
    }
    .btn {
        border: none;
        padding: 12px 25px;
        border-radius: 25px;
        font-family: 'Poppins', sans-serif;
        font-weight: 500;
        font-size: 14px;
        cursor: pointer;
        transition: all 0.2s ease;
        margin: 5px;
        text-decoration: none;
        display: inline-block;
    }
    .btn-yes {
        background-color: #e05a6d;
        color: white;
    }
    .btn-yes:hover {
        background-color: #c94b5d;
        transform: scale(1.05);
    }
    .btn-no {
        background-color: #9b7ebd;
        color: white;
        position: relative; /* For JS movement */
    }
    .btn-continue {
        background-color: #e05a6d;
        color: white;
        width: 80%;
    }
    .icon-circle {
        width: 60px;
        height: 60px;
        background-color: #fce4ec;
        border-radius: 50%;
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 0 auto 20px;
        font-size: 24px;
    }
    .grid-options {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 15px;
        margin-top: 20px;
    }
    .option-btn {
        background: #fff;
        border: 1px solid #eee;
        padding: 15px;
        border-radius: 12px;
        cursor: pointer;
        transition: all 0.2s;
        font-size: 14px;
    }
    .option-btn:hover {
        border-color: #e05a6d;
        background: #fff5f7;
    }
    .calendar-grid {
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        gap: 5px;
        margin-top: 20px;
    }
    .calendar-day {
        padding: 10px;
        border-radius: 8px;
        cursor: pointer;
        font-size: 13px;
    }
    .calendar-day:hover {
        background: #fce4ec;
        color: #b33951;
    }
    .time-list {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 10px;
        margin-top: 20px;
    }
</style>
"""

# 1. THE INITIAL ASK PAGE
ASK_PAGE = BASE_STYLE + """
<div class="card" id="ask-card">
    <img src="https://i.pravatar.cc/150?img=47" alt="Crush" class="profile-pic">
    <h2>Will you go on a date with me?</h2>
    <p>🌸</p>
    <div style="position: relative; height: 50px;">
        <button class="btn btn-yes" onclick="window.location.href='/confirmed'">YES ♡</button>
        <button class="btn btn-no" id="no-btn" onmouseover="moveButton()" onclick="alert('Nice try! 😂')">no 😢</button>
    </div>
</div>

<script>
    // Fun JavaScript to make the "No" button run away
    function moveButton() {
        const btn = document.getElementById('no-btn');
        const x = Math.random() * 100 - 50;
        const y = Math.random() * 100 - 50;
        btn.style.transform = `translate(${x}px, ${y}px)`;
    }
</script>
"""

# 2. CONFIRMED PAGE
CONFIRMED_PAGE = BASE_STYLE + """
<div class="card">
    <div class="icon-circle">🎉</div>
    <h2>Wait, you really said yes?? 🤭</h2>
    <p>Ngl I was fully prepared for a no 😅</p>
    <a href="/date-picker" class="btn btn-continue">pick a date & time →</a>
</div>
"""

# 3. DATE PICKER PAGE
DATE_PAGE = BASE_STYLE + """
<div class="card">
    <div class="icon-circle">📅</div>
    <h2>when's the date? 🗓️</h2>
    <p>pick a day, any day.</p>
    
    <div style="display: flex; justify-content: space-between; font-size: 12px; color: #b33951; font-weight: bold; margin-bottom: 10px;">
        <span>September 2026</span>
    </div>
    
    <div class="calendar-grid">
        <div style="color:#ccc">S</div><div style="color:#ccc">M</div><div style="color:#ccc">T</div><div style="color:#ccc">W</div><div style="color:#ccc">T</div><div style="color:#ccc">F</div><div style="color:#ccc">S</div>
        <div style="color:#ccc">1</div><div style="color:#ccc">2</div><div style="color:#ccc">3</div><div style="color:#ccc">4</div><div style="color:#ccc">5</div><div style="color:#ccc">6</div><div style="color:#ccc">7</div>
        <div style="color:#ccc">8</div><div style="color:#ccc">9</div>
        <div class="calendar-day" style="background:#fce4ec; color:#b33951;" onclick="window.location.href='/time-picker'">10</div>
        <div class="calendar-day" onclick="window.location.href='/time-picker'">11</div>
        <div class="calendar-day" onclick="window.location.href='/time-picker'">12</div>
        <div class="calendar-day" onclick="window.location.href='/time-picker'">13</div>
        <div class="calendar-day" onclick="window.location.href='/time-picker'">14</div>
        <div class="calendar-day" onclick="window.location.href='/time-picker'">15</div>
        <div class="calendar-day" onclick="window.location.href='/time-picker'">16</div>
    </div>
</div>
"""

# 4. TIME PICKER PAGE
TIME_PAGE = BASE_STYLE + """
<div class="card">
    <div class="icon-circle">⏰</div>
    <h2>what time works? 🕐</h2>
    <p>September 12, 2026 — pick a time</p>
    
    <div class="time-list">
        <button class="option-btn" onclick="window.location.href='/food'">11:00 AM</button>
        <button class="option-btn" onclick="window.location.href='/food'">11:30 AM</button>
        <button class="option-btn" onclick="window.location.href='/food'">12:00 PM</button>
        <button class="option-btn" onclick="window.location.href='/food'">12:30 PM</button>
        <button class="option-btn" onclick="window.location.href='/food'">1:00 PM</button>
        <button class="option-btn" onclick="window.location.href='/food'">1:30 PM</button>
        <button class="option-btn" onclick="window.location.href='/food'">5:00 PM</button>
        <button class="option-btn" onclick="window.location.href='/food'">5:30 PM</button>
        <button class="option-btn" onclick="window.location.href='/food'">6:00 PM</button>
        <button class="option-btn" onclick="window.location.href='/food'">6:30 PM</button>
        <button class="option-btn" onclick="window.location.href='/food'">7:00 PM</button>
        <button class="option-btn" onclick="window.location.href='/food'">7:30 PM</button>
    </div>
</div>
"""

# 5. FOOD PICKER PAGE
FOOD_PAGE = BASE_STYLE + """
<div class="card">
    <h2>What are we chopping? 🍽️✨</h2>
    <p>pick your vibe.</p>
    
    <div class="grid-options">
        <button class="option-btn" onclick="window.location.href='/ready'">🍚 Jollof Rice</button>
        <button class="option-btn" onclick="window.location.href='/ready'">🍢 Suya</button>
        <button class="option-btn" onclick="window.location.href='/ready'">🥣 Amala & Ewedu</button>
        <button class="option-btn" onclick="window.location.href='/ready'">🍩 Puff-Puff</button>
        <button class="option-btn" onclick="window.location.href='/ready'">🍿 Small Chops</button>
        <button class="option-btn" onclick="window.location.href='/ready'">🌯 Shawarma</button>
    </div>
</div>
"""

# 6. FINAL READY PAGE
READY_PAGE = BASE_STYLE + """
<div class="card">
    <h2 style="font-size: 22px;">glad you didn't say no.</h2>
    <h2 style="font-size: 22px;">be ready by 7, I'm coming to get you 🚗</h2>
    
    <p style="font-size: 11px; margin-top: 30px; line-height: 1.6;">
        P.S. normal people text. I made a website on Build3, during lunch, for you. no big deal.
    </p>
    <div style="color: #e05a6d; letter-spacing: 5px; margin-bottom: 20px;">♥ ♥ ♥ ♥</div>
    <button class="btn btn-continue" onclick="alert('See you then! 😉')">ok I accept 😛</button>
</div>
"""

# --- FLASK ROUTES ---

@app.route('/')
def index():
    return render_template_string(ASK_PAGE)

@app.route('/confirmed')
def confirmed():
    return render_template_string(CONFIRMED_PAGE)

@app.route('/date-picker')
def date_picker():
    return render_template_string(DATE_PAGE)

@app.route('/time-picker')
def time_picker():
    return render_template_string(TIME_PAGE)

@app.route('/food')
def food():
    return render_template_string(FOOD_PAGE)

@app.route('/ready')
def ready():
    return render_template_string(READY_PAGE)

if __name__ == '__main__':
    # Run the app in debug mode so you can see changes live
    app.run(debug=True, port=5000)
