"""
Module containing Constants, Enumerations and Other Static data
for User Models in the Application.

This module defines various functionailities that are used
throughout the application to ensure consistency in data representation.

Enums:
    - Gender: Enumeration of gender types.
    - AccountStatus: Enumeration of Account Statuses for a User.
    - AccountRole: Enumeration of Account Roles for a User.
    - AccountEmailVerification: Enumeration of Account or User Email Preferences
    - UserDevicePermission: Enumeration of Account or User Device Preferences
    - AccountLoginMethod: Enumeration of Account or User Login Preferences
    - AccountCommunication: Enumeration of Account or User Communication Preferences
    - Country: Enumeration of Account or User Country Preferences
    - Language: Enumeration of Account or User Language Preferences
    - Occupation: Enumeration of Account or User Occupation Preferences

Example:
    >>> from enums import Gender
    >>> user_gender = Gender.MALE
"""

from enum import Enum
from re import Pattern, compile as regex_compile


# KEY: Accessible using name attribute
# VALUE: Accessible using value attribute


class Status(Enum):
    """Enumeration of User Related Statuses."""

    NEW = "Newly Created."
    ACTIVE = "Actively is in Use."
    INACTIVE = "Not Actively in Use."
    DISABLED = "Can't be used."
    DELETED = "Has been Deleted."


class Role(Enum):
    """Enumeration of User Related Roles."""

    SUPER = "Super Administrator"
    SYS_ADMIN = "System Administrator"
    TESTER = "Application Tester"
    USER = "Application User"
    DEVELOPER = "Application developer"


class DateFormat(Enum):
    """Applications Permitted Date Formats."""

    SHORT = "%y/%m"  # Format 2: "24/03"
    LONG = "%d %B %Y %H:%M:%S"  # Format 1: "14 March 2024 20:05:12"
    SLASH = "%Y/%m/%d %H:%M:%S"  # Format 2: "2024/03/14 20:05:12"
    HYPHEN = "%Y-%m-%d %H:%M:%S"  # Format 3: "2024-03-14 20:05:12"


class Regex(Enum):
    """Holds Regex Constants That are Applicable to the Application."""

    EMAIL: Pattern = regex_compile(
        r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-_]+\.[a-zA-Z]+\.?[a-zA-Z]*$"
    )
    PASSWORD: Pattern = regex_compile(
        r"^(?=.*[a-zA-Z])(?=.*\d)(?=.*[!@#$%^&*()-_+=]).{8,}$"
    )
    NAME = regex_compile(r"^[a-zA-Z]{1,30}$")
    USERNAME = regex_compile(r"^[a-zA-Z][a-zA-Z0-9\s\-,._]{8,30}$")
    MOBILE_NUMBER = regex_compile(r"^\+\d{1,3}\d{3,14}$")
    DESCRIPTION = regex_compile(r"^[a-zA-Z][a-zA-Z0-9\s\-,._]{8,125}$")
    BIOGRAPHY = regex_compile(r"^(?!\s+$).{8,250}$")
    PIN = regex_compile(r"^\d{6}$")


class Gender(Enum):
    """Enumeration of Genders."""

    MALE = "male", "m"
    FEMALE = "female", "f"
    OTHER = "other", "o"


class AccountStatus(Enum):
    """Enumeration of Accounts."""

    NEW = "new"
    UNVERIFIED = "unverified"
    VERIFIED = "verified"
    ACTIVE = "active"
    DELETED = "deleted"
    DISABLED = "disabled"
    SUSPENDED = "suspended"


