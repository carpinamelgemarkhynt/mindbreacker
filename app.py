
import streamlit as st
import time
import random
from datetime import datetime
from zoneinfo import ZoneInfo

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="MINDBREAKER",
    page_icon="🧠",
    layout="centered"
)

# ==========================================
# SETTINGS
# ==========================================

REMINDER_INTERVAL = 60
PH_TIMEZONE = ZoneInfo("Asia/Manila")

REMINDER_MESSAGES = [
    "🧠 Stop scrolling. Start focusing!",
    "📚 Your goals need your attention.",
    "🔥 Focus now. Your future self will thank you.",
    "💪 Discipline is choosing what matters.",
    "⏳ Don't waste your precious time.",
    "🎯 One task at a time. Keep going!",
    "📖 Get back to studying. You can do it!"
]

# ==========================================
# SESSION STATE
# ==========================================

defaults = {
    "last_reminder": time.time(),
    "current_message": "Welcome to MINDBREAKER! Stay focused.",
    "reminder_count": 0,
    "alarm_active": False,
    "alarm_reason": "",
    "reminders_enabled": True,
    "timer_running": False,
    "timer_deadline": None
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ==========================================
# ALARM FUNCTIONS
# ==========================================

def trigger_alarm(reason):
    st.session_state.alarm_active = True
    st.session_state.alarm_reason = reason


def stop_alarm():
    st.session_state.alarm_active = False
    st.session_state.alarm_reason = ""


# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

/* Hide number input plus and minus buttons */
div[data-testid="stNumberInput"] button {
    display: none !important;
}

/* Hide browser number input spinners */
div[data-testid="stNumberInput"] input::-webkit-inner-spin-button,
div[data-testid="stNumberInput"] input::-webkit-outer-spin-button {
    -webkit-appearance: none;
    margin: 0;
}

div[data-testid="stNumberInput"] input {
    -moz-appearance: textfield;
    text-align: center;
    font-size: 25px;
    font-weight: bold;
}

/* Main title */
.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
}

/* Clock */
.digital-clock {
    text-align: center;
    font-size: 35px;
    font-weight: bold;
}

