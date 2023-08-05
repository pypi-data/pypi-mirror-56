import random

def random_emails(count):
    seed = int(random.random() * 10e12)
    return [
        'some{}email@domain.com'.format(a)
        for a in range(seed, seed + count)
    ]

LBAPP_ALL_FEATURES_RESPONSE = [
    {
        "id": "3Vg5Qg8",
        "gs": "staff"
    },
    {
        "id": "aQLMDyN",
        "gs": "staff"
    },
    {
        "id": "qGyN3Lo",
        "gs": "staff"
    },
    {
        "id": "5RnzKga",
        "gs": "staff"
    },
    {
        "id": "djL05np",
        "gs": "partial"
    },
    {
        "id": "mWnkGnv",
        "gs": "partial"
    },
    {
        "id": "oBLPmn3",
        "gs": "partial"
    },
    {
        "id": "plgYqgG",
        "es": [
            {
                "cmb": "OR",
                "mc": [
                    [
                        "DATE",
                        "User.signup_at",
                        "GT",
                        "8989"
                    ],
                    [
                        "DATE",
                        "User.signup_at",
                        "ISNOT",
                        "21121"
                    ],
                    [
                        "NUMERIC",
                        "User.expense",
                        "LTE",
                        "121212"
                    ],
                    [
                        "DATE",
                        "User.signup_at",
                        "GT",
                        "3333"
                    ],
                    [
                        "STRING",
                        "user.email",
                        "DNEQUAL",
                        "sdf"
                    ],
                    [
                        "STRING",
                        "user.email",
                        "STRTWITH",
                        "79898"
                    ],
                    [
                        "STRING",
                        "user.email",
                        "MATCHES",
                        "fghjkljhfgl;"
                    ],
                    [
                        "BOOLEAN",
                        "user.is_staff",
                        "IS",
                        "False"
                    ],
                    [
                        "STRING",
                        "user.email",
                        "STRTWITH",
                        "dipanjan"
                    ]
                ]
            }
        ],
        "gs": "partial",
        "ss": [
            {
                "cmb": "OR",
                "mc": [
                    [
                        "BOOLEAN",
                        "user.is_staff",
                        "ISNOT",
                        "true"
                    ],
                    [
                        "STRING",
                        "user.email",
                        "ENDSWITH",
                        "asdf"
                    ]
                ]
            },
        ]
    },
    {
        "id": "NByQPga",
        "es": [
            {
                "cmb": "OR",
                "mc": [
                    [
                        "BOOLEAN",
                        "user.is_staff",
                        "ISNOT",
                        "fghfdfgghf"
                    ],
                    [
                        "STRING",
                        "user.email",
                        "ENDSWITH",
                        "asdf"
                    ]
                ]
            }
        ],
        "gs": "partial",
        "ss": []
    }
]