class Country(Enum):
    """Enumeration of Email Verification Statuses."""

    AFGHANISTAN = "Afghanistan", "AF"
    ALBANIA = "Albania", "AL"
    ALGERIA = "Algeria", "DZ"
    ANDORRA = "Andorra", "AD"
    ANGOLA = "Angola", "AO"
    ANTIGUA_AND_BARBUDA = "Antigua and Barbuda", "AG"
    ARGENTINA = "Argentina", "AR"
    ARMENIA = "Armenia", "AM"
    AUSTRALIA = "Australia", "AU"
    AUSTRIA = "Austria", "AT"
    AZERBAIJAN = "Azerbaijan", "AZ"
    BAHAMAS = "Bahamas", "BS"
    BAHRAIN = "Bahrain", "BH"
    BANGLADESH = "Bangladesh", "BD"
    BARBADOS = "Barbados", "BB"
    BELARUS = "Belarus", "BY"
    BELGIUM = "Belgium", "BE"
    BELIZE = "Belize", "BZ"
    BENIN = "Benin", "BJ"
    BHUTAN = "Bhutan", "BT"
    BOLIVIA = "Bolivia", "BO"
    BOSNIA_AND_HERZEGOVINA = "Bosnia and Herzegovina", "BA"
    BOTSWANA = "Botswana", "BW"
    BRAZIL = "Brazil", "BR"
    BRUNEI = "Brunei", "BN"
    BULGARIA = "Bulgaria", "BG"
    BURKINA_FASO = "Burkina Faso", "BF"
    BURUNDI = "Burundi", "BI"
    CABO_VERDE = "Cabo Verde", "CV"
    CAMBODIA = "Cambodia", "KH"
    CAMEROON = "Cameroon", "CM"
    CANADA = "Canada", "CA"
    CENTRAL_AFRICAN_REPUBLIC = "Central African Republic", "CF"
    CHAD = "Chad", "TD"
    CHILE = "Chile", "CL"
    CHINA = "China", "CN"
    COLOMBIA = "Colombia", "CO"
    COMOROS = "Comoros", "KM"
    CONGO_DEMOCRATIC_REPUBLIC = "Congo (Democratic Republic)", "CD"
    CONGO_REPUBLIC = "Congo (Republic)", "CG"
    COSTA_RICA = "Costa Rica", "CR"
    COTE_DIVOIRE = "Côte d'Ivoire", "CI"
    CROATIA = "Croatia", "HR"
    CUBA = "Cuba", "CU"
    CYPRUS = "Cyprus", "CY"
    CZECH_REPUBLIC = "Czech Republic", "CZ"
    DENMARK = "Denmark", "DK"
    DJIBOUTI = "Djibouti", "DJ"
    DOMINICA = "Dominica", "DM"
    DOMINICAN_REPUBLIC = "Dominican Republic", "DO"
    ECUADOR = "Ecuador", "EC"
    EGYPT = "Egypt", "EG"
    EL_SALVADOR = "El Salvador", "SV"
    EQUATORIAL_GUINEA = "Equatorial Guinea", "GQ"
    ERITREA = "Eritrea", "ER"
    ESTONIA = "Estonia", "EE"
    ESWATINI = "Eswatini", "SZ"
    ETHIOPIA = "Ethiopia", "ET"
    FIJI = "Fiji", "FJ"
    FINLAND = "Finland", "FI"
    FRANCE = "France", "FR"
    GABON = "Gabon", "GA"
    GAMBIA = "Gambia", "GM"
    GEORGIA = "Georgia", "GE"
    GERMANY = "Germany", "DE"
    GHANA = "Ghana", "GH"
    GREECE = "Greece", "GR"
    GRENADA = "Grenada", "GD"
    GUATEMALA = "Guatemala", "GT"
    GUINEA = "Guinea", "GN"
    GUINEA_BISSAU = "Guinea-Bissau", "GW"
    GUYANA = "Guyana", "GY"
    HAITI = "Haiti", "HT"
    HONDURAS = "Honduras", "HN"
    HUNGARY = "Hungary", "HU"
    ICELAND = "Iceland", "IS"
    INDIA = "India", "IN"
    INDONESIA = "Indonesia", "ID"
    IRAN = "Iran", "IR"
    IRAQ = "Iraq", "IQ"
    IRELAND = "Ireland", "IE"
    ISRAEL = "Israel", "IL"
    ITALY = "Italy", "IT"
    JAMAICA = "Jamaica", "JM"
    JAPAN = "Japan", "JP"
    JORDAN = "Jordan", "JO"
    KAZAKHSTAN = "Kazakhstan", "KZ"
    KENYA = "Kenya", "KE"
    KIRIBATI = "Kiribati", "KI"
    KOREA_NORTH = "Korea (North)", "KP"
    KOREA_SOUTH = "Korea (South)", "KR"
    KOSOVO = "Kosovo", "XK"
    KUWAIT = "Kuwait", "KW"
    KYRGYZSTAN = "Kyrgyzstan", "KG"
    LAOS = "Laos", "LA"
    LATVIA = "Latvia", "LV"
    LEBANON = "Lebanon", "LB"
    LESOTHO = "Lesotho", "LS"
    LIBERIA = "Liberia", "LR"
    LIBYA = "Libya", "LY"
    LIECHTENSTEIN = "Liechtenstein", "LI"
    LITHUANIA = "Lithuania", "LT"
    LUXEMBOURG = "Luxembourg", "LU"
    MADAGASCAR = "Madagascar", "MG"
    MALAWI = "Malawi", "MW"
    MALAYSIA = "Malaysia", "MY"
    MALDIVES = "Maldives", "MV"
    MALI = "Mali", "ML"
    MALTA = "Malta", "MT"
    MARSHALL_ISLANDS = "Marshall Islands", "MH"
    MAURITANIA = "Mauritania", "MR"
    MAURITIUS = "Mauritius", "MU"
    MEXICO = "Mexico", "MX"
    MICRONESIA = "Micronesia", "FM"
    MOLDOVA = "Moldova", "MD"
    MONACO = "Monaco", "MC"
    MONGOLIA = "Mongolia", "MN"
    MONTENEGRO = "Montenegro", "ME"
    MOROCCO = "Morocco", "MA"
    MOZAMBIQUE = "Mozambique", "MZ"
    MYANMAR = "Myanmar", "MM"
    NAMIBIA = "Namibia", "NA"
    NAURU = "Nauru", "NR"
    NEPAL = "Nepal", "NP"
    NETHERLANDS = "Netherlands", "NL"
    NEW_ZEALAND = "New Zealand", "NZ"
    NICARAGUA = "Nicaragua", "NI"
    NIGER = "Niger", "NE"
    NIGERIA = "Nigeria", "NG"
    NORTH_MACEDONIA = "North Macedonia", "MK"
    NORWAY = "Norway", "NO"
    OMAN = "Oman", "OM"
    PAKISTAN = "Pakistan", "PK"
    PALAU = "Palau", "PW"
    PALESTINE = "Palestine", "PS"
    PANAMA = "Panama", "PA"
    PAPUA_NEW_GUINEA = "Papua New Guinea", "PG"
    PARAGUAY = "Paraguay", "PY"
    PERU = "Peru", "PE"
    PHILIPPINES = "Philippines", "PH"
    POLAND = "Poland", "PL"
    PORTUGAL = "Portugal", "PT"
    QATAR = "Qatar", "QA"
    ROMANIA = "Romania", "RO"
    RUSSIA = "Russia", "RU"
    RWANDA = "Rwanda", "RW"
    SAINT_KITTS_AND_NEVIS = "Saint Kitts and Nevis", "KN"
    SAINT_LUCIA = "Saint Lucia", "LC"
    SAINT_VINCENT_AND_GRENADINES = "Saint Vincent and the Grenadines", "VC"
    SAMOA = "Samoa", "WS"
    SAN_MARINO = "San Marino", "SM"
    SAO_TOME_AND_PRINCIPE = "Sao Tome and Principe", "ST"
    SAUDI_ARABIA = "Saudi Arabia", "SA"
    SENEGAL = "Senegal", "SN"
    SERBIA = "Serbia", "RS"
    SEYCHELLES = "Seychelles", "SC"
    SIERRA_LEONE = "Sierra Leone", "SL"
    SINGAPORE = "Singapore", "SG"
    SLOVAKIA = "Slovakia", "SK"
    SLOVENIA = "Slovenia", "SI"
    SOLOMON_ISLANDS = "Solomon Islands", "SB"
    SOMALIA = "Somalia", "SO"
    SOUTH_AFRICA = "South Africa", "ZA"
    SOUTH_SUDAN = "South Sudan", "SS"
    SPAIN = "Spain", "ES"
    SRI_LANKA = "Sri Lanka", "LK"
    SUDAN = "Sudan", "SD"
    SURINAME = "Suriname", "SR"
    SWEDEN = "Sweden", "SE"
    SWITZERLAND = "Switzerland", "CH"
    SYRIA = "Syria", "SY"
    TAIWAN = "Taiwan", "TW"
    TAJIKISTAN = "Tajikistan", "TJ"
    TANZANIA = "Tanzania", "TZ"
    THAILAND = "Thailand", "TH"
    TIMOR_LESTE = "Timor-Leste", "TL"
    TOGO = "Togo", "TG"
    TONGA = "Tonga", "TO"
    TRINIDAD_AND_TOBAGO = "Trinidad and Tobago", "TT"
    TUNISIA = "Tunisia", "TN"
    TURKEY = "Turkey", "TR"
    TURKMENISTAN = "Turkmenistan", "TM"
    TUVALU = "Tuvalu", "TV"
    UGANDA = "Uganda", "UG"
    UKRAINE = "Ukraine", "UA"
    UNITED_ARAB_EMIRATES = "United Arab Emirates", "AE"
    UNITED_KINGDOM = "United Kingdom", "GB"
    UNITED_STATES = "United States", "US"
    URUGUAY = "Uruguay", "UY"
    UZBEKISTAN = "Uzbekistan", "UZ"
    VANUATU = "Vanuatu", "VU"
    VATICAN_CITY = "Vatican City", "VA"
    VENEZUELA = "Venezuela", "VE"
    VIETNAM = "Vietnam", "VN"
    YEMEN = "Yemen", "YE"
    ZAMBIA = "Zambia", "ZM"
    ZIMBABWE = "Zimbabwe", "ZW"


