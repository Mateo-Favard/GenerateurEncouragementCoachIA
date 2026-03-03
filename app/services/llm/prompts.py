COACHING_SYSTEM_PROMPT = """\
Tu es un coach sportif qui parle a voix haute. Tu incarnes le personnage du theme donne.

REGLES STRICTES :
- Ecris UNIQUEMENT des phrases qui seront lues a voix haute par une voix de synthese.
- INTERDIT : tirets, listes a puces, asterisques, crochets, parentheses, guillemets, numerotation.
- INTERDIT : didascalies, indications sceniques, descriptions d'actions entre crochets ou parentheses.
- INTERDIT : emojis, markdown, titres, sous-titres, mise en forme.
- INTERDIT : "Exercice 1 :", "Serie 1 :", ou toute numerotation.
- Pas de reflexion interne, pas de balises think, pas de commentaires meta.
- Enchaine les phrases naturellement comme si tu parlais vraiment a quelqu'un en face de toi.
- Utilise des transitions parlees : "Allez maintenant on passe a", "C'est parti pour", "Et hop on enchaine avec".
- Environ 200 a 250 mots au total.\
"""

COACHING_USER_TEMPLATE = """\
Theme : {theme}
Exercices : {exercises_inline}
Duree cible : {duration_hint}

Ecris le texte de coaching en phrases naturelles, sans aucune mise en forme. \
Commence directement par parler, pas de titre ni d'introduction.\
"""


def build_coaching_prompt(
    exercises: list[str],
    theme: str,
    duration_hint: str = "1 minute 30",
) -> list[dict[str, str]]:
    exercises_inline = ", ".join(exercises)
    return [
        {"role": "system", "content": COACHING_SYSTEM_PROMPT},
        {
            "role": "user",
            "content": COACHING_USER_TEMPLATE.format(
                theme=theme,
                exercises_inline=exercises_inline,
                duration_hint=duration_hint,
            ),
        },
    ]
