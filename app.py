import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

# Configuration de la page
st.set_page_config(page_title="Surveillance santé maman", page_icon="❤️", layout="centered")

st.title("💖 Surveillance de la santé de maman")
st.write("Entrez vos données ci-dessous pour les suivre au quotidien.")

# Champs de saisie
systolique = st.number_input("Tension systolique (mmHg)", value=120, min_value=50, max_value=250)
diastolique = st.number_input("Tension diastolique (mmHg)", value=70, min_value=30, max_value=150)
bpm = st.number_input("Battements par minute (BPM)", value=80, min_value=30, max_value=150)

# État émotionnel
normale = st.checkbox("🙂 Normale")
joyeuse = st.checkbox("😊 Joyeuse")
anxieuse = st.checkbox("😰 Anxieuse")
stressee = st.checkbox("😖 Stressée")
fatiguee = st.checkbox("😴 Fatiguée")
changement_traitement = st.checkbox("💊 Changement de traitement")


# Historique
history_file = "historique.csv"

def lire_historique():
    if os.path.exists(history_file):
        return pd.read_csv(history_file, parse_dates=["Date"])
    else:
        return pd.DataFrame(columns=[
    "Date", "Systolique", "Diastolique", "BPM",
    "Normale", "Joyeuse", "Anxieuse", "Stressée", "Fatiguée", "Changement traitement"
])

def sauvegarder_mesure(date, sys, dia, bpm, joy, anx, stress, fat, chang):
    df = lire_historique()
    nouvelle_ligne = {
    "Date": date,
    "Systolique": sys,
    "Diastolique": dia,
    "BPM": bpm,
    "Normale": normale,
    "Joyeuse": joy,
    "Anxieuse": anx,
    "Stressée": stress,
    "Fatiguée": fat,
    "Changement traitement": chang
}

    nouvelle_df = pd.DataFrame([nouvelle_ligne])
    df = pd.concat([df, nouvelle_df], ignore_index=True)
    df.to_csv(history_file, index=False)

# Analyse
if st.button("Analyser"):
    anomalies = []

if not (120 <= systolique <= 139):
    anomalies.append("Systolique hors de la plage normale (120-139 mmHg)")
if not (70 <= diastolique <= 89):
    anomalies.append("Diastolique hors de la plage normale (70-89 mmHg)")
 
    if bpm < 65:
        anomalies.append("Rythme cardiaque trop lent")
    elif bpm > 100:
        anomalies.append("Rythme cardiaque trop rapide")

    if anomalies:
        st.error("⚠️ DANGER : " + ", ".join(anomalies))
    else:
        st.success("🎉 Super maman ! Toutes les valeurs sont normales.")

    # Détails
    st.write("### Détails :")
    st.write(f"Tension systolique : {systolique} mmHg")
    st.write(f"Tension diastolique : {diastolique} mmHg")
    st.write(f"BPM : {bpm}")

    # Sauvegarde
    now = datetime.now()
    sauvegarder_mesure(now, systolique, diastolique, bpm, joyeuse, anxieuse, stressee, fatiguee, changement_traitement)

# Affichage historique
df = lire_historique()

if not df.empty:
    st.write("## 📈 Historique des mesures")

    df = df.sort_values("Date")
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(df["Date"], df["Systolique"], label="Systolique", marker="o")
    ax.plot(df["Date"], df["Diastolique"], label="Diastolique", marker="o")
    ax.plot(df["Date"], df["BPM"], label="BPM", marker="o")
    ax.set_title("Historique de la tension et du cœur")
    ax.set_xlabel("Date")
    ax.set_ylabel("Valeurs")
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)

    # Affichage des émotions
    st.write("### État émotionnel relevé")
    st.dataframe(df[["Date", "Normale", "Joyeuse", "Anxieuse", "Stressée", "Fatiguée", "Changement traitement"]])

else:
    st.info("Aucun historique encore. Entrez une mesure pour commencer.")

# ----- 📤 ENVOI D'EMAIL - VERSION TEMPORAIRE -----
def envoyer_email(destinataire, fichier_csv):
    st.warning("📧 L'envoi d'e-mail n'est pas encore activé. Tu pourras le configurer plus tard ici.")
    return False

# Zone envoi mail
st.write("---")
st.write("## 📤 Envoi à un médecin (à activer plus tard)")
email_medecin = st.text_input("Adresse e-mail du médecin")
if st.button("Envoyer l'historique par e-mail"):
    if not email_medecin:
        st.warning("Veuillez entrer une adresse e-mail.")
    elif not os.path.exists(history_file):
        st.error("Aucun fichier d’historique à envoyer.")
    else:
        envoyer_email(email_medecin, history_file)