class Language(Enum):
    """Enumeration of Email Verification Statuses."""

    AFRIKAANS = "Afrikaans", "af"
    ALBANIAN = "Albanian", "sq"
    AMHARIC = "Amharic", "am"
    ARABIC = "Arabic", "ar"
    ARMENIAN = "Armenian", "hy"
    ASSAMESE = "Assamese", "as"
    AZERBAIJANI = "Azerbaijani", "az"
    BENGALI = "Bengali", "bn"
    BOSNIAN = "Bosnian", "bs"
    BULGARIAN = "Bulgarian", "bg"
    BURMESE = "Burmese", "my"
    CATALAN = "Catalan", "ca"
    CHINESE_MANDARIN = "Chinese (Mandarin)", "zh"
    CROATIAN = "Croatian", "hr"
    CZECH = "Czech", "cs"
    DANISH = "Danish", "da"
    DUTCH = "Dutch", "nl"
    ENGLISH = "English", "en"
    ESTONIAN = "Estonian", "et"
    FINNISH = "Finnish", "fi"
    FRENCH = "French", "fr"
    GEORGIAN = "Georgian", "ka"
    GERMAN = "German", "de"
    GREEK = "Greek", "el"
    GUJARATI = "Gujarati", "gu"
    HEBREW = "Hebrew", "he"
    HINDI = "Hindi", "hi"
    HUNGARIAN = "Hungarian", "hu"
    ICELANDIC = "Icelandic", "is"
    INDONESIAN = "Indonesian", "id"
    IRISH = "Irish", "ga"
    ITALIAN = "Italian", "it"
    JAPANESE = "Japanese", "ja"
    JAVANESE = "Javanese", "jv"
    KANNADA = "Kannada", "kn"
    KAZAKH = "Kazakh", "kk"
    KHMER = "Khmer", "km"
    KOREAN = "Korean", "ko"
    KURDISH = "Kurdish", "ku"
    KYRGYZ = "Kyrgyz", "ky"
    LAO = "Lao", "lo"
    LATVIAN = "Latvian", "lv"
    LITHUANIAN = "Lithuanian", "lt"
    MACEDONIAN = "Macedonian", "mk"
    MALAY = "Malay", "ms"
    MALAYALAM = "Malayalam", "ml"
    MARATHI = "Marathi", "mr"
    MONGOLIAN = "Mongolian", "mn"
    NEPALI = "Nepali", "ne"
    NORWEGIAN = "Norwegian", "no"
    ORIYA = "Oriya", "or"
    PASHTO = "Pashto", "ps"
    PERSIAN = "Persian", "fa"
    POLISH = "Polish", "pl"
    PORTUGUESE = "Portuguese", "pt"
    PUNJABI = "Punjabi", "pa"
    ROMANIAN = "Romanian", "ro"
    RUSSIAN = "Russian", "ru"
    SERBIAN = "Serbian", "sr"
    SINHALA = "Sinhala", "si"
    SLOVAK = "Slovak", "sk"
    SLOVENIAN = "Slovenian", "sl"
    SOMALI = "Somali", "so"
    SPANISH = "Spanish", "es"
    SUNDANESE = "Sundanese", "su"
    SWAHILI = "Swahili", "sw"
    SWEDISH = "Swedish", "sv"
    TAGALOG = "Tagalog", "tl"
    TAJIK = "Tajik", "tg"
    TAMIL = "Tamil", "ta"
    TATAR = "Tatar", "tt"
    TELUGU = "Telugu", "te"
    THAI = "Thai", "th"
    TIBETAN = "Tibetan", "bo"
    TURKISH = "Turkish", "tr"
    TURKMEN = "Turkmen", "tk"
    UKRAINIAN = "Ukrainian", "uk"
    URDU = "Urdu", "ur"
    UZBEK = "Uzbek", "uz"
    VIETNAMESE = "Vietnamese", "vi"
    WU_CHINESE = "Wu Chinese", "wuu"
    XHOSA = "Xhosa", "xh"
    YIDDISH = "Yiddish", "yi"
    YORUBA = "Yoruba", "yo"
    ZULU = "Zulu", "zu"


