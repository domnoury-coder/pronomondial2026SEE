> c:\users\domno\documents\install.py(1)<module>()
----> 1 import streamlit as st
      2 import sqlite3
      3 from db import conn, c, hash_password
      4 
      5 st.set_page_config(page_title="Pronostics Entreprise 2026", layout="wide")

st.set_page_config(page_title="Pronostics Entreprise 2026", layout="wide")

# =========================
# AUTH
# =========================
def login(user, pwd):
    c.execute("SELECT password, role FROM users WHERE username=?", (user,))
    data = c.fetchone()
    if data and data[0] == hash_password(pwd):
        return data[1]
    return None

# =========================
# INIT ADMIN DEFAULT
# =========================
def init_admin():
    c.execute("SELECT * FROM users WHERE username='admin'")
    if not c.fetchone():
        c.execute(
            "INSERT INTO users VALUES (?, ?, ?)",
            ("admin", hash_password("admin123"), "admin")
        )
        conn.commit()

init_admin()

# =========================
# SESSION
# =========================
if "user" not in st.session_state:
    st.session_state.user = None
    st.session_state.role = None

# =========================
# LOGIN PAGE
# =========================
if not st.session_state.user:
    st.title("🔐 Connexion Pronostics Entreprise")

    user = st.text_input("Utilisateur")
    pwd = st.text_input("Mot de passe", type="password")

    if st.button("Connexion"):
        role = login(user, pwd)
        if role:
            st.session_state.user = user
            st.session_state.role = role
            st.success("Connecté")
        else:
            st.error("Identifiants incorrects")

    st.stop()

# =========================
# MENU
# =========================
menu = st.sidebar.selectbox("Menu", [
    "Pronostics",
    "Classement",
    "Admin (résultats)"
])

# =========================
# PRONOSTICS
# =========================
if menu == "Pronostics":
    st.title("🎯 Pronostics")

    match_id = st.number_input("Match ID", 1, 104)
    pa = st.number_input("Score équipe A", 0)
    pb = st.number_input("Score équipe B", 0)

    if st.button("Valider"):
        c.execute("""
        INSERT INTO bets VALUES (?, ?, ?, ?)
        """, (st.session_state.user, match_id, pa, pb))
        conn.commit()
        st.success("Pronostic enregistré")

# =========================
# CLASSEMENT
# =========================
elif menu == "Classement":
    st.title("🏆 Classement")

    c.execute("""
    SELECT username,
    SUM(
        CASE
            WHEN prono_a = score_a AND prono_b = score_b THEN 5
            WHEN (prono_a > prono_b AND score_a > score_b)
              OR (prono_a < prono_b AND score_a < score_b)
              OR (prono_a = prono_b AND score_a = score_b)
            THEN 3
            ELSE 0
        END
    ) as points
    FROM bets
    JOIN matches ON bets.match_id = matches.id
    GROUP BY username
    ORDER BY points DESC
    """)

    data = c.fetchall()
    st.dataframe(data)

# =========================
# ADMIN
# =========================
elif menu == "Admin (résultats)":
    if st.session_state.role != "admin":
        st.error("Accès refusé")
        st.stop()

    st.title("⚙️ Admin - Résultats matchs")

    match_id = st.number_input("Match ID", 1, 104)
    sa = st.number_input("Score A", 0)
    sb = st.number_input("Score B", 0)

    if st.button("Enregistrer résultat"):
        c.execute("""
        INSERT OR REPLACE INTO matches VALUES (?, '', '', ?, ?)
        """, (match_id, sa, sb))
        conn.commit()
        st.success("Mis à jour") 