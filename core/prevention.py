"""Multilingual, practical scam-prevention guides for the Streamlit UI."""

GUIDES = {
    "fr": [
        {
            "id": "phishing", "icon": "🎣", "title": "Phishing / hameçonnage",
            "summary": "Des messages qui imitent un service connu pour voler des identifiants ou des données.",
            "checklist": [
                "Vérifiez l’adresse complète de l’expéditeur, pas seulement son nom affiché.",
                "Évitez les liens qui imposent une vérification urgente ou menacent de bloquer un compte.",
                "Un organisme légitime ne doit pas vous demander votre mot de passe ou un code de validation par message.",
            ],
            "legit_label": "Exemple potentiellement légitime",
            "legit": "Votre relevé est disponible dans votre espace client. Ouvrez l’application officielle comme d’habitude.",
            "scam_label": "Exemple suspect",
            "scam": "URGENT : votre compte sera bloqué dans 2 heures. Vérifiez vos identifiants via un lien inconnu.",
        },
        {
            "id": "parcel", "icon": "📦", "title": "Faux colis et frais de livraison",
            "summary": "Un SMS prétend qu’un colis est bloqué et demande un petit paiement ou des données bancaires.",
            "checklist": [
                "Demandez-vous si vous attendez réellement un colis.",
                "Consultez le suivi depuis l’application ou le site officiel que vous ouvrez vous-même.",
                "Méfiez-vous des frais inattendus, même très faibles, et des liens avec un domaine inhabituel.",
            ],
            "legit_label": "Exemple potentiellement légitime",
            "legit": "Le suivi est consultable dans l’application officielle du transporteur avec votre numéro de colis.",
            "scam_label": "Exemple suspect",
            "scam": "Votre colis est retenu. Payez immédiatement des frais de livraison sur ce lien inconnu.",
        },
        {
            "id": "bank", "icon": "📞", "title": "Faux conseiller bancaire",
            "summary": "Un appelant prétend protéger votre compte et vous pousse à valider une opération.",
            "checklist": [
                "Ne validez pas une opération pour l’« annuler » sur instruction d’un appelant.",
                "Le numéro affiché peut être falsifié : son apparence ne prouve pas l’identité de l’appelant.",
                "Raccrochez et rappelez votre banque au numéro officiel de votre carte ou de son site.",
            ],
            "legit_label": "Réflexe plus sûr",
            "legit": "Vous contactez votre banque vous-même via l’application officielle ou le numéro connu.",
            "scam_label": "Exemple suspect",
            "scam": "Je suis du service antifraude : validez cette notification pour bloquer le paiement frauduleux.",
        },
        {
            "id": "tech_support", "icon": "🖥️", "title": "Faux support technique",
            "summary": "Une fausse alerte affirme que l’appareil est infecté et demande d’appeler ou d’installer un outil.",
            "checklist": [
                "Une fenêtre surgissante ne prouve pas qu’un appareil est infecté.",
                "N’appelez pas un numéro affiché dans une alerte inattendue et n’installez pas de logiciel à la demande d’un inconnu.",
                "Fermez la page si possible et utilisez les outils de sécurité déjà installés ou le site officiel du fabricant.",
            ],
            "legit_label": "Réflexe plus sûr",
            "legit": "Vous ouvrez vous-même les paramètres de sécurité ou le site officiel du fabricant pour vérifier.",
            "scam_label": "Exemple suspect",
            "scam": "VIRUS DÉTECTÉ ! Appelez immédiatement ce numéro pour éviter le blocage de votre ordinateur.",
        },
    ],
    "en": [
        {
            "id": "phishing", "icon": "🎣", "title": "Phishing and credential theft",
            "summary": "Messages imitate a known service to steal sign-in details or personal data.",
            "checklist": [
                "Check the sender's full address, not just the display name.",
                "Be wary of links demanding urgent verification or threatening account closure.",
                "Legitimate organizations should not ask for your password or verification code by message.",
            ],
            "legit_label": "Potentially legitimate example",
            "legit": "Your statement is available in your account. Open the official app as you normally do.",
            "scam_label": "Suspicious example",
            "scam": "URGENT: your account will be locked in 2 hours. Verify your login through this unfamiliar link.",
        },
        {
            "id": "parcel", "icon": "📦", "title": "Fake parcel and delivery fees",
            "summary": "A text claims a parcel is on hold and asks for a small payment or bank details.",
            "checklist": [
                "Ask yourself whether you are actually expecting a parcel.",
                "Track it through the carrier's official app or website that you open yourself.",
                "Be cautious of unexpected fees, even tiny ones, and unfamiliar domains.",
            ],
            "legit_label": "Potentially legitimate example",
            "legit": "Tracking is available in the carrier's official app using your parcel number.",
            "scam_label": "Suspicious example",
            "scam": "Your parcel is held. Pay an immediate delivery fee through this unfamiliar link.",
        },
        {
            "id": "bank", "icon": "📞", "title": "Fake bank adviser",
            "summary": "A caller claims to protect your account and pressures you to approve a transaction.",
            "checklist": [
                "Do not approve a transaction to supposedly cancel it because a caller tells you to.",
                "Caller ID can be spoofed; the displayed number does not prove who is calling.",
                "Hang up and call your bank using the official number on your card or website.",
            ],
            "legit_label": "Safer response",
            "legit": "Contact your bank yourself through its official app or a number you already trust.",
            "scam_label": "Suspicious example",
            "scam": "I am from fraud prevention: approve this notification to block the fraudulent payment.",
        },
        {
            "id": "tech_support", "icon": "🖥️", "title": "Fake technical support",
            "summary": "A fake alert claims your device is infected and tells you to call or install a tool.",
            "checklist": [
                "A pop-up does not prove your device is infected.",
                "Do not call a number shown in an unexpected alert or install software at a stranger's request.",
                "Close the page if possible and use your existing security tools or the manufacturer's official site.",
            ],
            "legit_label": "Safer response",
            "legit": "Open your device's security settings or the manufacturer's official site yourself to check.",
            "scam_label": "Suspicious example",
            "scam": "VIRUS DETECTED! Call this number immediately to prevent your computer from being locked.",
        },
    ],
    "ar": [
        {
            "id": "phishing", "icon": "🎣", "title": "التصيد الاحتيالي وسرقة بيانات الدخول",
            "summary": "رسائل تنتحل صفة خدمة معروفة لسرقة بيانات الدخول أو المعلومات الشخصية.",
            "checklist": [
                "تحقق من عنوان المرسل الكامل، وليس الاسم الظاهر فقط.",
                "احذر الروابط التي تطلب التحقق فوراً أو تهدد بإغلاق الحساب.",
                "لا ينبغي للجهات الموثوقة طلب كلمة المرور أو رمز التحقق عبر الرسائل.",
            ],
            "legit_label": "مثال قد يكون سليماً",
            "legit": "كشف الحساب متاح في حسابك. افتح التطبيق الرسمي بالطريقة المعتادة.",
            "scam_label": "مثال مريب",
            "scam": "عاجل: سيتم قفل حسابك خلال ساعتين. تحقق من بيانات الدخول عبر رابط غير معروف.",
        },
        {
            "id": "parcel", "icon": "📦", "title": "احتيال الطرود ورسوم التوصيل",
            "summary": "رسالة تزعم أن الطرد محجوز وتطلب مبلغاً صغيراً أو بيانات مصرفية.",
            "checklist": [
                "اسأل نفسك هل تنتظر طرداً بالفعل.",
                "تحقق من التتبع عبر التطبيق أو الموقع الرسمي الذي تفتحه بنفسك.",
                "احذر الرسوم غير المتوقعة ولو كانت صغيرة، والنطاقات غير المعروفة.",
            ],
            "legit_label": "مثال قد يكون سليماً",
            "legit": "يمكن متابعة الشحنة من التطبيق الرسمي لشركة النقل باستخدام رقم الطرد.",
            "scam_label": "مثال مريب",
            "scam": "طردك محجوز. ادفع رسوم التوصيل فوراً عبر هذا الرابط غير المعروف.",
        },
        {
            "id": "bank", "icon": "📞", "title": "المستشار المصرفي المزيف",
            "summary": "متصل يدعي حماية حسابك ويضغط عليك للموافقة على معاملة.",
            "checklist": [
                "لا توافق على معاملة بحجة إلغائها بناءً على تعليمات المتصل.",
                "يمكن تزوير رقم المتصل؛ فالرقم الظاهر لا يثبت هويته.",
                "أنه المكالمة واتصل بالبنك عبر الرقم الرسمي الموجود على بطاقتك أو موقعه.",
            ],
            "legit_label": "تصرف أكثر أماناً",
            "legit": "تواصل مع البنك بنفسك عبر تطبيقه الرسمي أو رقم تعرفه مسبقاً.",
            "scam_label": "مثال مريب",
            "scam": "أنا من قسم مكافحة الاحتيال: وافق على هذا الإشعار لإيقاف الدفع الاحتيالي.",
        },
        {
            "id": "tech_support", "icon": "🖥️", "title": "الدعم التقني المزيف",
            "summary": "تنبيه مزيف يدعي إصابة الجهاز ويطلب الاتصال برقم أو تثبيت برنامج.",
            "checklist": [
                "ظهور نافذة منبثقة لا يثبت أن جهازك مصاب.",
                "لا تتصل برقم في تنبيه مفاجئ ولا تثبت برنامجاً بطلب من شخص مجهول.",
                "أغلق الصفحة إن أمكن واستخدم أدوات الأمان الموجودة أو الموقع الرسمي للشركة المصنعة.",
            ],
            "legit_label": "تصرف أكثر أماناً",
            "legit": "افتح إعدادات الأمان أو الموقع الرسمي للشركة المصنعة بنفسك للتحقق.",
            "scam_label": "مثال مريب",
            "scam": "تم اكتشاف فيروس! اتصل بهذا الرقم فوراً لمنع قفل جهاز الكمبيوتر.",
        },
    ],
}


def get_guides(lang="fr"):
    """Return guides for a supported UI language, falling back safely to French."""
    return GUIDES.get(lang, GUIDES["fr"])