class Occupation(Enum):
    """Enumeration of Email Verification Statuses."""

    SOFTWARE_ENGINEER = "Software Engineer"
    HARDWARE_ENGINEER = "Hardware Engineer"
    ELECTRICAL_ENGINEER = "Electrical Engineer"
    MECHANICAL_ENGINEER = "Mechanical Engineer"
    CIVIL_ENGINEER = "Civil engineer"
    BIOMEDICAL_ENGINEER = "Biomedical Engineer"
    DOCTOR = "Doctor"
    NURSE = "Nurse"
    TEACHER = "Teacher"
    PROFESSOR = "Professor"
    ARTIST = "Artist"
    MUSICIAN = "Musician"
    WRITER = "Writer"
    ACCOUNTANT = "Accountant"
    LAWYER = "Lawyer"
    POLICE_OFFICER = "Police Officer"
    FIREFIGHTER = "Firefighter"
    CHEF = "Chef"
    ARCHITECT = "Architect"
    SCIENTIST = "Scientist"
    STUDENT = "Student"
    RETIREE = "Retiree"
    ENTREPRENEUR = "Entrepreneur"
    ATHLETE = "Athlete"
    JOURNALIST = "Journalist"
    DESIGNER = "Designer"
    PHARMACIST = "Pharmacist"
    SOCIAL_WORKER = "Social Worker"
    OTHER = "Other"


