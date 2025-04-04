import streamlit as st
import random
import string

# Common weak passwords that should be avoided
blacklist = [
    "password", "123456", "qwerty", "letmein", "password123", "admin", "welcome",
    "abc123", "iloveyou", "111111", "123123", "passw0rd"
]

# Evaluate password strength
def evaluate_password(password):
    score = 0
    suggestions = []

    if password.lower() in blacklist:
        return 0, ["Avoid using common passwords like 'password123', 'admin', etc."]

    if len(password) >= 8:
        score += 1
    else:
        suggestions.append("Make your password at least 8 characters long.")

    if any(c.isupper() for c in password):
        score += 1
    else:
        suggestions.append("Add at least one uppercase letter (A-Z).")

    if any(c.islower() for c in password):
        score += 1
    else:
        suggestions.append("Add at least one lowercase letter (a-z).")

    if any(c.isdigit() for c in password):
        score += 1
    else:
        suggestions.append("Include at least one number (0-9).")

    special_chars = "!@#$%^&*"
    if any(c in special_chars for c in password):
        score += 1
    else:
        suggestions.append("Add at least one special character (!@#$%^&*).")

    return score, suggestions

# Strength label based on score
def get_strength_label(score):
    if score <= 2:
        return "Weak", "❌"
    elif 3 <= score <= 4:
        return "Moderate", "⚠️"
    else:
        return "Strong", "✅"

# Generate a strong password
def generate_strong_password(length=12):
    if length < 8:
        length = 8

    characters = (
        string.ascii_uppercase +
        string.ascii_lowercase +
        string.digits +
        "!@#$%^&*"
    )

    password = [
        random.choice(string.ascii_uppercase),
        random.choice(string.ascii_lowercase),
        random.choice(string.digits),
        random.choice("!@#$%^&*")
    ]

    password += random.choices(characters, k=length - 4)
    random.shuffle(password)

    return ''.join(password)

# Streamlit UI
st.set_page_config(page_title="Password Strength Meter", page_icon="🔐")

st.title("🔐 Password Strength Meter")

password_input = st.text_input("Enter your password", type="password")

if password_input:
    score, feedback = evaluate_password(password_input)
    label, emoji = get_strength_label(score)

    st.markdown(f"### {emoji} Password Strength: **{label}** (Score: {score}/5)")

    if label == "Strong":
        st.success("Your password is strong. Good job!")
    else:
        st.warning("Suggestions to improve your password:")
        for tip in feedback:
            st.write(f"- {tip}")

        st.markdown("💡 Here's a strong password you can use:")
        st.code(generate_strong_password(), language="text")
