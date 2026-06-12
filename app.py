import streamlit as st
import pandas as pd

st.set_page_config(page_title="Pronostics Mondial 2026", layout="wide")

# =========================
# INIT DATA
# =========================
if "matches" not in st.session_state:
    st.session_state.matches = pd.DataFrame({
        "id": range(1, 105),
        "equipe_a": [""] * 104,
        "equipe_b": [""] * 104,
        "score_a": [None] * 104,
        "score_b": [None] * 104
    })

if "bets" not in st.session_state:
    st.session_state.bets = pd.DataFrame(columns=[
        "joueur", "match_id", "prono_a", "prono_b"
    ])

# =========================
# CALCUL POINTS
# =========================
def calcul_points(row):
    match = st.session_state.matches.loc[
        st.session_state.matches["id"] == row["match_id"]
    ].iloc[0]

    if pd.isna(match["score_a"]) or pd.isna(match["score_b"]):
        return 0

    real_a, real_b = match["score_a"], match["score_b"]
    pa, pb = row["prono_a"], row["prono_b"]

    # score exact
    if real_a == pa and real_b == pb:
        return 5

    # bon vainqueur
    if (real_a > real_b and pa > pb) or (real_a < real_b and pa < pb) or (real_a == real_b and pa == pb):
        return 3

    return 0

# =========================
# SIDEBAR
# =========================
menu = st.sidebar.selectbox("Menu", [
    "Saisie matchs",
    "Pronostics",
    "Classement"
])

# =========================
# SAISIE MATCHS (ADMIN)
# =========================
if menu == "Saisie matchs":
    st.title("⚽ Saisie des résultats")

    edited = st.data_editor(st.session_state.matches, num_rows="dynamic")

    st.session_state.matches = edited

    st.success("Résultats mis à jour")

# =========================
# PRONOSTICS
# =========================
elif menu == "Pronostics":
    st.title("🎯 Pronostics")

    joueur = st.text_input("Nom du joueur")

    match_id = st.number_input("Match ID", 1, 104)

    col1, col2 = st.columns(2)
    with col1:
        pa = st.number_input("Score équipe A", 0)
    with col2:
        pb = st.number_input("Score équipe B", 0)

    if st.button("Valider pronostic"):
        st.session_state.bets.loc[len(st.session_state.bets)] = [
            joueur, match_id, pa, pb
        ]
        st.success("Pronostic enregistré")

# =========================
# CLASSEMENT
# =========================
elif menu == "Classement":
    st.title("🏆 Classement live")

    if len(st.session_state.bets) == 0:
        st.warning("Aucun pronostic")
    else:
        bets = st.session_state.bets.copy()
        bets["points"] = bets.apply(calcul_points, axis=1)

        classement = bets.groupby("joueur")["points"].sum().reset_index()
        classement = classement.sort_values("points", ascending=False)

        st.dataframe(classement, use_container_width=True)

        st.bar_chart(classement.set_index("joueur")) 
