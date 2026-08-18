"""Frozen Unable to Reach letter text from the Rohit sample PDF.

Only Date, Name, and A-number change when the frontend calls this API.
Every other line stays exactly as printed in the sample.
"""

from typing import Any

Span = dict[str, Any]

# Signature block is always Fremont, matching the sample letter.
SIGNATURE_OFFICE = [
    "3155 Kearney St, Suite 248",
    "Fremont, CA 94538",
]

HEADER_OFFICES = [
    {
        "align": "left",
        "lines": [
            "108-14, Jamaica Ave",
            "Richmond Hill, NY 11418",
            "Tel: (718) 533-8444",
            "Fax: (718) 533-8460",
        ],
    },
    {
        "align": "center",
        "lines": [
            "3155 Kearney St, Suite 248",
            "Fremont, CA 94538",
            "Tel: (510) 657-6444",
            "Fax: (510) 657-6443",
        ],
    },
    {
        "align": "right",
        "lines": [
            "5855 Auburn Blvd.",
            "Sacramento, CA 95841",
            "Tel: (916) 226-4189",
            "Fax: (510) 657-6443",
        ],
    },
]

CONTACT_NUMBERS = "510-657-6444, 718-657-6444, 916-513-2660"

LETTERS: dict[str, dict[str, Any]] = {
    "english": {
        "font": "Times New Roman",
        "complex_script": False,
        "bidi_lang": "en-US",
        "date_label": "Date:",
        "name_label": "Name :",
        "a_number_label": "A #:",
        "subject": "Subject : Urgent – Unable to Contact You Regarding Your Case",
        "salutation": "Dear Sir/Madam,",
        "paragraphs": [
            [
                {
                    "text": (
                        "The Law Office of Jaspreet Singh has made several attempts to "
                        "contact you regarding your immigration case using the phone number "
                        "you provided. Unfortunately, we have been unable to reach you."
                    )
                }
            ],
            [
                {
                    "text": (
                        "Your prompt communication is necessary so we can continue working "
                        "on your case. If we do not hear from you, we may have no "
                        "choice but to "
                    )
                },
                {"text": "withdraw as your attorneys of record", "bold": True},
                {"text": ", which could negatively affect your case."},
            ],
            [
                {
                    "text": (
                        "Please contact our office immediately upon receiving this letter "
                        "by calling any of the following numbers: "
                    )
                },
                {"text": CONTACT_NUMBERS, "bold": True},
            ],
            [
                {
                    "text": (
                        "You may also visit our nearby office during regular business hours. "
                        "If you have already contacted our office, please disregard this notice."
                    )
                }
            ],
            [
                {
                    "text": (
                        "We appreciate your prompt attention to this matter and look forward "
                        "to hearing from you."
                    )
                }
            ],
        ],
        "closing": "Sincerely,",
        "signatory_name": "Jaspreet Singh, Esq.",
        "signatory_firm": "Law Office of Jaspreet Singh",
        "signatory_office": SIGNATURE_OFFICE,
    },
    "hindi": {
        "font": "Nirmala UI",
        "complex_script": True,
        "bidi_lang": "hi-IN",
        "date_label": "दिनांक :",
        "name_label": "नामे :",
        "a_number_label": "ए #:",
        "subject": "विषय : तत्काल - आपके मामले के संबंध में आपसे संपर्क करने में असमर्थ",
        "salutation": "प्रिय महोदय/महोदया,",
        "paragraphs": [
            [
                {
                    "text": (
                        "जसप्रीत सिंह के कानून कार्यालय ने आपके द्वारा प्रदान किए गए फोन नंबर "
                        "का उपयोग करके आपके आव्रजन मामले के संबंध में आपसे संपर्क करने के कई "
                        "प्रयास किए हैं। दुर्भाग्य से, हम आप तक पहुंचने में असमर्थ रहे हैं।"
                    )
                }
            ],
            [
                {
                    "text": (
                        "आपका त्वरित संचार आवश्यक है ताकि हम आपके मामले पर काम करना जारी रख सकें। "
                        "अगर हम आपसे नहीं सुनते हैं। हमारे पास "
                    )
                },
                {
                    "text": "आपके रिकॉर्ड के वकीलों के रूप में वापस लेने के अलावा कोई विकल्प नहीं हो सकता है",
                    "bold": True,
                },
                {"text": ", जो आपके मामले को नकारात्मक रूप से प्रभावित कर सकता है।"},
            ],
            [
                {
                    "text": (
                        "कृपया इस पत्र को प्राप्त करने के तुरंत बाद निम्नलिखित में से किसी भी "
                        "नंबर पर कॉल करके हमारे कार्यालय से संपर्क करें: "
                    )
                },
                {"text": CONTACT_NUMBERS, "bold": True},
            ],
            [
                {
                    "text": (
                        "आप नियमित व्यावसायिक घंटों के दौरान हमारे नजदीकी कार्यालय में भी जा सकते हैं। "
                        "यदि आप पहले ही हमारे कार्यालय से संपर्क कर चुके हैं, तो कृपया इस नोटिस की "
                        "अवहेलना करें।"
                    )
                }
            ],
            [
                {
                    "text": (
                        "हम इस मामले पर आपके त्वरित ध्यान की सराहना करते हैं और आपसे सुनने के लिए "
                        "उत्सुक हैं।"
                    )
                }
            ],
        ],
        "closing": "भवदीय",
        "signatory_name": "जसप्रीत सिंह, एस्क।",
        "signatory_firm": "लॉ ऑफिस ऑफ जसप्रीत सिंह",
        "signatory_office": SIGNATURE_OFFICE,
    },
    "punjabi": {
        "font": "Nirmala UI",
        "complex_script": True,
        "bidi_lang": "pa-IN",
        "date_label": "ਮਿਤੀ :",
        "name_label": "ਨਾਮ :",
        "a_number_label": "ਏ #:",
        "subject": "ਵਿਸ਼ਾ : ਤੁਰੰਤ - ਤੁਹਾਡੇ ਕੇਸ ਸਬੰਧੀ ਤੁਹਾਡੇ ਨਾਲ ਸੰਪਰਕ ਕਰਨ ਵਿੱਚ ਅਸਮਰੱਥ",
        "salutation": "ਪਿਆਰੇ ਮਹੋਦਯ/ਮਹੋਦਯਾ,",
        "paragraphs": [
            [
                {
                    "text": (
                        "ਜਸਪ੍ਰੀਤ ਸਿੰਘ ਦੇ ਕਾਨੂੰਨ ਦਫ਼ਤਰ ਨੇ ਤੁਹਾਡੇ ਵੱਲੋਂ ਦਿੱਤੇ ਗਏ ਫੋਨ ਨੰਬਰ ਦੀ ਵਰਤੋਂ "
                        "ਕਰਕੇ ਤੁਹਾਡੇ ਇਮੀਗ੍ਰੇਸ਼ਨ ਕੇਸ ਸਬੰਧੀ ਤੁਹਾਡੇ ਨਾਲ ਸੰਪਰਕ ਕਰਨ ਦੀਆਂ ਕਈ ਕੋਸ਼ਿਸ਼ਾਂ "
                        "ਕੀਤੀਆਂ ਹਨ। ਬਦਕਿਸਮਤੀ ਨਾਲ, ਅਸੀਂ ਤੁਹਾਡੇ ਤੱਕ ਪਹੁੰਚਣ ਵਿੱਚ ਅਸਮਰੱਥ ਰਹੇ ਹਾਂ।"
                    )
                }
            ],
            [
                {
                    "text": (
                        "ਤੁਹਾਡਾ ਤੁਰੰਤ ਸੰਪਰਕ ਜ਼ਰੂਰੀ ਹੈ ਤਾਂ ਜੋ ਅਸੀਂ ਤੁਹਾਡੇ ਕੇਸ ਉੱਤੇ ਕੰਮ ਜਾਰੀ ਰੱਖ "
                        "ਸਕੀਏ। ਜੇਕਰ ਅਸੀਂ ਤੁਹਾਡੇ ਤੋਂ ਨਹੀਂ ਸੁਣਦੇ। ਸਾਡੇ ਕੋਲ "
                    )
                },
                {
                    "text": "ਤੁਹਾਡੇ ਰਿਕਾਰਡ ਦੇ ਵਕੀਲਾਂ ਵਜੋਂ ਵਾਪਸ ਲੈਣ ਤੋਂ ਇਲਾਵਾ ਕੋਈ ਚੋਣ ਨਹੀਂ ਰਹਿ ਸਕਦੀ",
                    "bold": True,
                },
                {"text": ", ਜਿਸ ਨਾਲ ਤੁਹਾਡੇ ਕੇਸ ਉੱਤੇ ਮਾੜਾ ਅਸਰ ਪੈ ਸਕਦਾ ਹੈ।"},
            ],
            [
                {
                    "text": (
                        "ਕਿਰਪਾ ਕਰਕੇ ਇਹ ਪੱਤਰ ਮਿਲਣ ਤੋਂ ਤੁਰੰਤ ਬਾਅਦ ਹੇਠ ਲਿਖੇ ਕਿਸੇ ਵੀ ਨੰਬਰ ਤੇ ਕਾਲ "
                        "ਕਰਕੇ ਸਾਡੇ ਦਫ਼ਤਰ ਨਾਲ ਸੰਪਰਕ ਕਰੋ: "
                    )
                },
                {"text": CONTACT_NUMBERS, "bold": True},
            ],
            [
                {
                    "text": (
                        "ਤੁਸੀਂ ਨਿਯਮਿਤ ਕਾਰੋਬਾਰੀ ਘੰਟਿਆਂ ਦੌਰਾਨ ਸਾਡੇ ਨਜ਼ਦੀਕੀ ਦਫ਼ਤਰ ਵਿੱਚ ਵੀ ਆ ਸਕਦੇ ਹੋ। "
                        "ਜੇਕਰ ਤੁਸੀਂ ਪਹਿਲਾਂ ਹੀ ਸਾਡੇ ਦਫ਼ਤਰ ਨਾਲ ਸੰਪਰਕ ਕਰ ਚੁੱਕੇ ਹੋ, ਤਾਂ ਕਿਰਪਾ ਕਰਕੇ "
                        "ਇਸ ਨੋਟਿਸ ਨੂੰ ਅਣਡਿੱਠਾ ਕਰੋ।"
                    )
                }
            ],
            [
                {
                    "text": (
                        "ਅਸੀਂ ਇਸ ਮਾਮਲੇ ਵਿੱਚ ਤੁਹਾਡੇ ਤੁਰੰਤ ਧਿਆਨ ਦੀ ਕਦਰ ਕਰਦੇ ਹਾਂ ਅਤੇ ਤੁਹਾਡੇ ਤੋਂ "
                        "ਸੁਣਨ ਲਈ ਉਤਸੁਕ ਹਾਂ।"
                    )
                }
            ],
        ],
        "closing": "ਸਤਿਕਾਰ ਸਹਿਤ,",
        "signatory_name": "ਜਸਪ੍ਰੀਤ ਸਿੰਘ, ਐਸਕਿਊ.",
        "signatory_firm": "ਲਾਅ ਆਫਿਸ ਆਫ ਜਸਪ੍ਰੀਤ ਸਿੰਘ",
        "signatory_office": SIGNATURE_OFFICE,
    },
}
