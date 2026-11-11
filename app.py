
import streamlit as st
import pygame
import random
import time
from pathlib import Path
from datetime import datetime, timedelta


# -------------------------------
# PAGE CONFIGURATION
# -------------------------------

st.set_page_config(
    page_title="MINDBREAKER",
    page_icon="🧠",
    layout="centered"
)


# -------------------------------
# SETTINGS
# -------------------------------

REMINDER_INTERVAL = 10  # Change to 60 for 1 minute

BASE_DIR = Path(__file__).resolve().parent
ALARM_FILE = BASE_DIR / "alarm.mp3"


# -------------------------------
# AUDIO SYSTEM
# -------------------------------

@st.cache_resource
def initialize_audio():
    pygame.mixer.init()
    return pygame


def play_alarm():
    try:
        if not ALARM_FILE.exists():
            return False, "alarm.mp3 was not found."

        audio = initialize_audio()

        if not audio.mixer.music.get_busy():
            audio.mixer.music.load(str(ALARM_FILE))
            audio.mixer.music.play(-1)

        return True, None

    except Exception as error:
        return False, str(error)


def stop_alarm():
    try:
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()

    except Exception:
        pass


# -------------------------------
# REMINDER TOGGLE CALLBACK
# -------------------------------

def handle_reminder_toggle():

    # WHEN TURNED OFF
    if not st.session_state.reminders_enabled:

        stop_alarm()

        st.session_state.alarm_active = False
        st.session_state.audio_error = None

        st.session_state.last_reminder = time.time()

        st.session_state.current_message = (
            "Automatic reminders are currently OFF."
        )

    # WHEN TURNED ON
    else:

        stop_alarm()

        st.session_state.alarm_active = False
        st.session_state.audio_error = None

        # Start a fresh countdown
        st.session_state.last_reminder = time.time()

        st.session_state.current_message = (
            "Welcome back! Stay focused!"
        )


# -------------------------------
# RANDOM REMINDER MESSAGES
# -------------------------------

reminders = [
    "Stop scrolling! Your future needs your attention.",
    "Ayaw kalimti imong goals. Balik sa imong study!",
    "Small progress is still progress. Keep going!",
    "Your dreams won't build themselves. Take action!",
    "Focus now. Enjoy the results later.",
    "Facebook can wait. Your future cannot!",
    "Discipline today, success tomorrow.",
    "You started for a reason. Don't give up!"
]


# -------------------------------
# SESSION STATE
# -------------------------------

if "last_reminder" not in st.session_state:
    st.session_state.last_reminder = time.time()

if "current_message" not in st.session_state:
    st.session_state.current_message = (
        "Stay focused! Your journey starts with one step."
    )

if "reminder_count" not in st.session_state:
    st.session_state.reminder_count = 0

if "alarm_active" not in st.session_state:
    st.session_state.alarm_active = False

if "reminders_enabled" not in st.session_state:
    st.session_state.reminders_enabled = True

if "audio_error" not in st.session_state:
    st.session_state.audio_error = None


# -------------------------------
# MAIN INTERFACE
# -------------------------------

st.title("🧠 MINDBREAKER")

st.subheader("STOP SCROLLING. START BUILDING.")

st.write(
    "Your personal study and productivity reminder."
)

st.divider()


# -------------------------------
# REMINDER ON / OFF CONTROL
# -------------------------------

st.header("⚙️ Reminder Settings")

st.toggle(
    "Enable Automatic Reminders",
    key="reminders_enabled",
    on_change=handle_reminder_toggle
)

if st.session_state.reminders_enabled:
    st.success("Automatic reminders are ON.")
else:
    st.warning(
        "Automatic reminders are OFF. Enjoy your break!"
    )


st.divider()


# -------------------------------
# REMINDER SYSTEM
# -------------------------------

st.header("🔥 Your Daily Reminder")


@st.fragment(run_every="1s")
def reminder_system():

    # AUTOMATIC REMINDERS
    if st.session_state.reminders_enabled:

        current_time = time.time()

        elapsed = (
            current_time - st.session_state.last_reminder
        )

        if elapsed >= REMINDER_INTERVAL:

            # Generate random reminder
            message = random.choice(reminders)

            st.session_state.current_message = message
            st.session_state.last_reminder = current_time
            st.session_state.reminder_count += 1

            # Start looping alarm
            success, error = play_alarm()

            st.session_state.alarm_active = success
            st.session_state.audio_error = error

            st.toast(
                "🧠 MINDBREAKER: Time to refocus!"
            )

    # DISPLAY CURRENT REMINDER
    st.info(st.session_state.current_message)

    # ALARM CONTROLS
    if st.session_state.alarm_active:

        st.error("🔊 ALARM IS RINGING!")

        if st.button(
            "🛑 STOP ALARM",
            type="primary",
            use_container_width=True
        ):

            stop_alarm()

            st.session_state.alarm_active = False
            st.session_state.audio_error = None

            st.success("Alarm stopped!")

    elif st.session_state.audio_error:

        st.warning(
            "Audio could not play: "
            + st.session_state.audio_error
        )

    elif not ALARM_FILE.exists():

        st.caption(
            "Add alarm.mp3 beside app.py "
            "to enable alarm sound."
        )

    # COUNTDOWN
    if st.session_state.reminders_enabled:

        elapsed = (
            time.time() - st.session_state.last_reminder
        )

        remaining = max(
            0,
            REMINDER_INTERVAL - elapsed
        )

        next_reminder = (
            datetime.now()
            + timedelta(seconds=remaining)
        )

        st.caption(
            "Next reminder: "
            + next_reminder.strftime("%I:%M:%S %p")
        )

    else:

        st.caption(
            "Automatic reminder countdown is paused."
        )

    # REMINDER COUNTER
    st.caption(
        f"Reminders delivered: "
        f"{st.session_state.reminder_count}"
    )


reminder_system()


st.divider()


# -------------------------------
# MANUAL REMINDER
# -------------------------------

st.header("💡 Manual Reminder")

if st.button(
    "🧠 Give me a reminder now",
    use_container_width=True
):

    st.session_state.current_message = random.choice(
        reminders
    )

    st.session_state.last_reminder = time.time()

    st.session_state.reminder_count += 1

    success, error = play_alarm()

    st.session_state.alarm_active = success
    st.session_state.audio_error = error

    st.rerun()


# -------------------------------
# FOOTER
# -------------------------------

st.divider()

st.caption(
    "MINDBREAKER v2.0 | Stay focused. Build your future."
)