class Interest(Enum):
    """Enumeration of Profile Interests."""

    ANIMALS = "Animals"
    ART = "Art"
    BEACH = "Beach"
    BOARD_GAMES = "Board Games"
    BOOKS = "Books"
    COOKING = "Cooking"
    CRAFTS = "Crafts"
    CRYPTO = "Cryptocurrency"
    DANCING = "Dancing"
    DECENTRALIZATION = "Decentralization"
    DRAWING = "Drawing"
    ENTREPRENEURSHIP = "Entrepreneurship"
    EXERCISE = "Exercise"
    FASHION = "Fashion"
    FITNESS = "Fitness"
    FOOD = "Food"
    GAMING = "Gaming"
    GARDENING = "Gardening"
    HEALTH_WELLNESS = "Health & Wellness"
    HIKING = "Hiking"
    HOME_DECOR = "Home Decor"
    LANGUAGES = "Languages"
    MOVIES = "Movies"
    MUSIC = "Music"
    NATURE = "Nature"
    PAINTING = "Painting"
    PHOTOGRAPHY = "Photography"
    POETRY = "Poetry"
    READING = "Reading"
    RUNNING = "Running"
    SCIENCE = "Science"
    SELF_IMPROVEMENT = "Self-Improvement"
    SHOPPING = "Shopping"
    SPORTS = "Sports"
    TECHNOLOGY = "Technology"
    TRAVEL = "Travel"
    VOLUNTEERING = "Volunteering"
    WRITING = "Writing"
    ASTROLOGY = "Astrology"
    ASTRONOMY = "Astronomy"
    COFFEE = "Coffee"
    TEA = "Tea"
    HISTORY = "History"
    PHILOSOPHY = "Philosophy"
    CINEMA = "Cinema"
    THEATER = "Theater"
    MUSIC_PRODUCTION = "Music Production"
    DANCE = "Dance"
    FITNESS_CLASSES = "Fitness Classes"
    YOGA = "Yoga"
    MEDITATION = "Meditation"
    PODCASTS = "Podcasts"
    COMICS = "Comics"
    VIDEO_GAMES = "Video Games"
    CARD_GAMES = "Card Games"
    POLITICS = "Politics"
    ENVIRONMENT = "Environment"
    TRADING = "Trading"
    INVESTING = "Investing"
    FINANCE = "Finance"
    ARTIFICIAL_INTELLIGENCE = "Artificial Intelligence"
    MACHINE_LEARNING = "Machine Learning"
    DATA_SCIENCE = "Data Science"
    CYBERSECURITY = "Cybersecurity"
    WEB_DEVELOPMENT = "Web Development"
    MOBILE_DEVELOPMENT = "Mobile Development"
    BLOCKCHAIN = "Blockchain"
    DEFI = "DeFi"
    NFTS = "NFTs"
    DAPPS = "DApps"
    CRYPTO_TRADING = "Crypto Trading"
    MINING = "Mining"
    WEB3 = "Web3"
    CRYPTO_INVESTING = "Crypto Investing"
    BLOCKCHAIN_DEVELOPMENT = "Blockchain Development"
    GENEALOGY = "Genealogy"
    ANIME = "Anime"
    MANGA = "Manga"
    COSPLAY = "Cosplay"
    URBAN_EXPLORATION = "Urban Exploration"
    SURFING = "Surfing"
    SKATEBOARDING = "Skateboarding"
    SNOWBOARDING = "Snowboarding"
    SKIING = "Skiing"
    CAMPING = "Camping"
    BACKPACKING = "Backpacking"
    SURVIVALISM = "Survivalism"
    FORAGING = "Foraging"
    ARTISANAL_CRAFTS = "Artisanal Crafts"
    CALLIGRAPHY = "Calligraphy"
    GLASSBLOWING = "Glassblowing"
    POTTERY = "Pottery"
    KNITTING = "Knitting"
    CROCHETING = "Crocheting"
    EMBROIDERY = "Embroidery"
    SEWING = "Sewing"
    WOODWORKING = "Woodworking"
    METALWORKING = "Metalworking"
    LEATHERWORKING = "Leatherworking"
    BEEKEEPING = "Beekeeping"
    HOMEBREWING = "Homebrewing"
    WINE_MAKING = "Wine Making"
    SPIRITS_DISTILLING = "Spirits Distilling"
    MIXOLOGY = "Mixology"
    COCKTAILS = "Cocktails"
    BEER = "Beer"
    WINE = "Wine"
    WHISKY = "Whisky"
    RUM = "Rum"
    VODKA = "Vodka"
    GIN = "Gin"
    TEQUILA = "Tequila"
    BRANDY = "Brandy"
    CIDER = "Cider"
    MEAD = "Mead"
    SODA = "Soda"
    JUICE = "Juice"


