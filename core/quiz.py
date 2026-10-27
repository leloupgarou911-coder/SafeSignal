"""Short, multilingual scam-awareness quiz for the Streamlit interface."""

QUIZ_QUESTIONS = {
    "fr": [
        {
            "id": 1,
            "message": "Alerte sécurité : votre accès sera suspendu ce soir. Confirmez vos identifiants via ce lien inconnu.",
            "is_scam": True,
            "explanation": "Les menaces de suspension et les liens inattendus sont des signaux de phishing. Ouvrez vous-même l’application ou le site officiel pour vérifier.",
        },
        {
            "id": 2,
            "message": "Votre facture mensuelle est disponible dans votre espace client. Ouvrez l’application officielle comme d’habitude.",
            "is_scam": False,
            "explanation": "Cet exemple est moins suspect : il invite à ouvrir l’application habituelle sans fournir de lien inconnu. Cela ne prouve toutefois pas l’authenticité du message.",
        },
        {
            "id": 3,
            "message": "VIRUS DÉTECTÉ ! Appelez immédiatement le numéro affiché dans cette fenêtre pour débloquer votre ordinateur.",
            "is_scam": True,
            "explanation": "Une fenêtre d’alerte qui pousse à appeler un numéro est un signal fréquent de faux support technique. Ne rappelez pas ce numéro ; vérifiez avec les outils de sécurité connus.",
        },
    ],
    "en": [
        {
            "id": 1,
            "message": "Security alert: your access will be suspended tonight. Confirm your login through this unfamiliar link.",
            "is_scam": True,
            "explanation": "Suspension threats and unexpected links are phishing signals. Open the official app or website yourself to check.",
        },
        {
            "id": 2,
            "message": "Your monthly bill is available in your account. Open the official app as you normally do.",
            "is_scam": False,
            "explanation": "This example is less suspicious because it directs you to your usual app instead of an unfamiliar link. That alone does not prove the message is authentic.",
        },
        {
            "id": 3,
            "message": "VIRUS DETECTED! Call the number in this pop-up immediately to unlock your computer.",
            "is_scam": True,
            "explanation": "A pop-up urging you to call a number is a common fake-support signal. Do not call it; check with security tools you already trust.",
        },
    ],
    "ar": [
        {
            "id": 1,
            "message": "تنبيه أمني: سيتم تعليق دخولك الليلة. أكد بيانات الدخول عبر هذا الرابط غير المعروف.",
            "is_scam": True,
            "explanation": "التهديد بتعليق الحساب والروابط غير المتوقعة من مؤشرات التصيد. افتح التطبيق أو الموقع الرسمي بنفسك للتحقق.",
        },
        {
            "id": 2,
            "message": "فاتورتك الشهرية متاحة في حسابك. افتح التطبيق الرسمي كالمعتاد.",
            "is_scam": False,
            "explanation": "هذا المثال أقل إثارة للشك لأنه يطلب فتح التطبيق المعتاد بدلاً من رابط مجهول. لكن ذلك لا يثبت وحده صحة الرسالة.",
        },
        {
            "id": 3,
            "message": "تم اكتشاف فيروس! اتصل فوراً بالرقم الظاهر في هذه النافذة لفتح جهاز الكمبيوتر.",
            "is_scam": True,
            "explanation": "النافذة التي تضغط عليك للاتصال برقم قد تكون دعماً تقنياً مزيفاً. لا تتصل به؛ تحقق باستخدام أدوات أمان موثوقة لديك.",
        },
    ],
}


def get_quiz(lang="fr"):
    """Return the quiz for a supported interface language, falling back to French."""
    return QUIZ_QUESTIONS.get(lang, QUIZ_QUESTIONS["fr"])
