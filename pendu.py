import random
import getpass

# =========================
# 1️⃣ Charger le dictionnaire local
# =========================
try:
    with open("francais.txt", "r", encoding="utf-8") as f:
        dictionnaire = [mot.strip().lower() for mot in f.readlines()]
except FileNotFoundError:
    print("⚠️ Le dictionnaire est introuvable. Assurez vous que le fichier 'francais.txt' est téléchargé.")
    dictionnaire = ["python", "ordinateur", "classe", "fonction", "variable"]

# =========================
# 2️⃣ Initialisation du jeu
# =========================
DEFAULT_SCORE = 15
DEFAULT_LEVEL = 2

score = DEFAULT_SCORE
level = DEFAULT_LEVEL
lettres_trouvees = []
lettres_proposees = []

# Mot de passe admin
ADMIN_PASSWORD = "admin123"

# --------------------------
# Fonctions utilitaires
# --------------------------
def filtrer_mots(level):
    if level == 1:
        return [mot for mot in dictionnaire if 4 <= len(mot) <= 6]
    elif level == 2:
        return [mot for mot in dictionnaire if 7 <= len(mot) <= 9]
    elif level == 3:
        return [mot for mot in dictionnaire if len(mot) >= 10]
    else:
        return [mot for mot in dictionnaire if len(mot) >= 4]

def choisir_mot(level):
    mots_valides = filtrer_mots(level)
    return random.choice(mots_valides)

def afficher_mot(mot, lettres_trouvees):
    """Affiche le mot avec les lettres trouvées et des '_' pour les lettres manquantes"""
    return ' '.join([lettre if lettre in lettres_trouvees else '_' for lettre in mot])

# Choisir le premier mot
mot_a_deviner = choisir_mot(level)

# =========================
# 3️⃣ Boucle principale du jeu
# =========================
while score > 0:
    print("\nMot à deviner :", afficher_mot(mot_a_deviner, lettres_trouvees))
    print(f"Score restant : {score}")
    print("Lettres déjà proposées :", ', '.join(sorted(lettres_proposees)))
    print(f"Niveau actuel : {level}")

    reponse = input("Propose une lettre ou un mot (utilise cette commande :'mot_TON MOT') : ").lower().strip()

    if reponse in ["end", "exit"]:
        print("👋 Tu as quitté le jeu.")
        break

    # --------------------------
    # Commandes admin
    # --------------------------
    if reponse.startswith("adm_"):
        mdp = getpass.getpass("🗝 ️Mot de passe admin : ").strip()
        if mdp != ADMIN_PASSWORD:
            print("❌ Mot de passe incorrect ! Commande refusée.")
            continue

        if reponse == "adm_help":
            print("""
🛠️ Commandes admin disponibles :
- adm_help : afficher cette aide
- adm_lifes_<nombre> : changer le nombre de vies/points (ex: adm_lifes_20)
- adm_level_<niveau> : changer le niveau (1, 2 ou 3) et relancer une manche
- adm_word_<mot> : choisir un mot personnalisé
- adm_reset : réinitialiser le jeu (score, niveau, mot)
- adm_end : arrêter le jeu immédiatement
""")
            continue

        # changer nombre de vies/points
        if reponse.startswith("adm_lifes_"):
            try:
                new_score = int(reponse.split("_")[-1])
                score = new_score
                print(f"✅ Nombre de vies/points changé à {score}.")
            except ValueError:
                print("⚠️ Valeur invalide pour adm_lifes.")
            continue

        # changer niveau et relancer une manche
        if reponse.startswith("adm_level_"):
            try:
                new_level = int(reponse.split("_")[-1])
                if new_level in [1, 2, 3]:
                    level = new_level
                    mot_a_deviner = choisir_mot(level)
                    lettres_trouvees = []
                    lettres_proposees = []
                    score = DEFAULT_SCORE
                    print(f"✅ Niveau changé à {level}. Nouveau mot choisi ! Score réinitialisé.")
                else:
                    print("⚠️ Niveau invalide, choix : 1, 2 ou 3.")
            except ValueError:
                print("⚠️ Valeur invalide pour adm_level.")
            continue

        # choisir un mot personnalisé
        if reponse.startswith("adm_word_"):
            mot_a_deviner = reponse.split("_", 2)[-1].lower()
            lettres_trouvees = []
            lettres_proposees = []
            score = DEFAULT_SCORE
            print(f"✍️ Nouveau mot défini par l'admin ({len(mot_a_deviner)} lettres). Score réinitialisé.")
            continue

        # reset complet
        if reponse == "adm_reset":
            score = DEFAULT_SCORE
            level = DEFAULT_LEVEL
            lettres_trouvees = []
            lettres_proposees = []
            mot_a_deviner = choisir_mot(level)
            print("🔄 Tout a été remis par défaut ! Nouvelle partie lancée.")
            continue

        # arrêter le jeu
        if reponse == "adm_end":
            print("⏹️ Jeu arrêté par l'admin !")
            break

    # --------------------------
    # Deviner un mot entier
    # --------------------------
    elif reponse.startswith("mot_"):
        mot_propose = reponse[4:]
        if mot_propose == mot_a_deviner:
            lettres_trouvees = list(mot_a_deviner)
            print("🎉 Bravo ! Tu as trouvé le mot entier !")
            break
        else:
            score -= 2
            print("❌ Mauvais mot ! -2 points.")

    # --------------------------
    # Deviner une lettre
    # --------------------------
    elif len(reponse) == 1:
        if reponse in lettres_proposees:
            print("ℹ️ Tu as déjà proposé cette lettre !")
        else:
            lettres_proposees.append(reponse)
            if reponse in mot_a_deviner:
                lettres_trouvees.append(reponse)
                print("✅ Bonne lettre !")
            else:
                score -= 1
                print("❌ Mauvaise lettre ! -1 point.")

    # --------------------------
    # Entrée invalide
    # --------------------------
    else:
        print("⚠️ Entrée invalide. Propose une lettre, 'mot_xxx', ou commande admin.")

    # --------------------------
    # Vérifier si toutes les lettres sont trouvées
    # --------------------------
    if all(lettre in lettres_trouvees for lettre in mot_a_deviner):
        print("🎉 Félicitations ! Tu as trouvé toutes les lettres !")
        break

# Fin du jeu
if score <= 0:
    print(f"💀 Game Over ! Le mot était : {mot_a_deviner}")

print(f"🏆 Score final : {score} | Niveau final : {level}")
  