class SocialMediaLink(Enum):
    """Enumeration of Social Media Links."""

    GITHUB = regex_compile(r"^https?:\/\/(www\.)?github\.com\/[a-zA-Z0-9_-]+$")
    FACEBOOK = regex_compile(r"^https?:\/\/(www\.)?facebook\.com\/[a-zA-Z0-9._-]+$")
    TWITTER = regex_compile(r"^https?:\/\/(www\.)?twitter\.com\/[a-zA-Z0-9_]+$")
    INSTAGRAM = regex_compile(r"^https?:\/\/(www\.)?instagram\.com\/[a-zA-Z0-9._]+$")
    LINKEDIN = regex_compile(r"^https?:\/\/(www\.)?linkedin\.com\/in\/[a-zA-Z0-9-]+$")
    PINTEREST = regex_compile(r"^https?:\/\/(www\.)?pinterest\.com\/[a-zA-Z0-9_]+$")
    TIKTOK = regex_compile(r"^https?:\/\/(www\.)?tiktok\.com\/@[a-zA-Z0-9_]+$")
    REDDIT = regex_compile(r"^https?:\/\/(www\.)?reddit\.com\/user\/[a-zA-Z0-9_]+$")
    DISCORD = regex_compile(r"^https?:\/\/(www\.)?discord\.com\/users\/[0-9]+$")
    TELEGRAM = regex_compile(
        r"^https?:\/\/(t(?:elegram)?\.me|telegram\.org)\/[a-zA-Z0-9_]+$"
    )
    YOUTUBE = regex_compile(
        r"^https?:\/\/(www\.)?youtube\.com\/(c|channel|user)\/[a-zA-Z0-9_-]+$"
    )
    SLACK = regex_compile(r"^https?:\/\/[a-zA-Z0-9-]+\.slack\.com\/?$")
    TWITCH = regex_compile(r"^https?:\/\/(www\.)?twitch\.tv\/[a-zA-Z0-9_]+$")
    SPOTIFY = regex_compile(r"^https?:\/\/open\.spotify\.com\/user\/[a-zA-Z0-9]+$")
    SOUNDCLOUD = regex_compile(r"^https?:\/\/(www\.)?soundcloud\.com\/[a-zA-Z0-9_-]+$")


