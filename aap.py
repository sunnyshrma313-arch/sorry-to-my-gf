import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Stop Crying & Play!", page_icon="🎮")

# --- GAME LOGIC IN JAVASCRIPT ---
game_html = """
<div id="game-container" style="text-align: center; font-family: sans-serif; background: #fff5f5; padding: 20px; border-radius: 15px;">
    <h2 id="status">Round 1: Reach Her! 💖</h2>
    <canvas id="gameCanvas" width="400" height="400" style="border: 2px solid #ffb6c1; background: white; cursor: none;"></canvas>
    <p style="color: #666; margin-top: 10px;">Move the <b>Blue Circle</b> to the <b>Pink Circle</b></p>
</div>

<script>
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const status = document.getElementById('status');

let round = 1;
let player = { x: 50, y: 50, radius: 15, color: '#007bff' }; // Manjot (Blue)
let target = { x: 300, y: 300, radius: 15, color: '#ff69b4' }; // Swan (Pink)
let speed = 0;
let gameOver = false;

canvas.addEventListener('mousemove', (e) => {
    if (gameOver) return;
    const rect = canvas.getBoundingClientRect();
    player.x = e.clientX - rect.left;
    player.y = e.clientY - rect.top;
});

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    if (!gameOver) {
        // Update target movement based on round
        if (round > 1 && round < 5) {
            target.x += (Math.random() - 0.5) * (round * 5);
            target.y += (Math.random() - 0.5) * (round * 5);
        } else if (round === 5) {
            target.x += (Math.random() - 0.5) * 60; // 10x Harder
            target.y += (Math.random() - 0.5) * 60;
        }

        // Keep target inside canvas
        target.x = Math.max(target.radius, Math.min(canvas.width - target.radius, target.x));
        target.y = Math.max(target.radius, Math.min(canvas.height - target.radius, target.y));

        // Draw Player
        ctx.beginPath();
        ctx.arc(player.x, player.y, player.radius, 0, Math.PI * 2);
        ctx.fillStyle = player.color;
        ctx.fill();
        ctx.closePath();

        // Draw Target
        ctx.beginPath();
        ctx.arc(target.x, target.y, target.radius, 0, Math.PI * 2);
        ctx.fillStyle = target.color;
        ctx.fill();
        ctx.closePath();

        // Collision detection
        const dist = Math.sqrt((player.x - target.x)**2 + (player.y - target.y)**2);
        if (dist < player.radius + target.radius) {
            if (round < 5) {
                round++;
                status.innerText = "Round " + round + (round === 5 ? ": 10x HARDER! 🔥" : ": Faster! 🏃‍♀️");
                // Reset positions
                target.x = Math.random() * 300 + 50;
                target.y = Math.random() * 300 + 50;
            } else {
                gameOver = true;
                status.innerHTML = "<span style='color:green;'>YOU WON! ❤️ Game Complete.</span>";
                window.parent.postMessage({type: 'game_complete'}, '*');
            }
        }
        requestAnimationFrame(draw);
    }
}
draw();
</script>
"""

# --- DISPLAY GAME ---
if 'won' not in st.session_state:
    st.session_state.won = False

# Listen for game completion
# Note: In Streamlit, we use a trick to catch JS events
st.write("### Oye! Rona band karo aur ye game jeet kar dikhao... 😤")
components.html(game_html, height=550)

# Instruction to trigger the "Sorry" page manually since JS-to-Python trigger is tricky in basic Streamlit
if st.button("I Won! (Click here after Round 5) 🏆"):
    st.session_state.won = True

# --- FINAL SORRY WEBSITE (SADA SA VERSION) ---
if st.session_state.won:
    st.divider()
    st.balloons()
    st.title("Ab Sunno... I am Sorry! ❤️")
    
    st.write(f"""
    Mujhe pata hai main thoda zyada gussa kar gaya tha. 
    Par sach toh ye hai ki jab aap bimar hoti ho aur andhere mein akele bahar jati ho, 
    toh mujhe bhot dar lagta hai. 
    """)
    
    st.info("aapko 'Gwaar' bolne ke liye I am really sorry. Main aapkii care karta hoon isliye pagal ho jata hoon. 🙏")
    
    st.markdown("---")
    st.subheader("Promise karo:")
    st.write("1. Agli baar se akele andhere mein nahi jaogi.")
    st.write("2. Apni tabiyat ka dhyan rakhogi.")
    
    st.success("Ab rona band karo aur ek smile do! 😊")
    st.caption("— Tumhara Manjot (Delhi Wala) 😎")
