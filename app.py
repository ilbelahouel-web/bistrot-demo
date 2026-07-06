import streamlit as st
from groq import Groq

# ─── CONFIG PAGE ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Le Bistrot Parisien",
    page_icon="🍽️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ─── STYLE ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Inter:wght@300;400;500&display=swap');

    /* Fond général */
    .stApp {
        background: #0f0f0f;
        font-family: 'Inter', sans-serif;
    }

    /* Masquer les éléments Streamlit par défaut */
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding-top: 0 !important; max-width: 720px; }

    /* Header restaurant */
    .resto-header {
        text-align: center;
        padding: 2.5rem 1rem 1.5rem 1rem;
        border-bottom: 1px solid #2a2a2a;
        margin-bottom: 1.5rem;
    }
    .resto-name {
        font-family: 'Playfair Display', serif;
        font-size: 2.2rem;
        font-weight: 700;
        color: #d4a843;
        margin: 0;
        letter-spacing: 1px;
    }
    .resto-sub {
        font-size: 0.85rem;
        color: #666;
        margin-top: 0.4rem;
        letter-spacing: 0.5px;
    }

    /* Badges infos */
    .badges {
        display: flex;
        gap: 0.6rem;
        justify-content: center;
        flex-wrap: wrap;
        margin-top: 1.2rem;
    }
    .badge {
        background: #1a1a1a;
        border: 1px solid #2a2a2a;
        color: #aaa;
        font-size: 0.75rem;
        padding: 0.3rem 0.75rem;
        border-radius: 20px;
    }

    /* Messages */
    [data-testid="stChatMessage"] {
        background: transparent !important;
    }
    [data-testid="stChatMessage"][data-testid*="assistant"] {
        background: #141414 !important;
        border: 1px solid #222 !important;
        border-radius: 12px !important;
        padding: 0.75rem !important;
    }

    /* Zone de texte */
    .stChatInput > div {
        border: 1px solid #2a2a2a !important;
        border-radius: 12px !important;
        background: #141414 !important;
    }
    .stChatInput textarea {
        color: #e0e0e0 !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* Texte global */
    p, li, span, div { color: #ddd; }
    strong { color: #fff; }

    /* Ligne de séparation */
    hr { border-color: #1e1e1e; }
</style>
""", unsafe_allow_html=True)

# ─── SYSTEM PROMPT ──────────────────────────────────────────────────────────
SYSTEM_PROMPT = """Tu es l'assistant virtuel du Bistrot Parisien, un restaurant gastronomique français à Paris.

INFOS DU RESTAURANT :
- Nom : Le Bistrot Parisien
- Adresse : 12 rue de la Paix, 75002 Paris (Métro Opéra)
- Téléphone : 01 23 45 67 89
- Email : contact@bistrotparisien.fr

HORAIRES :
- Lundi → Vendredi : 12h00–14h30 et 19h00–22h30
- Samedi : 19h00–23h00
- Dimanche : Fermé

MENU — ENTRÉES :
- Soupe à l'oignon gratinée : 10€
- Salade niçoise : 12€
- Foie gras maison, toast brioché : 18€
- Carpaccio de bœuf, roquette parmesan : 14€
- Œufs mimosa truffés : 11€

MENU — PLATS :
- Bœuf bourguignon traditionnel : 24€
- Sole meunière, pommes vapeur : 28€
- Entrecôte grillée, frites maison, sauce béarnaise : 26€
- Risotto aux champignons sauvages (végétarien) : 20€
- Magret de canard, sauce orange et miel : 27€
- Tartare de bœuf, frites maison : 23€

MENU — DESSERTS :
- Crème brûlée à la vanille de Madagascar : 8€
- Tarte tatin, crème fraîche : 9€
- Mousse au chocolat noir 70% : 7€
- Profiteroles sauce chocolat chaud : 10€
- Île flottante : 7€

FORMULES :
- Formule déjeuner (lun–ven) : Entrée + Plat OU Plat + Dessert → 19€
- Formule complète : Entrée + Plat + Dessert → 26€

BOISSONS :
- Vins au verre à partir de 5€ (rouge, blanc, rosé)
- Carafe d'eau : offerte
- Café/Thé : 3€
- Jus de fruits frais : 5€

INFOS PRATIQUES :
- Végétarien : oui (risotto + options sur demande)
- Allergènes : fournis sur demande
- Parking : 200m (Parking de la Paix)
- Accès PMR : oui
- Animaux : acceptés en terrasse
- Paiements : CB, espèces, tickets restaurant, Lydia

RÉSERVATIONS :
Pour réserver, demande au client : prénom et nom, date souhaitée, heure, nombre de personnes.
Confirme ensuite chaleureusement et rappelle le numéro de téléphone si besoin.

COMPORTEMENT :
- Sois chaleureux, élégant, concis. Maximum 3-4 phrases par réponse.
- Réponds en français sauf si le client écrit dans une autre langue.
- Si tu ne sais pas, propose d'appeler le restaurant.
- Ne parle que de ce qui concerne le restaurant.
- Jamais de liste à puces. Parle naturellement, comme un maître d'hôtel attentionné.
"""

# ─── HEADER ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="resto-header">
    <p class="resto-name">🍽 Le Bistrot Parisien</p>
    <p class="resto-sub">12 rue de la Paix, Paris 2ème · Cuisine française traditionnelle</p>
    <div class="badges">
        <span class="badge">⏰ Lun–Ven 12h–22h30</span>
        <span class="badge">🗓 Sam 19h–23h</span>
        <span class="badge">📍 Métro Opéra</span>
        <span class="badge">📞 01 23 45 67 89</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── HISTORIQUE ──────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
    welcome = "Bonsoir et bienvenue au Bistrot Parisien ! 😊 Je suis votre assistant, ravi de vous accueillir. Puis-je vous renseigner sur notre menu, nos horaires, ou vous aider à réserver une table ?"
    st.session_state.messages.append({"role": "assistant", "content": welcome})

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ─── INPUT & RÉPONSE ─────────────────────────────────────────────────────────
if prompt := st.chat_input("Écrivez votre message..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])

        with st.chat_message("assistant"):
            with st.spinner(""):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    max_tokens=400,
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        *[
                            {"role": m["role"], "content": m["content"]}
                            for m in st.session_state.messages
                        ]
                    ]
                )
                reply = response.choices[0].message.content
                st.markdown(reply)

        st.session_state.messages.append({"role": "assistant", "content": reply})

    except Exception:
        st.error("Une erreur s'est produite. Vérifiez votre clé GROQ_API_KEY dans les secrets Streamlit.")