class CardType(Enum):
    """Enumeration of Card Types."""

    CHEQUE = "cheque", "1991"
    SAVINGS = "savings", "1992"
    CREDIT = "credit", "1993"


class DataSharingPreference(Enum):
    """Enumeration of Data Sharing Options."""

    ACCOUNT = "Share All Permissible Account Data."
    PROFILE = "Share Profile Data."
    SETTINGS = "Share Settings Data."
    TRANSACTIONS = "Share Transaction Data."


class ProfileVisibility(Enum):
    """Enumeration of Profile Visibility Options."""

    PRIVATE = "Private"
    PUBLIC = "Public"
    ADMIN = "ADMIN"


class Theme(Enum):
    """Enumeration of Theme Options."""

    SYSTEM = "Defaults to Device Settings."
    DARK = "DARK Theme Preferred."
    LIGHT = "Light Theme Preferred."
    RED = "Red Theme Preferred."
    GREEN = "Green Theme Preferred."
    BLUE = "Blue Theme Preferred."


class Verification(Enum):
    """Enumeration of Verification Statuses."""

    UNVERIFIED = "New and Unverified"
    VERIFIED = "Verified"
    VERIFYING = "Verification Requested"
    FAILED = "Verification Failed"
    EXPIRED = "Verification Request Expired"


class UserDevicePermission(Enum):
    """Enumeration of Email Verification Statuses."""

    CAMERA = "camera"
    STORAGE = "STORAGE"
    CONTACTS = "contacts"


class AccountLoginMethod(Enum):
    """Enumeration of Email Verification Statuses."""

    EMAIL = "User Email and Password"
    GITHUB = "Github SSO"
    SLACK = "Slack SSO"
    GOOGLE = "Google SSO"
    FACEBOOK = "Facebook SSO"


class Communication(Enum):
    """Enumeration of Email Verification Statuses."""

    EMAIL = "Email Messenger"
    SMS = "SMS"
    CELL = "Mobile Phone"
    SLACK = "Slack Messenger"