/* Timer display */
.timer-display {
    text-align: center;
    font-size: 48px;
    font-weight: bold;
    padding: 15px;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# HEADER
# ==========================================

st.markdown(
    '<div class="main-title">🧠 MINDBREAKER</div>',
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align:center;'>Stop scrolling. Start focusing.</p>",
    unsafe_allow_html=True
)

st.divider()


# ==========================================
# PHILIPPINE DIGITAL CLOCK
# ==========================================

@st.fragment(run_every=1)
def live_clock():
    now = datetime.now(PH_TIMEZONE)

    st.markdown(
        f"""
        <div class="digital-clock">
            {now.strftime("%I:%M:%S %p")}
        </div>
        <p style="text-align:center;">
            {now.strftime("%A, %B %d, %Y")}
        </p>
        """,
        unsafe_allow_html=True
    )


st.subheader("🕒 Philippine Time")
live_clock()

st.divider()


# ==========================================
# DIGITAL STUDY ALARM SETTINGS
# ==========================================

st.subheader("⏰ Digital Study Timer")

st.write("Enter your desired study duration.")

col1, col2, col3 = st.columns(3)

with col1:
    alarm_hours = st.number_input(
        "Hours",
        min_value=0,
        max_value=9999,
        value=0,
        step=1,
        key="alarm_hours"
    )

with col2:
    alarm_minutes = st.number_input(
        "Minutes",
        min_value=0,
        max_value=59,
        value=0,
        step=1,
        key="alarm_minutes"
    )

with col3:
    alarm_seconds = st.number_input(
        "Seconds",
        min_value=0,
        max_value=59,
        value=0,
        step=1,
        key="alarm_seconds"
    )

total_seconds = (
    alarm_hours * 3600
    + alarm_minutes * 60
    + alarm_seconds
)

st.caption(
    f"Selected duration: "
    f"{alarm_hours:02d}:{alarm_minutes:02d}:{alarm_seconds:02d}"
)

start_col, cancel_col = st.columns(2)

with start_col:
    if st.button(
        "▶️ START TIMER",
        type="primary",
        use_container_width=True
    ):

        if total_seconds <= 0:
            st.warning("Please enter a valid timer duration.")

        else:
            st.session_state.timer_deadline = (
                time.time() + total_seconds
            )

            st.session_state.timer_running = True

            stop_alarm()

            st.session_state.current_message = (
                "📚 Your study timer has started. Stay focused!"
            )

            st.success("Your study timer has started!")

with cancel_col:
    if st.button(
        "⏹️ CANCEL TIMER",
        use_container_width=True
    ):

        st.session_state.timer_running = False
        st.session_state.timer_deadline = None

        st.info("Your timer has been cancelled.")


# ==========================================
# TIMER COUNTDOWN
# ==========================================

@st.fragment(run_every=1)
def study_timer():

    if st.session_state.timer_running:

        remaining = (
            st.session_state.timer_deadline - time.time()
        )

        if remaining <= 0:

            st.session_state.timer_running = False
            st.session_state.timer_deadline = None

            st.session_state.current_message = (
                "⏰ Your study session is finished!"
            )

            trigger_alarm("Your study timer is finished!")

            st.rerun()

        else:

            remaining = int(remaining)

            hours = remaining // 3600
            minutes = (remaining % 3600) // 60
            seconds = remaining % 60

            st.markdown(
                f"""
                <div class="timer-display">
                    {hours:02d}:{minutes:02d}:{seconds:02d}
                </div>
                """,
                unsafe_allow_html=True
            )

            st.caption("⏳ Timer is running...")

    else:

        st.markdown(
            """
            <div class="timer-display">
                00:00:00
            </div>
            """,
            unsafe_allow_html=True
        )

        st.caption("Timer is not running.")


study_timer()

st.divider()


# ==========================================
# AUTOMATIC REMINDERS
# ==========================================

st.subheader("🔔 Automatic Reminders")

st.session_state.reminders_enabled = st.toggle(
    "Enable automatic reminders",
    value=st.session_state.reminders_enabled
)


@st.fragment(run_every=1)
def automatic_reminders():

    if st.session_state.reminders_enabled:

        elapsed = (
            time.time() - st.session_state.last_reminder
        )

        if elapsed >= REMINDER_INTERVAL:

            message = random.choice(REMINDER_MESSAGES)

            st.session_state.current_message = message
            st.session_state.last_reminder = time.time()
            st.session_state.reminder_count += 1

            trigger_alarm(message)

            st.rerun()


automatic_reminders()

st.info(st.session_state.current_message)

st.caption(
    f"Total reminders: {st.session_state.reminder_count}"
)

# ==========================================
# MANUAL REMINDER
# ==========================================

if st.button(
    "🔔 REMIND ME NOW",
    use_container_width=True
):

    message = random.choice(REMINDER_MESSAGES)

    st.session_state.current_message = message
    st.session_state.reminder_count += 1
    st.session_state.last_reminder = time.time()

    trigger_alarm(message)

    st.rerun()


# ==========================================
# AUTOMATIC BROWSER ALARM
# ==========================================

if st.session_state.alarm_active:

    st.error(
        "🔊 ALARM: " + st.session_state.alarm_reason
    )

    st.components.v1.html(
        """
        <!DOCTYPE html>
        <html>
        <body>
        <script>

        const AudioContextClass =
            window.AudioContext || window.webkitAudioContext;

        if (!window.alarmContext) {
            window.alarmContext = new AudioContextClass();
        }

        const ctx = window.alarmContext;

        async function startAlarm() {

            try {

                await ctx.resume();

                if (window.alarmInterval) {
                    return;
                }

                function beep(frequency, delay) {

                    const oscillator = ctx.createOscillator();
                    const gain = ctx.createGain();

                    oscillator.type = "square";
                    oscillator.frequency.value = frequency;

                    const startTime = ctx.currentTime + delay;

                    gain.gain.setValueAtTime(0.15, startTime);
                    gain.gain.setValueAtTime(0.15, startTime + 0.3);
                    gain.gain.setValueAtTime(0, startTime + 0.4);

                    oscillator.connect(gain);
                    gain.connect(ctx.destination);

                    oscillator.start(startTime);
                    oscillator.stop(startTime + 0.4);
                }

                function ring() {
                    beep(1000, 0);
                    beep(1500, 0.5);
                }

                ring();

                window.alarmInterval = setInterval(ring, 1300);

            } catch (error) {

                console.log("Browser audio playback was blocked:", error);

            }
        }

        startAlarm();

        </script>
        </body>
        </html>
        """,
        height=0
    )

    if st.button(
        "🛑 STOP ALARM",
        type="primary",
        use_container_width=True
    ):

        stop_alarm()
        st.rerun()


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.markdown(
    """
    <div style="text-align:center;">
        <b>MINDBREAKER</b><br>
        <small>Stay focused. Stay disciplined. Keep improving.</small>
    </div>
    """,
    unsafe_allow_html=True
)
