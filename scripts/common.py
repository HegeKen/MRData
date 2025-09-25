import json
from sys import platform
import urllib
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import requests
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, date, timezone
from requests.adapters import HTTPAdapter
from pymysql import Connection
import config
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

test = ['marble']
sdk = {
	'15': '35',
	'14': '34',
	'13': '33',
	'12': '31',
	'11': '30',
	'10': '29',
	'9': '28',
	'8.1': '27',
	'8': '26',
	'7.1': '25',
	'7': '24',
	'6': '23',
	'5.1': '22',
	'5': '21',
	'4.4': '19',
	'4.3': '18',
	'4.2': '17',
	'4.1': '16',
	'4': '14',
	'2.3': '9',
	'2': '9'
}

def android(ver):
	if ver == "15.0":
		return "V"
	elif ver == "14.0":
		return "U"
	elif ver == "13.0":
		return "T"
	elif ver == "12.0":
		return "S"
	elif ver == "11.0":
		return "R"
	elif ver == "10.0":
		return "Q"
	elif ver == "9.0":
		return "P"
	elif ver == "8.1":
		return "O"
	elif ver == "8.0":
		return "O"
	elif ver == "7.1":
		return "N"
	elif ver == "7.0":
		return "N"
	elif ver == "6.0":
		return "M"
	elif ver == "5.1":
		return "L"
	elif ver == "5.0":
		return "L"
	elif ver == "4.4":
		return "K"
	elif ver == "4.3":
		return "J"
	elif ver == "4.2":
		return "J"
	elif ver == "4.1":
		return "J"
	elif ver == "4.0":
		return "I"
	else:
		return "U"
	 

branches = [
	{
		"code": "",
		"tag": "CNXM",
		"region": "cn",
		"carrier": ["","chinatelecom","chinamobile","chinaunicom"],
		"zone": "1"
	},
	{
		"code": "_demo",
		"tag": "CNDM",
		"region": "cn",
		"carrier": ["","chinatelecom","chinamobile","chinaunicom"],
		"zone": "1"
	},
	{
		"code": "_tw_global",
		"tag": "TWXM",
		"region": "tw",
		"carrier": [],
		"zone": "2"
	},
	{
		"code": "_global",
		"tag": "MIXM",
		"region": "global",
		"carrier": [],
		"zone": "2"
	},
		{
		"code": "_dc_global",
		"tag": "MIDC",
		"region": "global",
		"carrier": ["dc"],
		"zone": "2"
	},
	{
		"code": "_eea_global",
		"tag": "EUXM",
		"region": "eea",
		"carrier": [],
		"zone": "2"
	},
	{
		"code": "_eea_hg_global",
		"tag": "EUHG",
		"region": "eea",
		"carrier": [
			"h3g"
		],
		"zone": "2"
	},
	{
		"code": "_eea_or_global",
		"tag": "EUOR",
		"region": "eea",
		"carrier": [
			"orange"
		],
		"zone": "2"
	},
	{
		"code": "_eea_tf_global",
		"tag": "EUTF",
		"region": "eea",
		"carrier": [
			"tf"
		],
		"zone": "2"
	},
	{
		"code": "_eea_by_global",
		"tag": "EUBY",
		"region": "eea",
		"carrier": [
			"by"
		],
		"zone": "2"
	},
	{
		"code": "_eea_vf_global",
		"tag": "EUVF",
		"region": "eea",
		"carrier": [
			"vodafone"
		],
		"zone": "2"
	},
	{
		"code": "_eea_sf_global",
		"tag": "EUSF",
		"region": "eea",
		"carrier": [
			"sfr"
		],
		"zone": "2"
	},
	{
		"code": "_eea_ti_global",
		"tag": "EUTI",
		"region": "eea",
		"carrier": [
			"tim"
		],
		"zone": "2"
	},
	{
		"code": "_ru_global",
		"tag": "RUXM",
		"region": "ru",
		"carrier": [],
		"zone": "2"
	},
	{
		"code": "_id_global",
		"tag": "IDXM",
		"region": "id",
		"carrier": [],
		"zone": "2"
	},
	{
		"code": "_tr_global",
		"tag": "TRXM",
		"region": "tr",
		"carrier": [],
		"zone": "2"
	},
	{
		"code": "_cl_en_global",
		"tag": "CLEN",
		"region": "cl",
		"carrier": [
			"en"
		],
		"zone": "2"
	},
	{
		"code": "_lm_cr_global",
		"tag": "LMCR",
		"region": "lm",
		"carrier": [
			"cr"
		],
		"zone": "2"
	},
	{
		"code": "_mx_at_global",
		"tag": "MXAT",
		"region": "mx",
		"carrier": [
			"at"
		],
		"zone": "2"
	},
	{
		"code": "_in_global",
		"tag": "INXM",
		"region": "in",
		"carrier": [],
		"zone": "2"
	},
	{
		"code": "in_in_global",
		"tag": "INXM",
		"region": "in",
		"carrier": [],
		"zone": "2"
	},
	{
		"code": "_mx_tc_global",
		"tag": "MXTC",
		"region": "mx",
		"carrier": [
			"telcel"
		],
		"zone": "2"
	},
	{
		"code": "_in_rf_global",
		"tag": "INRF",
		"region": "in",
		"carrier": [],
		"zone": "2"
	},
	{
		"code": "n_tw_global",
		"tag": "TWXM",
		"region": "tw",
		"carrier": [],
		"zone": "2"
	},
	{
		"code": "n_global",
		"tag": "MIXM",
		"region": "global",
		"carrier": [],
		"zone": "2"
	},
	{
		"code": "n_eea_global",
		"tag": "EUXM",
		"region": "eea",
		"carrier": [],
		"zone": "2"
	},
	{
		"code": "n_eea_hg_global",
		"tag": "EUHG",
		"region": "eea",
		"carrier": [],
		"zone": "2"
	},
	{
		"code": "n_eea_or_global",
		"tag": "EUOR",
		"region": "eea",
		"carrier": [],
		"zone": "2"
	},
	{
		"code": "n_eea_tf_global",
		"tag": "EUTF",
		"region": "eea",
		"carrier": [],
		"zone": "2"
	},
	{
		"code": "n_eea_vf_global",
		"tag": "EUVF",
		"region": "eea",
		"carrier": [],
		"zone": "2"
	},
	{
		"code": "n_eea_sf_global",
		"tag": "EUSF",
		"region": "eea",
		"carrier": [],
		"zone": "2"
	},
	{
		"code": "n_eea_ti_global",
		"tag": "EUTI",
		"region": "eea",
		"carrier": [],
		"zone": "2"
	},
	{
		"code": "n_ru_global",
		"tag": "RUXM",
		"region": "ru",
		"carrier": [],
		"zone": "2"
	},
	{
		"code": "n_id_global",
		"tag": "IDXM",
		"region": "id",
		"carrier": [],
		"zone": "2"
	},
	{
		"code": "n_tr_global",
		"tag": "TRXM",
		"region": "tr",
		"carrier": [],
		"zone": "2"
	},
	{
		"code": "n_th_as_global",
		"tag": "THAS",
		"region": "th",
		"carrier": [
			"as"
		],
		"zone": "2"
	},
	{
		"code": "n_cl_en_global",
		"tag": "CLEN",
		"region": "global",
		"carrier": [],
		"zone": "2"
	},
	{
		"code": "n_lm_cr_global",
		"tag": "LMCR",
		"region": "global",
		"carrier": [],
		"zone": "2"
	},
	{
		"code": "n_mx_at_global",
		"tag": "MXAT",
		"region": "global",
		"carrier": [],
		"zone": "2"
	},
	{
		"code": "g_tw_global",
		"tag": "TWXM",
		"region": "tw",
		"carrier": [],
		"zone": "2"
	},
	{
		"code": "g_eea_global",
		"tag": "EUXM",
		"region": "eea",
		"carrier": [],
		"zone": "2"
	},
	{
		"code": "g_eea_or_global",
		"tag": "EUOR",
		"region": "eea",
		"carrier": [],
		"zone": "2"
	},
	{
		"code": "g_eea_tf_global",
		"tag": "EUTF",
		"region": "eea",
		"carrier": [],
		"zone": "2"
	},
	{
		"code": "g_eea_vf_global",
		"tag": "EUVF",
		"region": "eea",
		"carrier": [],
		"zone": "2"
	},
	{
		"code": "g_eea_sf_global",
		"tag": "EUSF",
		"region": "eea",
		"carrier": [],
		"zone": "2"
	},
	{
		"code": "g_eea_ti_global",
		"tag": "EUTI",
		"region": "eea",
		"carrier": [],
		"zone": "2"
	},
	{
		"code": "g_ru_global",
		"tag": "RUXM",
		"region": "ru",
		"carrier": [],
		"zone": "2"
	},
	{
		"code": "g_tr_global",
		"tag": "TRXM",
		"region": "tr",
		"carrier": [],
		"zone": "2"
	},
	{
		"code": "g_lm_cr_global",
		"tag": "LMCR",
		"region": "global",
		"carrier": [],
		"zone": "2"
	},
	{
		"code": "_eea_hg_global",
		"tag": "EUHG",
		"region": "eea",
		"carrier": ["h3g"],
		"zone": "2"
	},
	{
		"code": "_jp_global",
		"tag": "JPXM",
		"region": "jp",
		"carrier": [],
		"zone": "2"
	},
	{
		"code": "_za_mt_global",
		"tag": "ZAMT",
		"region": "za",
		"carrier": [
			"mt"
		],
		"zone": "2"
	},
	{
		"code": "_lm_ms_global",
		"tag": "LMMS",
		"region": "lm",
		"carrier": [
			"movistar"
		],
		"zone": "2"
	},
	{
		"code": "_gt_tg_global",
		"tag": "GTTG",
		"region": "gt",
		"carrier": [
			"gt"
		],
		"zone": "2"
	},
	{
		"code": "_za_vc_global",
		"tag": "ZAVC",
		"region": "za",
		"carrier": [
			"vc"
		],
		"zone": "2"
	},
	{
		"code": "_jp_sb_global",
		"tag": "JPSB",
		"region": "jp",
		"carrier": [
			"sb"
		],
		"zone": "2"
	},
	{
		"code": "_jp_kd_global",
		"tag": "JPKD",
		"region": "global",
		"carrier": [],
		"zone": "2"
	},
	{
		"code": "_kr_gu_global",
		"tag": "KRGU",
		"region": "global",
		"carrier": [],
		"zone": "2"
	},
	{
		"code": "_kr_kt_global",
		"tag": "KRKT",
		"region": "global",
		"carrier": [],
		"zone": "2"
	},
	{
		"code": "_kr_sk_global",
		"tag": "KRSK",
		"region": "global",
		"carrier": [],
		"zone": "2"
	},
	{
		"code": "_h3g_global",
		"tag": "MIHG",
		"region": "global",
		"carrier": [],
		"zone": "2"
	},
	{
		"code": "_in_fk_global",
		"tag": "INFK",
		"region": "in",
		"carrier": [],
		"zone": "2"
	},
	{
		"code": "_kr_global",
		"tag": "KRXM",
		"region": "global",
		"carrier": [],
		"zone": "2"
	}
]

currentStable = ['klein', 'air', 'blue', 'water', 'sapphire', 'sapphiren', 'emerald', 'gold', 'garnet', 'zircon', 'gale', 'aristotle',
								 'umi', 'cmi', 'monet', 'vangogh', 'cas', 'thyme', 'venus', 'courbet', 'star', 'renoir', 'agate', 'vili', 'lisa',
								 'pissarroin', 'cupid', 'zeus', 'psyche', 'daumier', 'mayfly', 'unicorn', 'thor', 'taoyao', 'plato',
								 'fuxi', 'nuwa', 'ishtar', 'cetus', 'odin', 'zizhan', 'babylon', 'nabu', 'elish', 'enuma', 'dagu', 'pipa',
								 'liuqin', 'yudi', 'mona', 'zijin', 'ziyi', 'yuechu', 'lancelot', 'dandelion', 'angelica', 'angelican',
								 'cattail', 'dandelion_c3l2', 'fog', 'fire', 'earth', 'biloba', 'merlin', 'lime', 'cannon', 'gauguin', 'joyeuse',
								 'excalibur', 'curtana', 'mojito', 'curtana_in_rf', 'sweet', 'camellia', 'chopin', 'rosemary', 'lilac', 'selene',
								 'evergo', 'pissarro', 'spes', 'spesn', 'veux', 'fleur', 'viva', 'vida', 'light', 'lightcm', 'opal', 'xaga',
								 'sunstone', 'sky', 'ruby', 'redwood', 'marble', 'pearl', 'tapas', 'topaz', 'sweet_k6a', 'sea', 'cezanne',
								 'apollo', 'alioth', 'haydn', 'ares', 'munch', 'ingres', 'rubens', 'matisse', 'diting', 'mondrian', 'socrates',
								 'corot', 'rembrandt', 'yunluo', 'xun', 'ice', 'angelicain', 'frost', 'evergreen', 'rock',
								 'rosemary_p', 'surya', 'vayu', 'moonstone']
newDevices = ['air', 'gale', 'gust', 'freeguy', 'sapphiren', 'sapphire',
							'aristotle', 'garnet', 'zircon', 'gold']

onedevices = ["blue", "tissot", "jasmine",
							"laurel", "tiare", "ice", "water"]

cn_devices = ['babylon', 'cas', 'cetus', 'dagu', 'daumier', 'duchamp', 'elish', 'enuma', 'evergo', 'haydnin', 'lightcm',
							'liuqin', 'manet', 'matisse', 'mayfly', 'mona', 'odin', 'pearl', 'rembrandt', 'rubens', 'socrates', 'thor',
							'thyme', 'unicorn', 'yudi', 'yuechu', 'zijin', 'zizhan']
gb_devices = ['blue', 'agate', 'aristotle', 'biloba', 'courbet', 'curtana_in_rf', 'curtana', 'evergreen', 'fire', 'fleur', 'fog',
							'frost', 'ice', 'lilac', 'mojito', 'monet', 'moonstone', 'opal', 'pissarroin', 'plato', 'rock', 'rosemary_p',
							'rosemary', 'sapphire', 'sapphiren', 'sea', 'spes', 'spesn', 'sweet_k6a', 'sweet', 'taoyao', 'tapas', 'tiare',
							'topaz', 'vida', 'vili', 'viva', 'water',]
both_regions = ['alioth', 'ares', 'camellia', 'camellia', 'chopin', 'cmi', 'corot', 'cupid', 'dandelion_c3l2', 'dandelion',
							'diting', 'earth', 'fuxi', 'garnet', 'gauguin', 'gold', 'haydn', 'ingres', 'ishtar', 'light', 'lime',
							'lisa', 'marble', 'mondrian', 'munch', 'nabu', 'nuwa', 'pipa', 'pissarro', 'psyche', 'renoir', 'ruby',
							'selene', 'sky', 'star', 'sunstone', 'umi', 'venus', 'xaga', 'xun', 'yunluo', 'zeus', 'zircon', 'ziyi']

fullDevices = [
							 "agate", "air", "alioth", "andromeda", "angelica", "angelicain", "angelican", "apollo",
							 "aqua", "ares", "aries", "aristotle", "armani", "atom", "babylon", "begonia", "beryllium",
							 "biloba", "blue", "bomb", "cactus", "camellia", "camellian", "cancro_lte_ct", "cancro", "cannon",
							 "cappu", "capricorn", "cas", "cattail", "cepheus", "cereus", "cetus", "cezanne", "chiron", "chopin", "citrus", "clover",
							 "cmi", "corot", "courbet", "crux", "cupid", "curtana_in_rf", "curtana", "dagu", "daisy", "dandelion_c3l2", "dandelion", "daumier",
							 "davinci", "dior", "dipper", "diting", "earth", "elish", "emerald", "enuma", "equuleus", "evergo",
							 "evergreen", "excalibur", "ferrari", "fire", "fleur", "fog", "frost", "fuxi", "gale", "garnet", "gauguin",
							 "gemini", "ginkgo", "gold", "gram", "grus", "gucci", "haydn",
							 "helium", "hennessy", "hermes", "hydrogen", "ice", "ido_xhdpi",
							 "ingres", "ishtar", "jasmine", "jason", "joyeuse", "kate", "kenzo", "lancelot", "land", "latte",
							 "laurel_sprout", "laurus", "lavender", "lcsh92_wet_jb9", "lcsh92_wet_tdd", "lcsh92_wet_xm_td", "lcsh92",
							 "leo", "libra", "light", "lightcm", "lilac", "lime", "lisa", "lithium", "liuqin", "lmi", "lotus", "lte26007",
							 "marble", "markw", "matisse", "mayfly", "meri", "merlin", "mido", "mione_plus",
							 "mocha", "mojito", "mona", "mondrian", "monet", "moonstone", "munch", "nabu", "natrium",
							 "nikel", "nitrogen", "nuwa", "odin", "olive", "olivelite", "olivewood", "omega", "onc", "onclite", "opal", "oxygen", "pearl",
							 "perseus", "phoenix", "picasso_48m", "picasso", "pine", "pipa", "pisces", "pissarro", "pissarroin",
							 "platina", "plato", "polaris", "prada", "psyche", "pyxis", "raphael", "raphaels", "redwood",
							 "rembrandt", "renoir", "riva", "rock", "rolex", "rosemary_p", "rosemary", "rosy", "rubens", "ruby",
							 "sagit", "sakura", "santoni", "sapphire", "sapphiren", "scorpio", "sea", "selene", "shiva", "sirius",
							 "sky", "socrates", "spes", "spesn", "star", "sunstone", "surya", "sweet_k6a", "sweet", "taoyao", "tapas", "taurus", "thor",
							 "thyme", "tiare", "tiffany", "tissot", "toco", "topaz", "tucana", "tulip", "ugg", "ugglite", "umi", "unicorn", "ursa",
							 "vangogh", "vayu", "vela", "venus", "veux", "vida", "vili", "vince", "violet", "virgo_lte_ct", "virgo", "viva", "water",
							 "wayne", "whyred", "willow", "wt86047_pro", "wt86047", "wt88047_pro", "wt88047", "wt93007", "wt93807", "wt96007", "wt98007",
							 "xaga", "xun", "ysl", "yudi", "yuechu", "yunluo", "zeus", "zijin", "zircon", "ziyi", "zizhan"
]
CurrentIDS = ['1900587', '1900586', '1900585', '1900584', '1900583', '1900582', '1900581', '1900580', '1900579', '1900578', '1900577', '1900576',
							'1900575', '1900574', '1900573', '1900571', '1900570', '1900567', '1900566', '1900565', '1900564', '1900563', '1900562', '1900561',
							'1900560', '1900559', '1900558', '1900557', '1900556', '1900555', '1900554', '1900553', '1900552', '1900551', '1900549', '1900547',
							'1900546', '1900545', '1900544', '1900543', '1900539', '1900538', '1900536', '1900535', '1900534', '1900533', '1900532', '1900531',
							'1900530', '1900529', '1900454', '1900453', '1900458', '1900457', '1900456', '1900455', '1900452', '1900450', '1900449', '1900448',
							'1900447', '1900446', '1900445', '1900440', '1900439', '1900438', '1900436', '1900435', '1900431', '1900430', '1900429', '1900428',
							'1900427', '1900425', '1900423', '1900440', '1900439', '1900438', '1900436', '1900435', '1900431', '1900430', '1900429', '1900428',
							'1900427', '1900425', '1900423', '1900422', '1900420', '1900419', '1900418', '1900415', '1900413', '1900412', '1900411', '1900410',
							'1900409', '1900408', '1900407', '1900406', '1900405', '1900404', '1900403', '1900401', '1900400', '1900399', '1900398', '1900397',
							'1900396', '1900395', '1900394', '1900393', '1900392', '1900391', '1900390', '1900389', '1900387', '1900386', '1900385', '1900383',
							'1900382', '1900381', '1900380', '1900379', '1900378', '1900377', '1900376', '1900375', '1900374', '1900372', '1900369', '1700360']
Full = ['1900587', '1900586', '1900585', '1900584', '1900583', '1900582', '1900581', '1900580', '1900579', '1900578', '1900577', '1900576',
				'1900575', '1900574', '1900573', '1900571', '1900570', '1900567', '1900566', '1900565', '1900564', '1900563', '1900562', '1900561',
				'1900560', '1900559', '1900558', '1900557', '1900556', '1900555', '1900554', '1900553', '1900552', '1900551', '1900549', '1900547',
				'1900546', '1900545', '1900544', '1900543', '1900539', '1900538', '1900536', '1900535', '1900534', '1900533', '1900532', '1900531',
				'1900530', '1900529', '1900528', '1900527', '1900526', '1900525', '1900458', '1900457', '1900456', '1900455', '1900454', '1900453',
				'1900452', '1900450', '1900449', '1900448', '1900447', '1900446', '1900445', '1900440', '1900439', '1900438', '1900436', '1900435',
				'1900431', '1900430', '1900429', '1900428', '1900427', '1900425', '1900423', '1900422', '1900420', '1900419', '1900418', '1900415',
				'1900413', '1900412', '1900411', '1900410', '1900409', '1900408', '1900407', '1900406', '1900405', '1900404', '1900403', '1900401',
				'1900400', '1900399', '1900398', '1900397', '1900396', '1900395', '1900394', '1900393', '1900392', '1900391', '1900390', '1900389',
				'1900387', '1900386', '1900385', '1900383', '1900382', '1900381', '1900380', '1900379', '1900378', '1900377', '1900376', '1900375',
				'1900374', '1900373', '1900372', '1900371', '1900370', '1900369', '1900367', '1900366', '1900365', '1900362', '1900361', '1900360',
				'1900357', '1900356', '1900355', '1900354', '1900353', '1900351', '1900346', '1900343', '1900342', '1900341', '1900340', '1900338',
				'1900336', '1900334', '1900333', '1900332', '1900328', '1900326', '1900323', '1900321', '1900320', '1900319', '1900318', '1900317',
				'1900316', '1900315', '1900314', '1900309', '1900303', '1900302', '1900301', '1900299', '1900298', '1900297', '1900274', '1900261',
				'1900240', '1900101', '1900082', '1900037', '1900001', '1800367', '1800366', '1800365', '1800362', '1800361', '1800360', '1800357',
				'1800356', '1800355', '1800354', '1800353', '1800351', '1800346', '1800343', '1800342', '1800341', '1800340', '1800338', '1800336',
				'1800334', '1800333', '1800332', '1800328', '1800326', '1800323', '1800321', '1800320', '1800319', '1800318', '1800317', '1800316',
				'1800315', '1800314', '1800309', '1800303', '1800302', '1800301', '1800299', '1800298', '1800297', '1800274', '1800261', '1800240',
				'1800101', '1800082', '1800037', '1800001', '1700367', '1700366', '1700365', '1700362', '1700361', '1700360', '1700357', '1700356',
				'1700355', '1700354', '1700353', '1700351', '1700349', '1700346', '1700345', '1700343', '1700342', '1700341', '1700340', '1700338',
				'1700336', '1700334', '1700333', '1700332', '1700328', '1700326', '1700323', '1700321', '1700320', '1700319', '1700318', '1700317',
				'1700316', '1700315', '1700314', '1700309', '1700303', '1700302', '1700301', '1700299', '1700298', '1700297', '1700274', '1700261',
				'1700240', '1700101', '1700082', '1700037', '1700002', '1700001']
flags = {
	'Mioneplus': 'mione_plus', 'MioneplusCDMA': 'mione_plus', 'NativeMioneplus': 'mione_plus', 'plus-ota-QDR68': 'mione_plus', 'plus-ota-QDR66': 'mione_plus', 'plus-ota-QDR65.zip': 'mione_plus', 'plus-ota-QDQ61.zip': 'mione_plus', 'plus-ota-QDO53.zip': 'mione_plus',
	'MI2': 'aries', 'MI2Beta': 'aries', 'MI2HK': 'aries', 'MI2TW': 'aries', 'NativeMI2': 'aries', 'MI2Global': 'aries',
	'MI2A': 'taurus', 'MI2ABeta': 'taurus', 'NativeMI2A': 'taurus',
	'MI3TD': 'pisces',
	'pipa_ep_stdee': 'pipa',
	'HOUJI': 'houji',
	'HOUJIDEMO': 'houji',
	'ALIOTHDEMO': 'alioth',
	"FLAREIDGlobal":"flare",
	"flare_id_global":"flare",
	"DUCHAMPIDGlobal": "duchamp",
	"duchamp_id_global": "duchamp",
	"sapphiren_tr_global": "sapphiren",
	"SAPPHIRENTRGlobal": "sapphiren",
	"vermeer_ep_stdee": "vermeer",
	"VERMEEREPSTDEE": "vermeer",
	"blue_ru_global": "blue",
	"BLUERUGlobal": "blue",
	"SERENITYLMCRGlobal":"serenity",
	"serenity_lm_cr_global": "serenity",
	'AIRGlobal': 'air',
	'air_global': 'air',
	"goku_ep_stdee": "goku",
	"ruyi_ep_stdee": "ruyi",
	"GOKUEPSTDEE": "goku",
	"RUYIEPSTDEE": "ruyi",
	"blue_global": "blue",
	"blue_eea_global": "blue",
	"BLUEGlobal": "blue",
	"blue_in_global": "blue",
	"BLUEINGlobal": "blue",
	"blue_id_global": "blue",
	"BLUEIDGlobal": "blue",
	"amethyst_demo": "amethyst",
	"AMETHYSTDEMO": "amethyst",
	"amethyst": "amethyst",
	"AMETHYST": "amethyst",
	"dali_demo": "dali",
	"dali": "dali",
	"violin" : "violin",
	"SERENITYDCGlobal": "serenity",
	"serenity_dc_global": "serenity",
	"SERENITYEEASFGlobal": "serenity",
	"serenity_eea_sf_global": "serenity",
	"onyx_global": "onyx",
	"taiko_id_global": "taiko",
	"taiko_tr_global": "taiko",
	"taiko_demo":"taiko",
	"taiko":"taiko",
	"taiko_ru_global": "taiko",
	"koto_ru_global": "koto",
	"violin_demo" : "violin",
	"koto_in_global" : "koto",
	"turner_demo":"turner",
	"turner": "turner",
	"onyx_tw_global": "onyx",
	"onyx_ru_global": "onyx",
	"onyx_id_global": "onyx",
	"beryl_demo": "beryl",
	"onyx_eea_global": "onyx",
	"onyx_in_global": "onyx",
	"bixi": "bixi",
	"bixi_demo": "bixi",
	"koto_dc_global": "koto",
	"flare_ru_global": "flare",
	"spark_ru_global": "spark",
	"FLARERUGlobal": "flare",
	"SPARKRUGlobal": "spark",
	'THORDEMO':'thor',
	'XAGADEMO':'xaga',
	"SERENITYGlobal": "serenity",
	"serenity_global": "serenity",
	'DITINGDEMO':'diting',
	'LAURELSPROUTMXTCGlobal':'laurel_sprout',
	"cupid_cl_en_global" : "cupid",
	"CUPIDCLENGlobal" : "cupid",
	"garnet_dc_global" : "garnet",
	"GARNETDCGlobal" : "garnet",
	"moon_cl_en_global" : "moon",
	"MOONLMCRGlobal" : "moon",
	"sky_lm_cr_global" : "sky",
	"SKYLMCRGlobal" : "sky",
	"lake_dc_global" : "lake",
	"LAKEDCGlobal" : "lake",
	"lake_id_global": "lake",
	"LAKEIDGlobal": "lake",
	"rothko_eea_global": "rothko",
	"ROTHKOEEAGlobal": "rothko",
	"rothko_global": "rothko",
	"rothko_ru_global": "rothko",
	"rothko_id_global": "rothko",
	"ROTHKOGlobal": "rothko",
	"ROTHKORUGlobal": "rothko",
	"ROTHKOIDGlobal": "rothko",
	"degas_lm_cr_global":"degas",
	"DEGASLMCRGlobal":"degas",
	"degas_mx_at_global":"degas",
	"moon_lm_cr_global" : "moon",
	"tapas_lm_ms_global" : "tapas",
	"zorn_demo" : "zorn",
	"zorn" : "zorn",
	"ZORN" : "zorn",
	"miro" : "miro",
	"MIRO" : "miro",
	"rodin" : "rodin",
	"RODIN" : "rodin",
	"warm_in_global":"warm",
	"WARMINGlobal":"warm",
	"beryl_in_global":"beryl",
	"BERYLINGlobal":"beryl",
	"malachite_in_global":"malachite",
	"MALACHITEINGlobal":"malachite",
	"lake_tr_global" : "lake",
	"LAKETRGlobal" : "lake",
	"dada_ep_stdee" : "dada",
	"flame_ep_stdee" : "flame",
	"FLAMEEPSTDEE" : "flame",
	"miro_demo" : "miro",
	"DEGASMXATGlobal":"degas",
	"rothko_lm_cr_global":"rothko",
	"ROTHKOLMCRGlobal":"rothko",
	"lake_lm_cr_global":"lake",
	"LAKELMCRGlobal":"lake",
	"lake_gt_tg_global":"lake",
	"LAKEGTTGGlobal":"lake",
	"lake_mx_at_global":"lake",
	"LAKEMXATGlobal":"lake",
	"air_lm_cr_global":"air",
	"AIRLMCRGlobal":"air",
	"air_dc_global":"air",
	"AIRDCGlobal":"air",
	"amethyst_in_global" : "amethyst",
	"AMETHYSTINGlobal" : "amethyst",
	"AMETHYSTEEAGlobal":"amethyst",
	"amethyst_eea_global": "amethyst",
	"AMETHYSTTWGlobal":"amethyst",
	"amethyst_tw_global":"amethyst",
	"AMETHYSTIDGlobal":"amethyst",
	"amethyst_id_global":"amethyst",
	"amethyst_ru_global":"amethyst",
	"AMETHYSTRUGlobal":"amethyst",
	"AMETHYSTGlobal":"amethyst",
	"amethyst_global":"amethyst",
	"AMETHYSTDCGlobal":"amethyst",
	"amethyst_dc_global":"amethyst",
	"aristotle_lm_cr_global":"aristotle",
	"ARISTOTLELMCRGlobal":"aristotle",
	"aristotle_dc_global":"aristotle",
	"ARISTOTLEDCGlobal":"aristotle",
	"aristotle_cl_en_global":"aristotle",
	"ARISTOTLECLENGlobal":"aristotle",
	"aristotle_mx_at_global":"aristotle",
	"ARISTOTLEMXATGlobal":"aristotle",
	"emerald_lm_cr_global":"emerald",
	"EMERALDLMCRGlobal":"emerald",
	"emerald_dc_global":"emerald",
	"EMERALDDCGlobal":"emerald",
	"emerald_mx_at_global":"emerald",
	"EMERALDMXATGlobal":"emerald",
	"fire_lm_cr_global":"fire",
	"FIRELMCRGlobal":"fire",
	"fire_dc_global":"fire",
	"FIREDCGlobal":"fire",
	"fire_za_vc_global":"fire",
	"FIREZAVCGlobal":"fire",
	"fire_za_mt_global":"fire",
	"FIREZAMTGlobal":"fire",
	"fire_mx_at_global":"fire",
	"FIREMXATGlobal":"fire",
	"fire_gt_tg_global":"fire",
	"FIREGTTGGlobal":"fire",
	"gale_lm_cr_global":"gale",
	"GALELMCRGlobal":"gale",
	"gale_dc_global":"gale",
	"GALEDCGlobal":"gale",
	"gale_mx_at_global":"gale",
	"GALEMXATGlobal":"gale",
	"gale_gt_tg_global":"gale",
	"GALEGTTGGlobal":"gale",
	"garnet_lm_cr_global":"garnet",
	"GARNETLMCRGlobal":"garnet",
	"gold_lm_cr_global":"gold",
	"GOLDLMCRGlobal":"gold",
	"gold_dc_global":"gold",
	"GOLDDCGlobal":"gold",
	"gold_gt_tg_global":"gold",
	"GOLDGTTGGlobal":"gold",
	"light_cl_en_global":"light",
	"LIGHTCLENGlobal":"light",
	"moon_mx_at_global":"moon",
	"MOONMXATGlobal":"moon",
	"moon_dc_global":"moon",
	"MOONDCGlobal":"moon",
	"moon_gt_tg_global":"moon",
	"MOONGTTGGlobal":"moon",
	"sapphire_lm_cr_global":"sapphire",
	"SAPPHIRELMCRGlobal":"sapphire",
	"sapphire_dc_global":"sapphire",
	"SAPPHIREDCGlobal":"sapphire",
	"sapphire_mx_at_global":"sapphire",
	"SAPPHIREMXATGlobal":"sapphire",
	"sapphiren_dc_global":"sapphiren",
	"SAPPHIRENDCGlobal":"sapphiren",
	"sea_lm_ms_global":"sea",
	"SEALMMSGlobal":"sea",
	"sea_dc_global":"sea",
	"SEADCGlobal":"sea",
	"sea_gt_tg_global":"sea",
	"SEAGTTGGlobal":"sea",
	"sea_cl_en_global":"sea",
	"SEACLENGlobal":"sea",
	"sea_mx_at_global":"sea",
	"SEAMXATGlobal":"sea",
	"sea_lm_cr_global":"sea",
	"SEALMCRGlobal":"sea",
	"sky_cl_en_global":"sky",
	"SKYCLENGlobal":"sky",
	"sky_dc_global":"sky",
	"SKYDCGlobal":"sky",
	"taoyao_lm_cr_global":"taoyao",
	"TAOYAOLMCRGlobal":"taoyao",
	"TAPASLMMSGlobal":"tapas",
	"tapas_gt_tg_global":"tapas",
	"TAPASGTTGGlobal":"tapas",
	"tapas_cl_en_global":"tapas",
	"TAPASCLENGlobal":"tapas",
	"tapas_mx_at_global":"tapas",
	"TAPASMXATGlobal":"tapas",
	"tapas_lm_cr_global":"tapas",
	"TAPASLMCRGlobal":"tapas",
	"topaz_za_mt_global":"topaz",
	"TOPAZZAMTGlobal":"topaz",
	"topaz_za_vc_global":"topaz",
	"TOPAZZAVCGlobal":"topaz",
	"zircon_lm_cr_global":"zircon",
	"ZIRCONLMCRGlobal":"zircon",
	"zircon_dc_global":"zircon",
	"ZIRCONDCGlobal":"zircon",
	"degas_global": "degas",
	"degas_eea_global": "degas",
	"DEGASGlobal": "degas",
	"tanzanite_tw_global": "tanzanite",
	"TANZANITETWGlobal": "tanzanite",
	"TANZANITERUGlobal":"tanzanite",
	"tanzanite_ru_global":"tanzanite",
	"OBSIDIANLMCRGlobal":"obsidian",
	"obsidian_lm_cr_global":"obsidian",
	"DEGASEEAGlobal": "degas",
	"degas_tw_global": "degas",
	"DEGASTWGlobal": "degas",
	"degas_id_global": "degas",
	"DEGASIDGlobal": "degas",
	"degas_tr_global": "degas",
	"DEGASTRGlobal": "degas",
	"malachite": "malachite",
	"malachite_demo": "malachite",
	"degas_ru_global": "degas",
	"DEGASRUGlobal": "degas",
	"rothko_tw_global": "rothko",
	"ROTHKOTWGlobal": "rothko",
	"MALACHITE": "malachite",
	"MALACHITEDEMO": "malachite",
	"lake_tw_global": "lake",
	"lake_eea_global": "lake",
	"LAKEEEAGlobal": "lake",
	"malachite_ep_stdee":"malachite",
	"MALACHITEEPSTDEE":"malachite",
	"xun_ep_cmcc": "xun",
	"XUNEPCMCC": "xun",
	'BLUELMCRGlobal': 'blue',
	"ruyi_eea_global": "ruyi",
	"RUYIEEAGlobal": "ruyi",
	"rothko_tr_global": "rothko",
	"DEGASDCGlobal": "degas",
	"ROTHKODCGlobal": "rothko",
	"degas_dc_global": "degas",
	"rothko_dc_global": "rothko",
	"ROTHKOTRGlobal": "rothko",
	"LAKETWGlobal": "lake",
	"beryl": "beryl",
	"BERYL": "beryl",
	"SPARKINGlobal": "spark",
	"spark_in_global": "spark",
	'RUANEEAGlobal': 'ruan',
	"lake_global": "lake",
	"LAKEGlobal": "lake",
	'HM6EEASFGlobal': 'cereus',
	'ARESDEMO': 'ares',
	'MATISSEDEMO': 'matisse',
	'SOCRATESDEMO': 'socrates',
	"peridot_ep_stdee": "peridot",
	"PERIDOTEPSTDEE": "peridot",
	"PERIDOTTWGlobal": "peridot",
	"peridot_tw_global": "peridot",
	"klein_demo": "klein",
	"garnet_ep_cjcc": "garnet",
	"GARNETEPCJCC": "garnet",
	"klein": "klein",
	"klein_in_global": "klein",
	"KLEININGlobal": "klein",
	"klein_ru_global": "klein",
	"flare_eea_global": "flare",
	"flare_global": "flare",
	"SPARKGlobal": "spark",
	"SPARKEEAGlobal": "spark",
	"FLAREGlobal": "flare",
	"FLAREEEAGlobal": "flare",
	"spark_global": "spark",
	"spark_tw_global": "spark",
	"SPARKTWGlobal": "spark",
	"flare_tw_global": "flare",
	"FLARETWGlobal": "flare",
	"spark_eea_global": "spark",
	"KLEINRUGlobal": "klein",
	'ODINDEMO': 'odin',
	"RUANEEAGlobal": "ruan",
	"ruan_eea_global": "ruan",
	"ruan_ru_global": "ruan",
	"RUANRUGlobal": "ruan",
	"RUYITWGlobal": "ruyi",
	"ruyi_tw_global": "ruyi",
	"aurora_ep_stdee": "aurora",
	"AURORAEPSTDEE": "aurora",
	"breeze_ep_stdee": "breeze",
	"BREEZEEPSTDEE": "breeze",
	'BLUEEEAGlobal': 'blue',
	"degas_demo": "degas",
	"rothko_demo": "rothko",
	"pond_global": "pond",
	"flame": "flame",
	"FLAME": "flame",
	"flame_demo": "flame",
	"FLAMEDEMO": "flame",
	"ruan_ep_stdee": "ruan",
	"RUANEPSTDEE": "ruan",
	"PONDGlobal": "pond",
	"tides_demo": "tides",
	"ruyi_global": "ruyi",
	"RUYIGlobal": "ruyi",
	'ZIZHANDEMO': 'zizhan',
	'MONADEMO': 'mona',
	"dizi_eea_global": "dizi",
	"DIZIEEAGlobal": "dizi",
	"MOONTRGlobal": "moon",
	"moon_tr_global": "moon",
	"SHENGPREDPPGlobal": "sheng",
	"ruyi_demo": "ruyi",
	"goku_demo": "goku",
	"RUYIDEMO": "ruyi",
	"GOKUDEMO": "goku",
	"breeze_in_global": "breeze",
	"BREEZEINGlobal": "breeze",
	"ruan_global": "ruan",
	"RUANGlobal": "ruan",
	"ROTHKODEMO": "rothko",
	"TIDESDEMO": "tides",
	"DUCHAMPGlobal": "duchamp",
	"DUCHAMPEEAGlobal": "duchamp",
	"chenfeng": "chenfeng",
	"dizi": "dizi",
	"moon_id_global": "moon",
	"MOONIDGlobal": "moon",
	"zircon_jp_global": "zircon",
	"ZIRCONJPGlobal": "zircon",
	"moon_eea_global": "moon",
	"MOONEEAGlobal": "moon",
	"moon_ru_global": "moon",
	"MOONRUGlobal": "moon",
	"klein_global": "klein",
	"KLEINGlobal": "klein",
	"air_tw_global": "air",
	"AIRTWGlobal": "air",
	"breeze_demo": "breeze",
	"moon_tw_global": "moon",
	"MOONTWGlobal": "moon",
	"dizi_tr_global": "dizi",
	"DIZITRGlobal": "dizi",
	"babylon_ep_stdee": "babylon",
	"BABYLONEPSTDEE": "babylon",
	"gold_demo": "gold",
	"GOLDDEMO": "gold",
	"chenfeng_in_global": "chenfeng",
	"CHENFENGINGlobal": "chenfeng",
	"dizi_global": "dizi",
	"DIZIGlobal": "dizi",
	"dizi_ru_global": "dizi",
	"DIZIRUGlobal": "dizi",
	"dizi_id_global": "dizi",
	"DIZIIDGlobal": "dizi",
	"MOONGlobal": "moon",
	"moon_global": "moon",
	"goku": "goku",
	"COROTPREDPP": "corot",
	"COROTPREDPPGlobal": "corot",
	"HOUJIPREDPP": "houji",
	"SHENGPREDPP": "sheng",
	"dizi_tw_global": "dizi",
	"DIZITWGlobal": "dizi",
	"HOUJIPREDPPGlobal": "sheng",
	"SHENNONGPREDPP": "shennong",
	"vermeer_global": "vermeer",
	"peridot_id_global": "peridot",
	"PERIDOTIDGlobal": "peridot",
	"VERMEERGlobal": "vermeer",
	"air_eea_global": "air",
	"AIREEAGlobal": "air",
	'XUNINGlobal': 'xun',
	'xun_in_global': 'xun',
	"aurora_global": "aurora",
	"AURORAGlobal": "aurora",
	"peridot": "peridot",
	"ruan": "ruan",
	"vermeer_tw_global": "vermeer",
	"VERMEERTWGlobal": "vermeer",
	"SHENGIDGlobal": "sheng",
	"sheng_id_global": "sheng",
	"breeze": "breeze",
	"degas": "degas",
	"rothko": "rothko",
	"tides": "tides",
	"moon": "moon",
	"peridot_in_global": "peridot",
	"PERIDOTINGlobal": "peridot",
	"peridot_global": "peridot",
	"PERIDOTGlobal": "peridot",
	"peridot_eea_global": "peridot",
	"PERIDOTEEAGlobal": "peridot",
	"peridot_ru_global": "peridot",
	"PERIDOTRUGlobal": "peridot",
	"vermeer_eea_global": "vermeer",
	"VERMEEREEAGlobal": "vermeer",
	"SHENGGlobal": "sheng",
	"sheng_global": "sheng",
	"SHENGRUGlobal": "sheng",
	"sheng_ru_global": "sheng",
	"BREEZE": "breeze",
	"DEGAS": "degas",
	"ROTHKO": "rothko",
	"TIDES": "tides",
	"MOON": "moon",
	"dizi_demo": "dizi",
	"DIZIDEMO": "dizi",
	"ruan_demo": "ruan",
	"RUANDEMO": "ruan",
	"peridot_demo": "peridot",
	"PERIDOTDEMO": "peridot",
	"aurora_ru_global": "aurora",
	"AURORARUGlobal": "aurora",
	"dagu_ep_stdee": "dagu",
	"DAGUEPSTDEE": "dagu",
	"sheng_ep_stdee": "sheng",
	"SHENGEPSTDEE": "sheng",
	"AURORAINGlobal": "aurora",
	"aurora_in_global": "aurora",
	"aurora_tr_global": "aurora",
	"AURORATRGlobal": "aurora",
	"sheng_eea_global": "sheng",
	"SHENGEEAGlobal": "sheng",
	"manet_ep_stdee": "manet",
	"MANETEPSTDEE": "manet",
	"CHENFENG": "chenfeng",
	"DIZI": "dizi",
	"GOKU": "goku",
	"PERIDOT": "peridot",
	"aurora_eea_global": "aurora",
	"AURORAEEAGlobal": "aurora",
	"RUAN": "ruan",
	'OLIVELITELMCRGlobal': 'olivelite',
	'ONCLITELMCRGlobal': 'onclite',
	'PINEEEAORGlobal': 'pine',
	'PINEEEATFGlobal': 'pine',
	'PINEEEAVFGlobal': 'pine',
	'PINEEEASFGlobal': 'pine',
	'PYXISEEATFGlobal': 'pyxis',
	'PYXISEEAVFGlobal': 'pyxis',
	'PYXISEEASFGlobal': 'pyxis',
	'TUCANAEEAHGGlobal': 'tucana',
	'TUCANAEEAORGlobal': 'tucana',
	'TUCANAEEATFGlobal': 'tucana',
	'TUCANAEEAVFGlobal': 'tucana',
	'TUCANAEEATIGlobal': 'tucana',
	'WILLOWEEAHGGlobal': 'willow',
	'WILLOWEEAORGlobal': 'willow',
	'WILLOWEEATFGlobal': 'willow',
	'WILLOWEEAVFGlobal': 'willow',
	'WILLOWEEATIGlobal': 'willow',
	"duchamp_eea_global": "duchamp",
	"DUCHAMPRUGlobal": "duchamp",
	"duchamp_ru_global": "duchamp",
	"DUCHAMPINGlobal": "duchamp",
	"emerald_tr_global": "emerald",
	"EMERALDTRGlobal": "emerald",
	"garnet_ru_global": "garnet",
	"GARNETRUGlobal": "garnet",
	"blue_ru_global": "blue",
	"duchamp_ep_stdee": "duchamp",
	"DUCHAMPEPSTDEE": "duchamp",
	"houji_ru_global": "houji",
	"HOUJIRUGlobal": "houji",
	"BLUERUGlobal": "blue",
	"aurora_tw_global": "aurora",
	"AURORATWGlobal": "aurora",
	"blue_global": "blue",
	"BLUEGlobal": "blue",
	"blue_id_global": "blue",
	"BLUEIDGlobal": "blue",
	"AURORA": "aurora",
	"ruyi": "ruyi",
	"RUYI": "ruyi",
	"air_ep_stdee": "air",
	"AIREPSTDEE": "air",
	"sheng": "sheng",
	"SHENG": "sheng",
	"duchamp_in_global": "duchamp",
	"houji_ep_stdee": "houji",
	"HOUJIEPSTDEE": "houji",
	"shennong_ep_stdee": "shennong",
	"SHENNONGEPSTDEE": "shennong",
	'houji': 'houji',
	'emerald_eea_global': 'emerald',
	'EMERALDEEAGlobal': 'emerald',
	'emerald_ru_global': 'emerald',
	"houji_global": "houji",
	"HOUJIGlobal": "houji",
	"houji_in_global": "houji",
	"HOUJIINGlobal": "houji",
	"houji_id_global": "houji",
	"HOUJIIDGlobal": "houji",
	"houji_tw_global": "houji",
	"HOUJITWGlobal": "houji",
	"houji_tr_global": "houji",
	"HOUJITRGlobal": "houji",
	"sheng_demo": "sheng",
	"SHENGDEMO": "sheng",
	'sapphiren_eea_global': 'sapphiren',
	'SAPPHIRENEEAGlobal': 'sapphiren',
	'sapphiren_ru_global': 'sapphiren',
	'SAPPHIRENRUGlobal': 'sapphiren',
	'sapphiren_global': 'sapphiren',
	'SAPPHIRENGlobal': 'sapphiren',
	'sapphiren_tw_global': 'sapphiren',
	'SAPPHIRENTWGlobal': 'sapphiren',
	"aurora_demo": "aurora",
	"shennong_t": "shennong_t",
	"SHENNONGT": "shennong_t",
	"AURORADEMO": "aurora",
	"houji_eea_global": "houji",
	"HOUJIEEAGlobal": "houji",
	"corot_jp_global": "corot",
	"COROTJPGlobal": "corot",
	"yuechu_demo": "yuechu",
	"YUECHUDEMO": "yuechu",
	'sapphire_global': 'sapphire',
	'SAPPHIREGlobal': 'sapphire',
	'EMERALDRUGlobal': 'emerald',
	'zircon_tw_global': 'zircon',
	'ZIRCONTWGlobal': 'zircon',
	'VERMEER': 'vermeer',
	'duchamp_global': 'duchamp',
	'DUCHAMPTWGlobal': 'duchamp',
	'duchamp_tw_global': 'duchamp',
	'zircon_ep_stdee': 'zircon',
	'ZIRCONEPSTDEE': 'zircon',
	"blue_lm_cr_global": "blue",
	'VERMEERDEMO': 'vermeer',
	'vermeer_demo': 'vermeer',
	'water_eea_vf_global': 'water',
	'WATEREEAVFGlobal': 'water',
	'zircon_ru_global': 'zircon',
	'ZIRCONRUGlobal': 'zircon',
	'gale_eea_global': 'gale',
	'GALEEEAGlobal': 'gale',
	'gale_in_global': 'gale',
	'gale_tr_global': 'gale',
	'gold_tw_global': 'gold',
	'emerald_global': 'emerald',
	'EMERALDGlobal': 'emerald',
	'emerald_id_global': 'emerald',
	'EMERALDIDGlobal': 'emerald',
	'GOLDTWGlobal': 'gold',
	'GALETRGlobal': 'gale',
	'GALEINGlobal': 'gale',
	'xun_ep_stdee': 'xun',
	'XUNEPSTDEE': 'xun',
	'vermeer': 'vermeer',
	'DUCHAMP': 'duchamp',
	'DUCHAMPDEMO': 'duchamp',
	'garnet_tw_global': 'garnet',
	'GARNETTWGlobal': 'garnet',
	'duchamp_demo': 'duchamp',
	'sapphire_global': 'sapphire',
	'SAPPHIREGlobal': 'sapphire',
	'duchamp': 'duchamp',
	'gale_ru_global': 'gale',
	'GALERUGlobal': 'gale',
	'gold_global': 'gold',
	'gold_eea_global': 'gold',
	'gold_in_global': 'gold',
	'gold_id_global': 'gold',
	'gold_tr_global': 'gold',
	'GOLDGlobal': 'gold',
	'GOLDEEAGlobal': 'gold',
	'GOLDINGlobal': 'gold',
	'GOLDIDGlobal': 'gold',
	'GOLDTRGlobal': 'gold',
	"ruan_in_global": "ruan",
	"RUANINGlobal": "ruan",
	'garnet_global': 'garnet',
	'garnet_eea_global': 'garnet',
	'garnet_in_global': 'garnet',
	'garnet_id_global': 'garnet',
	'garnet_tr_global': 'garnet',
	'GARNETGlobal': 'garnet',
	'GARNETEEAGlobal': 'garnet',
	'GARNETINGlobal': 'garnet',
	'GARNETIDGlobal': 'garnet',
	'GARNETTRGlobal': 'garnet',
	'zircon_global': 'zircon',
	'zircon_eea_global': 'zircon',
	'zircon_in_global': 'zircon',
	'zircon_id_global': 'zircon',
	'zircon_tr_global': 'zircon',
	'ZIRCONGlobal': 'zircon',
	'ZIRCONEEAGlobal': 'zircon',
	'ZIRCONINGlobal': 'zircon',
	'ZIRCONIDGlobal': 'zircon',
	'ZIRCONTRGlobal': 'zircon',
	'GALEIDGlobal': 'gale',
	'gale_id_global': 'gale',
	'MANET': 'manet',
	'AIR': 'air',
	'air': 'air',
	'MANETDEMO': 'manet',
	'manet_demo': 'manet',
	'air_in_global': 'air',
	'AIRINGlobal': 'air',
	'fuxi_ep_sdlybjcg': 'fuxi',
	'FUXIEPSDLYBJCG': 'fuxi',
	'GALETWGlobal': 'gale',
	'gale_tw_global': 'gale',
	'manet': 'manet',
	'houji_demo': 'houji',
	'gale_global': 'gale',
	'GOLDEPSTDEE': 'gold',
	'gold_ep_stdee': 'gold',
	'pearl_ep_stdee': 'pearl',
	'PEARLEPSTDEE': 'pearl',
	'xaga_ep_stdee': 'xaga',
	'XAGAEPSTDEE': 'xaga',
	"corot_pre_dpp": "corot",
	"corot_pre_dpp_global": "corot",
	"houji_pre_dpp": "houji",
	"houji_pre_dpp_global": "houji",
	"sheng_pre_dpp": "sheng",
	"sheng_pre_dpp_global": "sheng",
	"shennong_pre_dpp": "shennong",
	"VERMEERRUGlobal": "vermeer",
	"vermeer_ru_global": "vermeer",
	'garnet_ep_stdee': 'garnet',
	'GARNETEPSTDEE': 'garnet',
	'GALEGlobal': 'gale',
	'shennong_demo': 'shennong',
	'SHENNONG': 'shennong',
	'SHENNONGDEMO': 'shennong',
	'shennong': 'shennong',
	'sapphire': 'sapphire',
	'SKYJPGlobal': 'sky',
	'sky_jp_global': 'sky',
	'SAPPHIRE': 'sapphire',
	'sapphiren': 'sapphiren',
	'SAPPHIREN': 'sapphiren',
	'PIPAEPSTDEE': 'pipa',
	'WATEREEASFGlobal': 'water',
	'WATERZAMTGlobal': 'water',
	'ANDROMEDAEEAVFGlobal': 'andromeda',
	'BEGONIALMCRGlobal': 'begonia',
	'OLIVEEEAHGGlobal': 'olive',
	'GRUSEEAORGlobal': 'grus',
	'CEPHEUSEEAORGlobal': 'cepheus',
	'CEPHEUSEEAVFGlobal': 'cepheus',
	'CEPHEUSEEAHGGlobal': 'cepheus',
	'XUN': 'xun',
	'aristotle_ru_global': 'aristotle',
	'ARISTOTLERUGlobal': 'aristotle',
	'MI3W': 'cancro',
	'AGATELMCRGlobal': 'agate',
	'ANGELICALMCRGlobal': 'angelica',
	'APOLLOEEAHGGlobal': 'apollo',
	'APOLLOEEAORGlobal': 'apollo',
	'APOLLOEEATFGlobal': 'apollo',
	'APOLLOEEAVFGlobal': 'apollo',
	'APOLLOEEASFGlobal': 'apollo',
	'APOLLOEEATIGlobal': 'apollo',
	'APOLLOMXTCGlobal': 'apollo',
	'APOLLOLMCRGlobal': 'apollo',
	'CAMELLIANEEATFGlobal': 'camellia',
	'CAMELLIANEEAHGGlobal': 'camellia',
	'CAMELLIANEEAORGlobal': 'camellia',
	'CAMELLIANEEAVFGlobal': 'camellia',
	'CAMELLIANEEASFGlobal': 'camellia',
	'CAMELLIANEEATIGlobal': 'camellia',
	'CANNONGEEAORGlobal': 'cannon',
	'CANNONGEEATFGlobal': 'cannon',
	'CANNONGEEAVFGlobal': 'cannon',
	'CANNONGEEASFGlobal': 'cannon',
	'CANNONGEEATIGlobal': 'cannon',
	'CANNONGLMCRGlobal': 'cannon',
	'DANDELIONC3L2EEABYGlobal': 'dandelion_c3l2',
	'DANDELIONC3L2EEASFGlobal': 'dandelion_c3l2',
	'EARTHEEAHGGlobal': 'earth',
	'EARTHEEAORGlobal': 'earth',
	'EARTHEEATFGlobal': 'earth',
	'EARTHEEABYGlobal': 'earth',
	'EARTHEEAVFGlobal': 'earth',
	'EARTHEEASFGlobal': 'earth',
	'EARTHEEATIGlobal': 'earth',
	'EARTHLMMSGlobal': 'earth',
	'EARTHMXATGlobal': 'earth',
	'EARTHGTTGGlobal': 'earth',
	"spring_eea_global": "spring",
	"spring_global": "spring",
	'EARTHZAMTGlobal': 'earth',
	'EARTHZAVCGlobal': 'earth',
	'FLEUREEAORGlobal': 'fleur',
	'FLEUREEABYGlobal': 'fleur',
	'FLEUREEASFGlobal': 'fleur',
	'FOGEEAHGGlobal': 'fog',
	'FOGEEAORGlobal': 'fog',
	'FOGEEATFGlobal': 'fog',
	'FOGEEAVFGlobal': 'fog',
	'FOGEEASFGlobal': 'fog',
	'FOGEEATIGlobal': 'fog',
	'GARNETDEMO': 'garnet',
	'GAUGUINEEAHGGlobal': 'gauguin',
	'GAUGUINEEAORGlobal': 'gauguin',
	'GAUGUINEEATFGlobal': 'gauguin',
	'GAUGUINEEAVFGlobal': 'gauguin',
	'GAUGUINEEASFGlobal': 'gauguin',
	'GAUGUINEEATIGlobal': 'gauguin',
	'HAYDNEEAHGGlobal': 'haydn',
	'HAYDNEEAORGlobal': 'haydn',
	'HAYDNEEATFGlobal': 'haydn',
	'HAYDNEEABYGlobal': 'haydn',
	'HAYDNEEAVFGlobal': 'haydn',
	'HAYDNEEASFGlobal': 'haydn',
	'HAYDNEEATIGlobal': 'haydn',
	'ICEMXTCGlobal': 'ice',
	'ICELMCRGlobal': 'ice',
	'ICEZAMTGlobal': 'ice',
	'ICEZAVCGlobal': 'ice',
	'ISHTAREPSTDEE': 'ishtar',
	'JOYEUSEEEAORGlobal': 'joyeuse',
	'JOYEUSEEEATFGlobal': 'joyeuse',
	'JOYEUSEEEAVFGlobal': 'joyeuse',
	'JOYEUSEEEASFGlobal': 'joyeuse',
	'JOYEUSELMCRGlobal': 'joyeuse',
	'LANCELOTEEASFGlobal': 'lancelot',
	'LIGHTEEAHGGlobal': 'light',
	'LIGHTEEAORGlobal': 'light',
	'LIGHTEEATFGlobal': 'light',
	'LIGHTEEABYGlobal': 'light',
	'LIGHTEEAVFGlobal': 'light',
	'LIGHTEEASFGlobal': 'light',
	'LIGHTEEATIGlobal': 'light',
	'LILACJPSBGlobal': 'lilac',
	'LIMEDEMO': 'lime',
	'LIMEYUNKE': 'lime',
	'LIMETL': 'lime',
	'LIMEEEAHGGlobal': 'lime',
	'LIMEEEAORGlobal': 'lime',
	'LIMEEEATFGlobal': 'lime',
	'LIMEEEAVFGlobal': 'lime',
	'LIMEEEASFGlobal': 'lime',
	'LIMEEEATIGlobal': 'lime',
	'LISALMCRGlobal': 'lisa',
	'LIUQINDEMO': 'liuqin',
	'LIUQINEPSTDEE': 'liuqin',
	'MARBLEEPSTDEE': 'marble',
	'MONDRIANDEMO': 'mondrian',
	'NUWADEMO': 'nuwa',
	'OPALEEAHGGlobal': 'opal',
	'OPALEEAORGlobal': 'opal',
	'OPALEEATFGlobal': 'opal',
	'OPALEEABYGlobal': 'opal',
	'OPALEEAVFGlobal': 'opal',
	'OPALEEASFGlobal': 'opal',
	'PIPADEMO': 'pipa',
	'PISSARRODEMO': 'pissarro',
	'ROSEMARYEEAORGlobal': 'rosemary',
	'ROSEMARYEEATFGlobal': 'rosemary',
	'ROSEMARYEEAVFGlobal': 'rosemary',
	'ROSEMARYEEASFGlobal': 'rosemary',
	'RUBYDEMO': 'ruby',
	'RUBYCLENGlobal': 'ruby',
	'RUBYLMCRGlobal': 'ruby',
	'RUBYMXATGlobal': 'ruby',
	'RUBYLMMSGlobal': 'ruby',
	'SELENEZAVCGlobal': 'selene',
	'SELENEZAMTGlobal': 'selene',
	'SKYEPSTDEE': 'sky',
	"rodin_id_global":"rodin",
	"xuanyuan":"xuanyuan",
	"muyu_id_global":"muyu",
	"muyu_ru_global":"muyu",
	"muyu_tr_global":"muyu",
	"muyu_tw_global":"muyu",
	"muyu_eea_global":"muyu",
	"muyu_global":"muyu",
	"uke_id_global":"uke",
	"uke_ru_global":"uke",
	"uke_tw_global":"uke",
	"uke_eea_global":"uke",
	"uke_global":"uke",
	"xuanyuan_tw_global":"xuanyuan",
	"xuanyuan_global":"xuanyuan",
	"xuanyuan_dc_global":"xuanyuan",
	"xuanyuan_eea_global":"xuanyuan",
	"xuanyuan_ru_global":"xuanyuan",
	"xuanyuan_id_global":"xuanyuan",
	"xuanyuan_tr_global":"xuanyuan",
	 "dada_tw_global":"dada",
	"dada_global":"dada",
	"dada_dc_global":"dada",
	"dada_eea_global":"dada",
	"dada_ru_global":"dada",
	"dada_in_global":"dada",
	"dada_id_global":"dada",
	"dada_lm_cr_global":"dada",
	"uke_tr_global":"uke",
	"MALACHITEMXATGlobal":"malachite",
	"malachite_lm_cr_global":"malachite",
	"malachite_mx_at_global":"malachite",
	"MALACHITELMCRGlobal":"malachite",
	"xuanyuan_demo":"xuanyuan",
	'SPESNEEAHGGlobal': 'spesn',
	'SPESNEEAORGlobal': 'spesn',
	'SPESNEEATFGlobal': 'spesn',
	'SPESNEEABYGlobal': 'spesn',
	'SPESNEEAVFGlobal': 'spesn',
	'SPESNEEASFGlobal': 'spesn',
	'SPESNEEATIGlobal': 'spesn',
	'SWEETEEAHGGlobal': 'sweet',
	'SWEETEEAORGlobal': 'sweet',
	'SWEETEEATFGlobal': 'sweet',
	'SWEETEEAVFGlobal': 'sweet',
	'SWEETEEASFGlobal': 'sweet',
	'SWEETEEATIGlobal': 'sweet',
	'VEUXEEAHGGlobal': 'veux',
	'VEUXEEAORGlobal': 'veux',
	'VEUXEEATFGlobal': 'veux',
	'VEUXEEABYGlobal': 'veux',
	'VEUXEEAVFGlobal': 'veux',
	'VEUXEEASFGlobal': 'veux',
	'VEUXEEATIGlobal': 'veux',
	'VILILMCRGlobal': 'vili',
	'WATEREEAHGGlobal': 'water',
	'WATEREEABYGlobal': 'water',
	'WATERCLENGlobal': 'water',
	'WATERMXTCGlobal': 'water',
	'WATERMXATGlobal': 'water',
	'WATERLMCRGlobal': 'water',
	'WATERZAVCGlobal': 'water',
	'YUNLUODEMO': 'yunluo',
	'ZIRCONDEMO': 'zircon',
	"DIZIINGlobal": "dizi",
	"dizi_in_global": "dizi",
	'Mione': 'mione_plus',
	'MI3': 'pisces',
	'UGG': 'ugg',
	'HM2WSG': 'wt98007',
	'umi': 'umi',
	'umi_pre': 'umi',
	'umi_global': 'umi',
	'umi_eea_global': 'umi',
	'umi_eea_hg_global': 'umi',
	'umi_eea_or_global': 'umi',
	'umi_eea_tf_global': 'umi',
	'umi_eea_vf_global': 'umi',
	'umi_eea_sf_global': 'umi',
	'umi_eea_ti_global': 'umi',
	'umi_ru_global': 'umi',
	'umi_in_global': 'umi',
	'umi_id_global': 'umi',
	'umi_tr_global': 'umi',
	'cmi': 'cmi',
	'cmi_pre': 'cmi',
	'cmi_global': 'cmi',
	'cmi_eea_global': 'cmi',
	'vangogh_pre': 'vangogh',
	'cas_pre': 'cas',
	'cas': 'cas',
	'thyme_pre': 'thyme',
	'star_pre': 'star',
	'renoir_pre': 'renoir',
	'lisa_pre': 'lisa',
	'psyche_pre': 'psyche',
	'plato_pre_dpp_global': 'plato',
	'fuxi_pre_gpp_global': 'fuxi',
	'fuxi_pre_dpp': 'fuxi',
	'fuxi_pre_dpp_global': 'fuxi',
	'nuwa_pre_gpp_global': 'nuwa',
	'nuwa_pre_dpp': 'nuwa',
	'nuwa_pre_dpp_global': 'nuwa',
	'cetus_pre': 'cetus',
	'odin_pre': 'odin',
	'nabu_pre': 'nabu',
	'elish_pre': 'elish',
	'enuma_pre': 'enuma',
	'pipa_pre_dpp': 'pipa',
	'mona_pre': 'mona',
	'lime_pre': 'lime',
	'cannon_pre': 'cannon',
	'gauguin_pre': 'gauguin',
	'camellia_pre': 'camellia',
	'chopin_pre': 'chopin',
	'chopin_id_global': 'chopin',
	'selenes': 'selene',
	'selene_ep_tly': 'selene',
	'evergo_pre': 'evergo',
	'pissarro_pre': 'pissarro',
	'xaga_demo': 'xaga',
	'sea_tw_global': 'sea',
	'sea_global': 'sea',
	'sea_eea_global': 'sea',
	'sea_ru_global': 'sea',
	'sea_tr_global': 'sea',
	'cezanne': 'cezanne',
	'cezanne_pre': 'cezanne',
	'alioth_pre': 'alioth',
	'haydn_pre': 'haydn',
	'ares_pre': 'ares',
	'ares_demo': 'ares',
	'ARISTOTLETWGlobal': 'aristotle',
	'ARISTOTLEGlobal': 'aristotle',
	'ARISTOTLEEEAGlobal': 'aristotle',
	'ARISTOTLEIDGlobal': 'aristotle',
	'ARISTOTLETRGlobal': 'aristotle',
	'COROTTWGlobal': 'corot',
	'XUNRUGlobal': 'xun',
	'XUNTRGlobal': 'xun',
	'COROTGlobal': 'corot',
	'COROTEEAGlobal': 'corot',
	'COROTRUGlobal': 'corot',
	'COROTTRGlobal': 'corot',
	'FUXIDEMO': 'fuxi',
	'REMBRANDTEPSTDEE': 'rembrandt',
	'FIREIDGlobal': 'fire',
	'MI3WMI4W': 'cancro', 'MI3WHK': 'cancro', 'MI3WTW': 'cancro', 'MI3WMY': 'cancro', 'MI3WSG': 'cancro', 'MI3WMI4WGlobal': 'cancro', 'MI3WGlobal': 'cancro',
	'MI4LTECT': 'cancro_lte_ct',
	'MI4i': 'ferrari', 'MI4iGlobal': 'ferrari', 'FERRARIGlobal': 'ferrari',
	'MI4c': 'libra', 'LIBRA': 'libra',
	'MI4s': 'aqua', 'AQUA': 'aqua',
	'MI5': 'gemini', 'MI5Global': 'gemini',
	'MI5S': 'capricorn', 'MI5SGlobal': 'capricorn',
	'MI5SPlus': 'natrium', 'NATRIUM': 'natrium', 'MI5SPlusGlobal': 'natrium',
	'MI5C': 'meri', 'MERI': 'meri',
	'MI5X': 'tiffany', 'TIFFANY': 'tiffany',
	"FLAMEINGlobal":"flame",
	"flame_in_global":"flame",
	"BERYLTWGlobal":"beryl",
	"beryl_tw_global":"beryl",
	"BERYLGlobal":"beryl",
	"beryl_global":"beryl",
	"BERYLDCGlobal":"beryl",
	"beryl_dc_global":"beryl",
	"BERYLEEAGlobal":"beryl",
	"beryl_eea_global":"beryl",
	"rodin_global":"rodin",
	"rodin_eea_global":"rodin",
	"RIDONGlobal":"rodin",
	"RIDONEEAGlobal":"rodin",
	'MI6': 'sagit', 'MI6Alpha': 'sagit', 'MI6Global': 'sagit',
	'MI6X': 'wayne',
	'MI8': 'dipper', 'DIPPER': 'dipper', 'MI8Global': 'dipper', 'MI8RUGlobal': 'dipper',
	'MI8UD': 'equuleus', 'EQUULEUS': 'equuleus', 'MI8UDGlobal': 'equuleus', 'MI8ProRUGlobal': 'equuleus',
	'MI8Explorer': 'ursa',
	'MI8Lite': 'platina', 'PLATINA': 'platina', 'MI8LiteGlobal': 'platina', 'PLATINARUGlobal': 'platina',
	'CEPHEUS': 'cepheus',
	'CEPHEUSGlobal': 'cepheus', 'CEPHEUSEEAGlobal': 'cepheus', 'CEPHEUSRUGlobal': 'cepheus', 'CEPHEUSLMCRGlobal': 'cepheus', 'CEPHEUSMXTCGlobal': 'cepheus',
	'CRUX': 'crux',
	'UMI': 'umi', 'UMIPRE': 'umi', 'UMIGlobal': 'umi', 'UMIEEAGlobal': 'umi', 'UMIRUGlobal': 'umi', 'UMIINGlobal': 'umi', 'UMIIDGlobal': 'umi', 'UMITRGlobal': 'umi',
	'CMI': 'cmi', 'CMIPRE': 'cmi', 'CMIGlobal': 'cmi', 'CMIEEAGlobal': 'cmi',
	'MONETTWGlobal': 'monet', 'MONETGlobal': 'monet', 'MONETEEAGlobal': 'monet', 'MONETJPKDGlobal': 'monet', 'MONETKRGUGlobal': 'monet', 'MONETKRKTGlobal': 'monet', 'MONETKRSKGlobal': 'monet',
	'VANGOGH': 'vangogh', 'VANGOGHPRE': 'vangogh',
	'CAS': 'cas', 'CASPRE': 'cas',
	'VENUS': 'venus', 'VENUSPRE': 'venus', 'VENUSTWGlobal': 'venus', 'VENUSGlobal': 'venus', 'VENUSEEAGlobal': 'venus', 'VENUSRUGlobal': 'venus', 'VENUSIDGlobal': 'venus', 'VENUSTRGlobal': 'venus', 'VENUSMXTCGlobal': 'venus',
	'HAYDN': 'haydn', 'HAYDNPRE': 'haydn', 'HAYDNGlobal': 'haydn', 'HAYDNEEAGlobal': 'haydn', 'HAYDNINGlobal': 'haydn',
	'THYME': 'thyme', 'THYMEPRE': 'thyme',
	'COURBETGlobal': 'courbet', 'COURBETEEAGlobal': 'courbet', 'COURBETRUGlobal': 'courbet', 'COURBETINGlobal': 'courbet', 'COURBETIDGlobal': 'courbet', 'COURBETTRGlobal': 'courbet', 'COURBETLMCRGlobal': 'courbet', 'COURBETMXTCGlobal': 'courbet',
	'STAR': 'star', 'STARPRE': 'star', 'STAREPXY': 'star', 'STARGlobal': 'star', 'STAREEAGlobal': 'star', 'STARINGlobal': 'star', 'STARIDGlobal': 'star',
	'RENOIR': 'renoir', 'RENOIRPRE': 'renoir', 'RENOIREPYY': 'renoir', 'RENOIRTWGlobal': 'renoir', 'RENOIRGlobal': 'renoir', 'RENOIREEAGlobal': 'renoir', 'RENOIRRUGlobal': 'renoir', 'RENOIRLMCRGlobal': 'renoir', 'RENOIRMXTCGlobal': 'renoir', 'RENOIRCLENGlobal': 'renoir', 'RENOIRJPGlobal': 'renoir',
	'AGATETWGlobal': 'agate', 'AGATEGlobal': 'agate', 'AGATEEEAGlobal': 'agate', 'AGATERUGlobal': 'agate', 'AGATEIDGlobal': 'agate', 'AGATETRGlobal': 'agate', 'AGATECLENGlobal': 'agate', 'AGATEMXATGlobal': 'agate',
	'VILITWGlobal': 'vili', 'VILIGlobal': 'vili', 'VILIEEAGlobal': 'vili', 'VILIRUGlobal': 'vili', 'VILIINGlobal': 'vili', 'VILIIDGlobal': 'vili', 'VILITRGlobal': 'vili', 'VILIJPGlobal': 'vili', 'VILICLENGlobal': 'vili', 'VILIMXATGlobal': 'vili',
	'LISA': 'lisa', 'LISAPRE': 'lisa', 'MONAPRE': 'mona', 'LISATWGlobal': 'lisa', 'LISAGlobal': 'lisa', 'LISAEEAGlobal': 'lisa', 'LISARUGlobal': 'lisa', 'LISAINGlobal': 'lisa', 'LISATRGlobal': 'lisa', 'LISACLENGlobal': 'lisa', 'LISAMXTCGlobal': 'lisa', 'LISAMXATGlobal': 'lisa',
	'PISSARROINGlobal': 'pissarro', 'PISSARROINFKGlobal': 'pissarroin',
	'CUPID': 'cupid', 'CUPIDEPXY': 'cupid', 'CUPIDTWGlobal': 'cupid', 'CUPIDGlobal': 'cupid', 'CUPIDEEAGlobal': 'cupid', 'CUPIDRUGlobal': 'cupid', 'CUPIDIDGlobal': 'cupid', 'CUPIDTRGlobal': 'cupid', 'CUPIDLMCRGlobal': 'cupid', 'CUPIDMXATGlobal': 'cupid',
	'ZEUS': 'zeus', 'ZEUSEPXY': 'zeus', 'ZEUSEPSTDEE': 'zeus', 'ZEUSTWGlobal': 'zeus', 'ZEUSGlobal': 'zeus', 'ZEUSEEAGlobal': 'zeus', 'ZEUSRUGlobal': 'zeus', 'ZEUSINGlobal': 'zeus', 'ZEUSIDGlobal': 'zeus', 'ZEUSTRGlobal': 'zeus',
	'PSYCHE': 'psyche', 'PSYCHEPRE': 'psyche', 'PSYCHETWGlobal': 'psyche', 'PSYCHEGlobal': 'psyche', 'PSYCHEEEAGlobal': 'psyche', 'PSYCHERUGlobal': 'psyche',
	'DAUMIER': 'daumier',
	'MAYFLY': 'mayfly', 'MAYFLYDEMO': 'mayfly',
	'UNICORN': 'unicorn',
	'THOR': 'thor',
	'XUNIDGlobal': 'xun',
	'TAOYAOTWGlobal': 'taoyao', 'TAOYAOGlobal': 'taoyao', 'TAOYAOEEAGlobal': 'taoyao', 'TAOYAORUGlobal': 'taoyao', 'TAOYAOIDGlobal': 'taoyao', 'TAOYAOTRGlobal': 'taoyao', 'TAOYAOLMCRGlobal': 'taoyao', 'TAOYAOCLENGlobal': 'taoyao',
	'PLATOTWGlobal': 'plato', 'PLATOGlobal': 'plato', 'PLATOEEAGlobal': 'plato', 'PLATORUGlobal': 'plato', 'PLATOIDGlobal': 'plato', 'PLATOTRGlobal': 'plato', 'PLATOCLENGlobal': 'plato', 'PLATOLMCRGlobal': 'plato',
	'FUXI': 'fuxi', 'FUXIEPSTDEE': 'fuxi', 'FUXITWGlobal': 'fuxi', 'FUXIGlobal': 'fuxi', 'FUXIEEAGlobal': 'fuxi', 'FUXIRUGlobal': 'fuxi', 'FUXITRGlobal': 'fuxi',
	'NUWA': 'nuwa', 'NUWAEPSTDEE': 'nuwa', 'NUWATWGlobal': 'nuwa', 'NUWAGlobal': 'nuwa', 'NUWAEEAGlobal': 'nuwa', 'NUWARUGlobal': 'nuwa', 'NUWATRGlobal': 'nuwa', 'NUWAINGlobal': 'nuwa',
	'MI8SE': 'sirius', 'SIRIUS': 'sirius',
	'GRUS': 'grus', 'GRUSGlobal': 'grus', 'GRUSEEAGlobal': 'grus', 'GRUSRUGlobal': 'grus',
	'PYXIS': 'pyxis', 'PYXISGlobal': 'pyxis', 'PYXISEEAGlobal': 'pyxis', 'PYXISRUGlobal': 'pyxis',
	'VELA': 'vela',
	'LAURUS': 'laurus',
	'TUCANA': 'tucana', 'TUCANAGlobal': 'tucana', 'TUCANAEEAGlobal': 'tucana', 'TUCANARUGlobal': 'tucana', 'TUCANAIDGlobal': 'tucana', 'TUCANAMXTCGlobal': 'tucana',
	'MINote': 'virgo', 'MINoteGlobal': 'virgo',
	'MINoteCT': 'virgo_lte_ct',
	'MINotePro': 'leo',
	'MINote2': 'scorpio', 'MINote2Global': 'scorpio',
	'MINote3': 'jason', 'JASON': 'jason', 'MINote3Global': 'jason',
	'TOCOGlobal': 'toco', 'TOCOEEAGlobal': 'toco', 'TOCORUGlobal': 'toco', 'TOCOTRGlobal': 'toco',
	'MIMAX': 'hydrogen',
	'MIMAXGlobal': 'hydrogen',
	'MIMAX652': 'helium', 'MIMAXPro': 'helium', 'MIMAX652Global': 'helium',
	'MIMAX2': 'oxygen', 'OXYGEN': 'oxygen', 'MIMAX2Global': 'oxygen',
	'MIMAX3': 'nitrogen', 'NITROGEN': 'nitrogen', 'MIMAX3Global': 'nitrogen', 'NITROGENRUGlobal': 'nitrogen',
	'MIMIX': 'lithium', 'MIMIXGlobal': 'lithium',
	'MIMIX2': 'chiron', 'CHIRON': 'chiron', 'MIMIX2Global': 'chiron',
	'MIMIX2S': 'polaris', 'POLARIS': 'polaris', 'MIMIX2SGlobal': 'polaris', 'MIMIX2SRUGlobal': 'polaris',
	'MIMIX3': 'perseus', 'MIMIX3Global': 'perseus', 'PERSEUSH3GGlobal': 'perseus', 'MIMIX3RUGlobal': 'perseus',
	'ANDROMEDA': 'andromeda', 'ANDROMEDAGlobal': 'andromeda', 'ANDROMEDAEEAGlobal': 'andromeda',
	'CETUS': 'cetus', 'CETUSPRE': 'cetus',
	'ODIN': 'odin', 'ODINPRE': 'odin',
	'ZIZHAN': 'zizhan',
	'MIPAD': 'mocha', 'MOCHA': 'mocha', 'MIPADGlobal': 'mocha', 'MOCHAGlobal': 'mocha',
	'MIPAD2': 'latte',
	'MIPAD3': 'cappu',
	'SKYGlobal': 'sky',
	'GARNET': 'garnet',
	'ZIRCON': 'zircon',
	'GOLD': 'gold',
	'MIPAD4': 'clover', 'CLOVER': 'clover',
	'NABU': 'nabu', 'NABUPRE': 'nabu', 'NABUDEMO': 'nabu', 'NABUEPLITEE': 'nabu', 'NABUTWGlobal': 'nabu', 'NABUGlobal': 'nabu', 'NABUEEAGlobal': 'nabu', 'NABURUGlobal': 'nabu', 'NABUINGlobal': 'nabu', 'NABUTRGlobal': 'nabu', 'NABUEPSTDEE': 'nabu',
	'ELISH': 'elish', 'ELISHPRE': 'elish', 'ELISHEPSTDEE': 'elish',
	'ENUMA': 'enuma', 'ENUMAPRE': 'enuma', 'ENUMAEPTBKJ': 'enuma', 'ENUMADEMO': 'enuma',
	'DAGU': 'dagu', 'DAGUDEMO': 'dagu',
	'MONA': 'mona',
	'ZIJIN': 'zijin',
	'ZIYI': 'ziyi', 'ZIYITWGlobal': 'ziyi', 'ZIYIGlobal': 'ziyi', 'ZIYIEEAGlobal': 'ziyi', 'ZIYIRUGlobal': 'ziyi', 'ZIYITRGlobal': 'ziyi',
	'TISSOT': 'tissot',
	'JASMINEGlobal': 'jasmine',
	'DAISYGlobal': 'daisy',
	'LAURELSPROUTGlobal': 'laurel', 'LAURELSPROUTEEAGlobal': 'laurel',
	'MIPLAY': 'lotus', 'LOTUS': 'lotus', 'MIPLAYGlobal': 'lotus', 'MIPLAYRUGlobal': 'lotus',
	'HMTD': 'wt93007', 'HM2': 'wt93007',
	'HMW': 'wt98007', 'HM2W': 'wt98007', 'HM2WHK': 'wt98007', 'HM2WTW': 'wt98007', 'HMWSGGlobal': 'wt98007', 'HMWSGP': 'wt98007', 'HM2WSGP': 'wt98007', 'HMWGlobal': 'wt98007', 'HM2WGlobal': 'wt98007',
	'HM1SWC': 'armani', 'H2A': 'armani', 'HM1SWCGlobal': 'armani', 'H2AGlobal': 'armani',
	'HM1STD': 'wt93807', 'H2S82TD': 'wt93807', 'HM1SLTE': 'wt96007', 'HM2014501': 'wt96007', 'WT96007': 'wt96007',
	'HM2XTD': 'wt86047', 'HM2014813': 'wt86047',
	'HM2XWC': 'wt88047', 'HM2014811': 'wt88047', 'HM2XWCGlobal': 'wt88047', 'HM2014811Global': 'wt88047',
	'HM2XTDPro': 'wt86047_pro', 'HM2XWCPro': 'wt88047_pro', 'HM2XWCProGlobal': 'wt88047_pro',
	'HM2A': 'lte26007', 'HM2XLCLTE': 'lte26007',
	'HM3': 'ido_xhdpi', 'HM3Global': 'ido_xhdpi',
	'HM3S': 'land', 'LAND': 'land', 'HM3SGlobal': 'land',
	'HM4': 'prada', 'PRADA': 'prada', 'HM4Global': 'prada',
	'HM4Pro': 'markw', 'MARKW': 'markw', 'HM4ProGlobal': 'markw',
	'HM4A': 'rolex', 'ROLEX': 'rolex', 'HM4AGlobal': 'rolex',
	'HM4X': 'santoni', 'HM4XGlobal': 'santoni',
	'HM5': 'rosy', 'ROSY': 'rosy', 'HM5Global': 'rosy', 'HM5RUGlobal': 'rosy',
	'HM5A': 'riva', 'RIVA': 'riva', 'HM5AGlobal': 'riva',
	'HM5Plus': 'vince', 'VINCE': 'vince', 'HM5PlusGlobal': 'vince', 'HM5PlusRUGlobal': 'vince',
	'HM6': 'cereus', 'CEREUS': 'cereus', 'HM6Global': 'cereus', 'HM6RUGlobal': 'cereus', 'CEREUSRUGlobal': 'cereus',
	'HM6A': 'cactus', 'CACTUS': 'cactus', 'HM6AGlobal': 'cactus', 'CACTUSGlobal': 'cactus', 'HM6ARUGlobal': 'cactus', 'CACTUSRUGlobal': 'cactus',
	'HM6Pro': 'sakura', 'SAKURA': 'sakura', 'HM6ProINGlobal': 'sakura', 'SAKURAINDIAGlobal': 'sakura',
	'ONCLITE': 'onclite', 'ONCLITEGlobal': 'onclite', 'ONCLITEEEAGlobal': 'onclite', 'ONCLITERUGlobal': 'onclite', 'ONCLITEINGlobal': 'onclite', 'ONCLITEMXTCGlobal': 'onclite',
	'PINE': 'pine', 'PINEGlobal': 'pine', 'PINEEEAGlobal': 'pine', 'PINERUGlobal': 'pine', 'PINEINGlobal': 'pine',
	'OLIVE': 'olive',
	'OLIVEGlobal': 'olive', 'OLIVEEEAGlobal': 'olive', 'OLIVERUGlobal': 'olive', 'OLIVEINGlobal': 'olive', 'OLIVEIDGlobal': 'olive',
	'OLIVELITE': 'olivelite', 'OLIVELITEGlobal': 'olivelite', 'OLIVELITEEEAGlobal': 'olivelite', 'OLIVELITERUGlobal': 'olivelite', 'OLIVELITEINGlobal': 'olivelite', 'OLIVELITEIDGlobal': 'olivelite', 'OLIVELITEMXTCGlobal': 'olivelite',
	'OLIVEWOODINGlobal': 'olivewood', 'OLIVEWOODIDGlobal': 'olivewood',
	'ATOM': 'atom', 'ATOMPRE': 'atom',
	'BOMB': 'bomb', 'BOMBPRE': 'bomb',
	'LANCELOT': 'lancelot', 'LANCELOTGlobal': 'lancelot', 'LANCELOTEEAGlobal': 'lancelot', 'LANCELOTRUGlobal': 'lancelot', 'LANCELOTINGlobal': 'lancelot', 'LANCELOTIDGlobal': 'lancelot', 'LANCELOTTRGlobal': 'lancelot', 'LANCELOTCLENGlobal': 'lancelot', 'LANCELOTMXTCGlobal': 'lancelot', 'LANCELOTMXATGlobal': 'lancelot', 'LANCELOTLMCRGlobal': 'lancelot',
	'DANDELION': 'dandelion', 'DANDELIONGlobal': 'dandelion', 'DANDELIONEEAGlobal': 'dandelion', 'DANDELIONRUGlobal': 'dandelion', 'DANDELIONINGlobal': 'dandelion', 'DANDELIONIDGlobal': 'dandelion', 'DANDELIONTRGlobal': 'dandelion', 'DANDELIONMXTCGlobal': 'dandelion', 'DANDELIONMXATGlobal': 'dandelion', 'DANDELIONLMCRGlobal': 'dandelion', 'DANDELIONZAMTGlobal': 'dandelion',
	'ANGELICAGlobal': 'angelica', 'ANGELICAEEAGlobal': 'angelica', 'ANGELICAININGlobal': 'angelica', 'ANGELICAIDGlobal': 'angelica', 'ANGELICATRGlobal': 'angelica', 'ANGELICAMXTCGlobal': 'angelica', 'ANGELICAMXATGlobal': 'angelica', 'ANGELICANGlobal': 'angelican', 'ANGELICANEEAGlobal': 'angelican', 'ANGELICANRUGlobal': 'angelican',
	'CATTAILINGlobal': 'cattail',
	'DANDELIONC3L2': 'dandelion_c3l2', 'DANDELIONC3L2TWGlobal': 'dandelion_c3l2', 'DANDELIONC3L2Global': 'dandelion_c3l2', 'DANDELIONC3L2EEAGlobal': 'dandelion_c3l2', 'DANDELIONC3L2RUGlobal': 'dandelion_c3l2', 'DANDELIONC3L2INGlobal': 'dandelion_c3l2', 'DANDELIONC3L2IDGlobal': 'dandelion_c3l2', 'DANDELIONC3L2CLENGlobal': 'dandelion_c3l2', 'DANDELIONC3L2MXATGlobal': 'dandelion_c3l2', 'DANDELIONC3L2LMCRGlobal': 'dandelion_c3l2', 'DANDELIONC3L2ZAMTGlobal': 'dandelion_c3l2',
	'FOGTWGlobal': 'fog', 'FOGGlobal': 'fog', 'FOGEEAGlobal': 'fog', 'FOGRUGlobal': 'fog', 'FOGINGlobal': 'fog', 'FOGIDGlobal': 'fog', 'FOGTRGlobal': 'fog', 'FOGCLENGlobal': 'fog', 'FOGMXATGlobal': 'fog', 'FOGLMCRGlobal': 'fog', 'FOGZAMTGlobal': 'fog',
	'HMNoteTD': 'lcsh92_wet_xm_td', 'H3TD': 'lcsh92_wet_xm_td',
	'HMNoteW': 'lcsh92_wet_jb9', 'H3W': 'lcsh92_wet_jb9', 'HMNoteWGlobal': 'lcsh92_wet_jb9', 'H3WGlobal': 'lcsh92_wet_jb9',
	'HMNoteLTE': 'dior', 'H3LTE': 'dior', 'HMNoteLTEGlobal': 'dior', 'H3LTEGlobal': 'dior',
	'HMNote1S': 'gucci', 'GUCCI': 'gucci', 'HMNote1SGlobal': 'gucci',
	'HMNote2': 'hermes', 'HERMES': 'hermes', 'HMNote2Global': 'hermes',
	'HMNote3': 'hennessy',
	'HMNote3Pro': 'kenzo', 'HMNote3CT': 'kenzo', 'HMNote3ProGlobal': 'kenzo', 'HMNote3CTGlobal': 'kenzo',
	'HMNote3ProtwGlobal': 'kate',
	'HMNote4': 'nikel', 'HMNote4Global': 'nikel',
	'HMNote4X': 'mido', 'HMNote4XGlobal': 'mido', 'MIDOGlobal': 'mido',
	'HMNote5ALITE': 'ugglite', 'UGGLITE': 'ugglite', 'HMNote5ALITEGlobal': 'ugglite',
	'HMNote5A': 'ugg', 'HMNote5AGlobal': 'ugg',
	'HMNote5': 'whyred', 'WHYRED': 'whyred', 'HMNote5Global': 'whyred', 'HMNote5HMNote5ProGlobal': 'whyred', 'WHYREDGlobal': 'whyred', 'HMNote5RUGlobal': 'whyred',
	'HMNote6ProGlobal': 'tulip', 'TULIPGlobal': 'tulip', 'HMNote6ProRUGlobal': 'tulip',
	'LAVENDER': 'lavender', 'LAVENDERGlobal': 'lavender', 'LAVENDEREEAGlobal': 'lavender', 'LAVENDERRUGlobal': 'lavender', 'LAVENDERINGlobal': 'lavender', 'LAVENDERMXTCGlobal': 'lavender',
	'VIOLET': 'violet', 'VIOLETINGlobal': 'violet',
	'GINKGO': 'ginkgo', 'GINKGOGlobal': 'ginkgo', 'GINKGOEEAGlobal': 'ginkgo', 'GINKGORUGlobal': 'ginkgo', 'GINKGOINGlobal': 'ginkgo', 'GINKGOIDGlobal': 'ginkgo', 'GINKGOMXTCGlobal': 'ginkgo',
	'BEGONIA': 'begonia', 'BEGONIAGlobal': 'begonia', 'BEGONIAEEAGlobal': 'begonia', 'BEGONIARUGlobal': 'begonia', 'BEGONIAININGlobal': 'begonia', 'BEGONIAIDGlobal': 'begonia', 'BEGONIAMXTCGlobal': 'begonia',
	'WILLOWGlobal': 'willow', 'WILLOWEEAGlobal': 'willow', 'WILLOWRUGlobal': 'willow', 'BILOBAGlobal': 'biloba', 'BILOBAEEAGlobal': 'biloba', 'BILOBARUGlobal': 'biloba',
	'MERLIN': 'merlin', 'MERLINTWGlobal': 'merlin', 'MERLINGlobal': 'merlin', 'MERLINEEAGlobal': 'merlin', 'MERLINRUGlobal': 'merlin', 'MERLININGlobal': 'merlin', 'MERLINIDGlobal': 'merlin', 'MERLINTRGlobal': 'merlin', 'MERLINCLENGlobal': 'merlin', 'MERLINMXTCGlobal': 'merlin', 'MERLINMXATGlobal': 'merlin', 'MERLINLMCRGlobal': 'merlin',
	'LIME': 'lime', 'LIMEPRE': 'lime', 'LIMETWGlobal': 'lime', 'LIMEGlobal': 'lime', 'LIMEEEAGlobal': 'lime', 'LIMERUGlobal': 'lime', 'LIMEINGlobal': 'lime', 'LIMEIDGlobal': 'lime', 'LIMETRGlobal': 'lime', 'LIMEMXTCGlobal': 'lime', 'LIMELMCRGlobal': 'lime',
	'CANNON': 'cannon', 'CANNONPRE': 'cannon', 'CANNONYUNKE': 'cannon', 'CANNONGTWGlobal': 'cannon', 'CANNONGGlobal': 'cannon', 'CANNONGEEAGlobal': 'cannon', 'CANNONGRUGlobal': 'cannon', 'CANNONGTRGlobal': 'cannon',
	'GAUGUIN': 'gauguin', 'GAUGUINPRE': 'gauguin', 'GAUGUINTWGlobal': 'gauguin', 'GAUGUINGlobal': 'gauguin', 'GAUGUINEEAGlobal': 'gauguin', 'GAUGUININGlobal': 'gauguin', 'GAUGUINTRGlobal': 'gauguin',
	'JOYEUSETWGlobal': 'joyeuse', 'JOYEUSEGlobal': 'joyeuse', 'JOYEUSEEEAGlobal': 'joyeuse', 'JOYEUSERUGlobal': 'joyeuse', 'JOYEUSEIDGlobal': 'joyeuse', 'JOYEUSETRGlobal': 'joyeuse', 'JOYEUSECLENGlobal': 'joyeuse',
	'EXCALIBURINGlobal': 'excalibur',
	'CURTANAGlobal': 'curtana', 'CURTANAEEAGlobal': 'curtana', 'CURTANARUGlobal': 'curtana', 'CURTANAINGlobal': 'curtana', 'CURTANATRGlobal': 'curtana', 'CURTANAMXATGlobal': 'curtana',
	'MOJITOGlobal': 'mojito', 'MOJITOEEAGlobal': 'mojito', 'MOJITORUGlobal': 'mojito', 'MOJITOINGlobal': 'mojito', 'MOJITOIDGlobal': 'mojito', 'MOJITOTRGlobal': 'mojito',
	'CURTANAINRFGlobal': 'curtana_in_rf',
	'SWEETTWGlobal': 'sweet', 'SWEETGlobal': 'sweet', 'SWEETEEAGlobal': 'sweet', 'SWEETRUGlobal': 'sweet', 'SWEETININGlobal': 'sweet', 'SWEETIDGlobal': 'sweet', 'SWEETTRGlobal': 'sweet', 'SWEETCLENGlobal': 'sweet', 'SWEETMXTCGlobal': 'sweet', 'SWEETMXATGlobal': 'sweet', 'SWEETLMCRGlobal': 'sweet', 'SWEETZAVCGlobal': 'sweet',
	'SWEETK6AGlobal': 'sweet_k6a', 'SWEETK6AEEAGlobal': 'sweet_k6a', 'SWEETK6ARUGlobal': 'sweet_k6a',
	'CAMELLIA': 'camellia', 'CAMELLIAPRE': 'camellia', 'CAMELLIAEPSTDEE': 'camellia', 'CAMELLIANTWGlobal': 'camellia', 'CAMELLIANGlobal': 'camellia', 'CAMELLIANEEAGlobal': 'camellia', 'CAMELLIANRUGlobal': 'camellia', 'CAMELLIAINGlobal': 'camellia', 'CAMELLIANIDGlobal': 'camellia', 'CAMELLIANTRGlobal': 'camellia', 'CAMELLIANTHASGlobal': 'camellia', 'CAMELLIANCLENGlobal': 'camellia', 'CAMELLIANLMCRGlobal': 'camellia', 'CAMELLIANMXATGlobal': 'camellia',
	'CHOPIN': 'chopin', 'CHOPINPRE': 'chopin', 'CHOPINDEMO': 'chopin', 'CHOPINEPKYWL': 'chopin', 'CHOPINGlobal': 'chopin', 'CHOPINIDGlobal': 'chopin', 'CHOPINTRGlobal': 'chopin',
	'LILACJPGlobal': 'lilac',
	'SELENE': 'selene', 'SELENES': 'selene', 'SELENEEPTLY': 'selene', 'SELENETWGlobal': 'selene', 'SELENEGlobal': 'selene', 'SELENEEEAGlobal': 'selene', 'SELENERUGlobal': 'selene', 'SELENEINGlobal': 'selene', 'SELENEIDGlobal': 'selene', 'SELENETRGlobal': 'selene', 'SELENEMXATGlobal': 'selene', 'SELENELMCRGlobal': 'selene',
	'EVERGO': 'evergo', 'EVERGOPRE': 'evergo', 'EVERGOEPCQRCB': 'evergo', 'EVERGOEPEC': 'evergo', 'EVERGOEPSTDEE': 'evergo', 'EVERGOEPSXHT': 'evergo', 'EVERGOEPYFAN': 'evergo', 'EVERGOEPYX': 'evergo', 'EVERGOINGlobal': 'evergo',
	'PISSARRO': 'pissarro', 'PISSARROPRE': 'pissarro', 'PISSARROTWGlobal': 'pissarro', 'PISSARROGlobal': 'pissarro', 'PISSARROEEAGlobal': 'pissarro', 'PISSARRORUGlobal': 'pissarro', 'PISSARROTRGlobal': 'pissarro',
	'SPESGlobal': 'spes', 'SPESINGlobal': 'spes', 'SPESTRGlobal': 'spes', 'SPESCLENGlobal': 'spes', 'SPESMXATGlobal': 'spes', 'SPESLMCRGlobal': 'spes', 'SPESLMMSGlobal': 'spes', 'SPESNGlobal': 'spesn', 'SPESNEEAGlobal': 'spesn', 'SPESNRUGlobal': 'spesn', 'SPESNIDGlobal': 'spesn', 'SPESNZAMTGlobal': 'spesn',
	'VEUX': 'veux', 'VEUXEPSTDEE': 'veux', 'VEUXTWGlobal': 'veux', 'VEUXGlobal': 'veux', 'VEUXEEAGlobal': 'veux', 'VEUXRUGlobal': 'veux', 'VEUXINGlobal': 'veux', 'VEUXIDGlobal': 'veux', 'VEUXTRGlobal': 'veux', 'VEUXJPGlobal': 'veux', 'VEUXCLENGlobal': 'veux', 'VEUXLMCRGlobal': 'veux', 'VEUXMXATGlobal': 'veux',
	'FLEURTWGlobal': 'fleur', 'FLEURGlobal': 'fleur', 'FLEUREEAGlobal': 'fleur', 'FLEURRUGlobal': 'fleur', 'FLEURINGlobal': 'fleur', 'FLEURIDGlobal': 'fleur', 'FLEURTRGlobal': 'fleur', 'FLEURCLENGlobal': 'fleur', 'FLEURLMCRGlobal': 'fleur', 'FLEURMXATGlobal': 'fleur', 'FLEURLMMSGlobal': 'fleur',
	'VIVATWGlobal': 'viva', 'VIVAGlobal': 'viva', 'VIVAEEAGlobal': 'viva', 'VIVARUGlobal': 'viva', 'VIVAIDGlobal': 'viva', 'VIVATRGlobal': 'viva', 'VIVALMCRGlobal': 'viva', 'VIVALMMSGlobal': 'viva', 'VIVAZAMTGlobal': 'viva', 'VIDAINGlobal': 'vida',
	'LIGHT': 'light', 'LIGHTEPSTDCE': 'light', 'LIGHTEPXY': 'light', 'LIGHTEPXDJA': 'light', 'LIGHTEPSTDEE': 'light', 'LIGHTTWGlobal': 'light', 'LIGHTGlobal': 'light', 'LIGHTEEAGlobal': 'light', 'LIGHTRUGlobal': 'light', 'LIGHTINGlobal': 'light', 'LIGHTIDGlobal': 'light', 'LIGHTTRGlobal': 'light', 'LIGHTTHASGlobal': 'light', 'LIGHTCLENGlobal': 'light', 'LIGHTLMCRGlobal': 'light',
	'LIGHTCM': 'lightcm', 'LIGHTCMEPSTDEE': 'lightcm',
	'OPALTWGlobal': 'opal', 'OPALGlobal': 'opal', 'OPALEEAGlobal': 'opal', 'OPALRUGlobal': 'opal', 'OPALCLENGlobal': 'opal', 'OPALMXATGlobal': 'opal', 'OPALLMCRGlobal': 'opal',
	'XAGA': 'xaga', 'XAGATWGlobal': 'xaga', 'XAGAGlobal': 'xaga', 'XAGAEEAGlobal': 'xaga', 'XAGARUGlobal': 'xaga', 'XAGAINGlobal': 'xaga', 'XAGATRGlobal': 'xaga',
	'SUNSTONE': 'sunstone', 'SUNSTONEEPSTDEE': 'sunstone', 'SUNSTONEINGlobal': 'sunstone', 'SUNSTONEGlobal': 'sunstone', 'SUNSTONEEEAGlobal': 'sunstone',
	'RUBY': 'ruby', 'RUBYEPSTDEE': 'ruby', 'RUBYINGlobal': 'ruby', 'RUBYGlobal': 'ruby', 'RUBYIDGlobal': 'ruby', 'RUBYTWGlobal': 'ruby', 'RUBYEEAGlobal': 'ruby',
	'REDWOOD': 'redwood', 'REDWOODTWGlobal': 'redwood', 'REDWOODGlobal': 'redwood', 'REDWOODEEAGlobal': 'redwood', 'REDWOODRUGlobal': 'redwood', 'REDWOODINGlobal': 'redwood', 'REDWOODTRGlobal': 'redwood',
	'DAVINCI': 'davinci', 'DAVINCIGlobal': 'davinci', 'DAVINCIEEAGlobal': 'davinci', 'DAVINCIRUGlobal': 'davinci', 'DAVINCIININGlobal': 'davinci',
	'RAPHAEL': 'raphael', 'RAPHAELGlobal': 'raphael', 'RAPHAELEEAGlobal': 'raphael', 'RAPHAELRUGlobal': 'raphael', 'RAPHAELININGlobal': 'raphael',
	'RAPHAELS': 'raphaels',
	'PHOENIX': 'phoenix', 'PHOENIXPRE': 'phoenix', 'PHOENIXININGlobal': 'phoenix',
	'PICASSO': 'picasso', 'PICASSOPRE': 'picasso',
	'PICASSO48M': 'picasso_48m', 'PICASSO48MPRE': 'picasso_48m',
	'LMI': 'lmi', 'LMIPRE': 'lmi', 'LMIGlobal': 'lmi', 'LMIEEAGlobal': 'lmi', 'LMIRUGlobal': 'lmi', 'LMIIDGlobal': 'lmi', 'LMITRGlobal': 'lmi',
	'CEZANNE': 'cezanne', 'CEZANNEPRE': 'cezanne',
	'APOLLO': 'apollo', 'APOLLOPRE': 'apollo', 'APOLLOTWGlobal': 'apollo', 'APOLLOGlobal': 'apollo', 'APOLLOEEAGlobal': 'apollo', 'APOLLORUGlobal': 'apollo', 'APOLLOINGlobal': 'apollo', 'APOLLOIDGlobal': 'apollo', 'APOLLOTRGlobal': 'apollo', 'APOLLOCLENGlobal': 'apollo',
	'ALIOTH': 'alioth', 'ALIOTHPRE': 'alioth', 'ALIOTHEPYUNKE': 'alioth', 'ALIOTHTWGlobal': 'alioth', 'ALIOTHGlobal': 'alioth', 'ALIOTHEEAGlobal': 'alioth', 'ALIOTHRUGlobal': 'alioth', 'ALIOTHINGlobal': 'alioth', 'ALIOTHIDGlobal': 'alioth', 'ALIOTHTRGlobal': 'alioth',
	'ARES': 'ares', 'ARESPRE': 'ares', 'ARESINGlobal': 'ares',
	'MUNCH': 'munch', 'MUNCHTWGlobal': 'munch', 'MUNCHGlobal': 'munch', 'MUNCHEEAGlobal': 'munch', 'MUNCHRUGlobal': 'munch', 'MUNCHINGlobal': 'munch', 'MUNCHIDGlobal': 'munch', 'MUNCHTRGlobal': 'munch',
	'INGRES': 'ingres', 'INGRESTWGlobal': 'ingres', 'INGRESGlobal': 'ingres', 'INGRESEEAGlobal': 'ingres', 'INGRESRUGlobal': 'ingres', 'INGRESIDGlobal': 'ingres', 'INGRESTRGlobal': 'ingres',
	'RUBENS': 'rubens', 'RUBENSEPSTDEE': 'rubens', 'RUBENSDEMO': 'rubens',
	'MATISSE': 'matisse', 'MATISSEEPSTDEE': 'matisse',
	'DITING': 'diting', 'DITINGTWGlobal': 'diting', 'DITINGGlobal': 'diting', 'DITINGEEAGlobal': 'diting', 'DITINGRUGlobal': 'diting', 'DITINGTRGlobal': 'diting', 'DITINGCLENGlobal': 'diting', 'DITINGLMCRGlobal': 'diting', 'DITINGMXATGlobal': 'diting', 'DITINGJPGlobal': 'diting', 'DITINGEPSTDEE': 'diting',
	'MONDRIAN': 'mondrian', 'MONDRIANEPSTDEE': 'mondrian',
	'SOCRATES': 'socrates',
	'REMBRANDT': 'rembrandt',
	'YUNLUO': 'yunluo', 'YUNLUOTWGlobal': 'yunluo', 'YUNLUOGlobal': 'yunluo', 'YUNLUOEEAGlobal': 'yunluo', 'YUNLUORUGlobal': 'yunluo', 'YUNLUOINGlobal': 'yunluo', 'YUNLUOIDGlobal': 'yunluo', 'YUNLUOTRGlobal': 'yunluo',
	'HMPro': 'omega', 'OMEGA': 'omega',
	'HMS2': 'ysl', 'YSL': 'ysl', 'HMS2Global': 'ysl', 'HMS2RUGlobal': 'ysl', 'HMS2CLMovistarGlobal': 'ysl',
	'TIAREGlobal': 'tiare', 'TIAREEEAGlobal': 'tiare', 'TIARERUGlobal': 'tiare', 'TIAREINGlobal': 'tiare',
	'ONCINGlobal': 'onc',
	'ICETWGlobal': 'ice', 'ICEGlobal': 'ice', 'ICEEEAGlobal': 'ice', 'ICERUGlobal': 'ice', 'ICEINGlobal': 'ice', 'ICEIDGlobal': 'ice',
	'ANGELICAININRFGlobal': 'angelicain',
	'FROSTTWGlobal': 'frost', 'FROSTGlobal': 'frost', 'FROSTEEAGlobal': 'frost', 'FROSTRUGlobal': 'frost', 'FROSTIDGlobal': 'frost',
	'POCOF1Global': 'beryllium', 'BERYLLIUMGlobal': 'beryllium', 'POCOF1RUGlobal': 'beryllium', 'BERYLLIUMRUGlobal': 'beryllium',
	'SHIVAINGlobal': 'shiva',
	'GRAMINGlobal': 'gram',
	'CITRUSTWGlobal': 'citrus', 'CITRUSGlobal': 'citrus', 'CITRUSEEAGlobal': 'citrus', 'CITRUSRUGlobal': 'citrus', 'CITRUSINGlobal': 'citrus', 'CITRUSIDGlobal': 'citrus', 'CITRUSTRGlobal': 'citrus',
	'ROCKTWGlobal': 'rock', 'ROCKGlobal': 'rock', 'ROCKEEAGlobal': 'rock', 'ROCKRUGlobal': 'rock', 'ROCKINGlobal': 'rock', 'ROCKIDGlobal': 'rock', 'ROCKTRGlobal': 'rock',
	'ROSEMARYPTWGlobal': 'rosemary_p', 'ROSEMARYPGlobal': 'rosemary_p', 'ROSEMARYPEEAGlobal': 'rosemary_p', 'ROSEMARYPRUGlobal': 'rosemary_p', 'ROSEMARYPIDGlobal': 'rosemary_p', 'ROSEMARYPTRGlobal': 'rosemary_p',
	'SURYAGlobal': 'surya', 'SURYAEEAGlobal': 'surya', 'SURYARUGlobal': 'surya', 'SURYAINGlobal': 'surya', 'SURYAIDGlobal': 'surya', 'SURYATRGlobal': 'surya',
	'VAYUTWGlobal': 'vayu', 'VAYUGlobal': 'vayu', 'VAYUEEAGlobal': 'vayu', 'VAYURUGlobal': 'vayu', 'VAYUINGlobal': 'vayu', 'VAYUIDGlobal': 'vayu', 'VAYUTRGlobal': 'vayu',
	'MOONSTONETWGlobal': 'moonstone', 'MOONSTONEGlobal': 'moonstone', 'MOONSTONEEEAGlobal': 'moonstone', 'MOONSTONERUGlobal': 'moonstone', 'MOONSTONEINGlobal': 'moonstone', 'MOONSTONEIDGlobal': 'moonstone',
	'EARTH': 'earth', 'EARTHINGlobal': 'earth', 'EARTHCLENGlobal': 'earth', 'EARTHGlobal': 'earth', 'EARTHIDGlobal': 'earth', 'EARTHLMCRGlobal': 'earth', 'EARTHTRGlobal': 'earth', 'EARTHEEAGlobal': 'earth', 'EARTHEPSTDEE': 'earth', 'EARTHTWGlobal': 'earth',
	'ROSEMARYGlobal': 'rosemary', 'ROSEMARYLMCRGlobal': 'rosemary', 'ROSEMARYCLENGlobal': 'rosemary', 'ROSEMARYIDGlobal': 'rosemary', 'ROSEMARYMXATGlobal': 'rosemary', 'ROSEMARYMXTCGlobal': 'rosemary', 'ROSEMARYRUGlobal': 'rosemary', 'ROSEMARYTRGlobal': 'rosemary', 'ROSEMARYTWGlobal': 'rosemary', 'ROSEMARYZAMTGlobal': 'rosemary', 'ROSEMARYZAVCGlobal': 'rosemary',
	'EVERGREENGlobal': 'evergreen', 'EVERGREENRUGlobal': 'evergreen', 'EVERGREENTRGlobal': 'evergreen', 'EVERGREENTWGlobal': 'evergreen',
	'TAPASGlobal': 'tapas', 'TAPASINGlobal': 'tapas', 'TAPASTRGlobal': 'tapas',
	'TOPAZEEAGlobal': 'topaz', 'TOPAZGlobal': 'topaz', 'TOPAZIDGlobal': 'topaz', 'TOPAZTRGlobal': 'topaz',
	'WATEREEAGlobal': 'water', 'WATERGlobal': 'water', 'WATERIDGlobal': 'water', 'WATERINGlobal': 'water', 'WATERTWGlobal': 'water',
	'ISHTAR': 'ishtar', 'ISHTARGlobal': 'ishtar', 'ISHTARRUGlobal': 'ishtar', 'ISHTARTWGlobal': 'ishtar',
	'PIPA': 'pipa', 'PIPAEEAGlobal': 'pipa', 'PIPAGlobal': 'pipa', 'PIPAIDGlobal': 'pipa', 'PIPAINGlobal': 'pipa', 'PIPARUGlobal': 'pipa', 'PIPATRGlobal': 'pipa', 'PIPATWGlobal': 'pipa',
	'LIUQIN': 'liuqin',
	'MARBLE': 'marble', 'MARBLEEEAGlobal': 'marble', 'MARBLEGlobal': 'marble', 'MARBLEINGlobal': 'marble', 'MARBLEIDGlobal': 'marble', 'MARBLERUGlobal': 'marble', 'MARBLETRGlobal': 'marble', 'MARBLETWGlobal': 'marble',
	'MONETEEAHGGlobal': 'monet', 'MONETEEAORGlobal': 'monet', 'MONETEEATFGlobal': 'monet', 'MONETEEAVFGlobal': 'monet', 'MONETEEASFGlobal': 'monet', 'MONETEEATIGlobal': 'monet',
	'RENOIREEAHGGlobal': 'renoir', 'RENOIREEAORGlobal': 'renoir', 'RENOIREEATFGlobal': 'renoir', 'RENOIREEAVFGlobal': 'renoir',
	'AGATEEEAHGGlobal': 'agate', 'AGATEEEAORGlobal': 'agate', 'AGATEEEATFGlobal': 'agate', 'AGATEEEABYGlobal': 'agate', 'AGATEEEAVFGlobal': 'agate', 'AGATEEEASFGlobal': 'agate', 'AGATEEEATIGlobal': 'agate',
	'LISAEEAHGGlobal': 'lisa', 'LISAEEAORGlobal': 'lisa', 'LISAEEATFGlobal': 'lisa', 'LISAEEABYGlobal': 'lisa', 'LISAEEAVFGlobal': 'lisa', 'LISAEEASFGlobal': 'lisa', 'LISAEEATIGlobal': 'lisa',
	'MERLINEEAHGGlobal': 'merlin',
	'MERLINEEAORGlobal': 'merlin',
	'MERLINEEATFGlobal': 'merlin',
	'MERLINEEAVFGlobal': 'merlin',
	'MERLINEEASFGlobal': 'merlin', 'MERLINEEATIGlobal': 'merlin',
	'LANCELOTEEAHGGlobal': 'lancelot',
	'LANCELOTEEAORGlobal': 'lancelot',
	'FIREINGlobal': 'fire',
	'FIRETRGlobal': 'fire',
	'SKYEEAGlobal': 'sky',
	"rodin_tr_global":"rodin",
	'LANCELOTEEATFGlobal': 'lancelot',
	'LANCELOTEEAVFGlobal': 'lancelot',
	'DANDELIONEEATFGlobal': 'dandelion',
	'DANDELIONEEAVFGlobal': 'dandelion',
	'DANDELIONEEASFGlobal': 'dandelion',
	'DANDELIONEEATIGlobal': 'dandelion',
	'ANGELICANEEAORGlobal': 'angelican',
	'EARTHRUGlobal': 'earth',
	'ROSEMARYEEAGlobal': 'rosemary',
	'ROSEMARYINGlobal': 'rosemary',
	'EVERGOEPYUNKE': 'evergo',
	'RUBYTRGlobal': 'ruby',
	'MARBLEDEMO': 'marble',
	'TOPAZRUGlobal': 'topaz',
	'EVERGREENEEAGlobal': 'evergreen',
	'RENOIREEASFGlobal': 'renoir',
	'RENOIREEATIGlobal': 'renoir',
	'SELENEEEAHGGlobal': 'selene',
	'SELENEEEAORGlobal': 'selene',
	'SELENEEEATFGlobal': 'selene',
	'SELENEEEABYGlobal': 'selene',
	'SELENEEEAVFGlobal': 'selene',
	'SELENEEEASFGlobal': 'selene',
	'UMIEEAHGGlobal': 'umi',
	'UMIEEAORGlobal': 'umi',
	'UMIEEATFGlobal': 'umi',
	'UMIEEAVFGlobal': 'umi',
	'UMIEEASFGlobal': 'umi',
	'UMIEEATIGlobal': 'umi',
	"onyx_demo":"onyx",
	"onyx":"onyx",
	"malachite_jp_global":"malachite",
	"SERENITYEEATFGlobal":"serenity",
	"serenity_eea_tf_global":"serenity",
	"SERENITYZAMTGlobal":"serenity",
	"serenity_za_mt_global":"serenity",
	"SERENITYRUGlobal":"serenity",
	"serenity_ru_global":"serenity",
	'VENUSEEAHGGlobal': 'venus',
	'VENUSEEAORGlobal': 'venus',
	'VENUSEEATFGlobal': 'venus',
	'VENUSEEAVFGlobal': 'venus',
	'VENUSEEASFGlobal': 'venus',
	'VENUSEEATIGlobal': 'venus',
	'STAREEAORGlobal': 'star',
	'STAREEAVFGlobal': 'star',
	'VILIEEAORGlobal': 'vili',
	'VILIEEATFGlobal': 'vili',
	'VILIEEAVFGlobal': 'vili',
	'VILIEEASFGlobal': 'vili',
	'TOCOEEAORGlobal': 'toco',
	'TOCOEEATFGlobal': 'toco',
	'TOCOEEAVFGlobal': 'toco',
	'SUNSTONETWGlobal': 'sunstone',
	'RUBYRUGlobal': 'ruby',
	'ISHTAREEAGlobal': 'ishtar',
	'SEAGlobal': 'sea',
	'SEAEEAGlobal': 'sea',
	'SEARUGlobal': 'sea',
	'SEATRGlobal': 'sea',
	'MONDRIANTWGlobal': 'mondrian',
	'MONDRIANEEAGlobal': 'mondrian',
	'MONDRIANRUGlobal': 'mondrian',
	'MONDRIANTRGlobal': 'mondrian',
	'SUNSTONEDEMO': 'sunstone', 'SUNSTONEEPTKGWDL': 'sunstone',
	'ISHTARDEMO': 'ishtar',
	'MONDRIANGlobal': 'mondrian',
	'YUECHU': 'yuechu',
	'CAMELLIAEPYUNKE': 'camellia',
	'PEARL': 'pearl',
	'MOONSTONETRGlobal': 'moonstone',
	'PSYCHEEPSTDEE': 'psyche',
	'UNICORNDEMO': 'unicorn',
	"AMETHYSTTRGlobal":"amethyst",
	"amethyst_tr_global":"amethyst",
	'ZIYIDEMO': 'ziyi',
	'REDWOODIDGlobal': 'redwood',
	'SWEETK6ATRGlobal': 'sweet_k6a',
	'SEATWGlobal': 'sea',
	'FIREGlobal': 'fire',
	'FIREEEAGlobal': 'fire',
	'FIRERUGlobal': 'fire',
	'RUBENSEPYX': 'rubens',
	'PISSARROEPYUNKE': 'pissarro',
	'CAMELLIAEPYX': 'camellia',
	'SOCRATESEPSTDEE': 'socrates',
	'NUWAEPSDLYBJCG': 'nuwa',
	'SKY': 'sky',
	'SKYINGlobal': 'sky',
	'ENUMAEPSTDEE': 'enuma',
	'RUBYKRGlobal': 'ruby',
	'SWEETK6AIDGlobal': 'sweet_k6a',
	'WATERRUGlobal': 'water',
	'FROSTTRGlobal': 'frost',
	'UNICORNEPSTDEE': 'unicorn',
	'COROTDEMO': 'corot',
	'COROT': 'corot',
	'YUDI': 'yudi',
	'YUDIDEMO': 'yudi',
	'YUNLUOEPSTDEE': 'yunluo',
	'BABYLON': 'babylon',
	'BABYLONDEMO': 'babylon',
	'XUNTWGlobal': 'xun',
	'XUNGlobal': 'xun',
	'XUNEEAGlobal': 'xun',
	'SKYTWGlobal': 'sky',
	'zircon': 'zircon',
	'zircon_demo': 'zircon',
	'gold': 'gold',
	'sapphiren': 'sapphiren',
	'sapphire': 'sapphire',
	'aurora': 'aurora',
	'manet': 'manet',
	'vermeer': 'vermeer',
	'aristotle_tw_global': 'aristotle',
	'aristotle_global': 'aristotle',
	'aristotle_eea_global': 'aristotle',
	'aristotle_id_global': 'aristotle',
	'aristotle_tr_global': 'aristotle',
	'corot': 'corot',
	'corot_demo': 'corot',
	'corot_tw_global': 'corot',
	'corot_global': 'corot',
	'corot_eea_global': 'corot',
	'corot_ru_global': 'corot',
	'corot_tr_global': 'corot',
	'river': 'river',
	'xun': 'xun',
	'xun_demo': 'xun',
	"XUNDEMO": "xun",
	'xun_tw_global': 'xun',
	'xun_global': 'xun',
	'xun_eea_global': 'xun',
	'xun_id_global': 'xun',
	'babylon': 'babylon',
	'babylon_demo': 'babylon',
	'fire_global': 'fire',
	'fire_eea_global': 'fire',
	'fire_ru_global': 'fire',
	'fire_in_global': 'fire',
	'fire_id_global': 'fire',
	'fire_tr_global': 'fire',
	'sky': 'sky',
	'sky_ep_stdee': 'sky',
	'sky_tw_global': 'sky',
	'sky_global': 'sky',
	'sky_eea_global': 'sky',
	'sky_in_global': 'sky',
	'heat': 'heat',
	'garnet': 'garnet',
	'garnet_demo': 'garnet',
	'houji': 'houji',
	'shennong': 'shennong',
	'pipa_pre_gpp': 'pipa',
	'pipa': 'pipa',
	'pipa_demo': 'pipa',
	'pipa_tw_global': 'pipa',
	'pipa_global': 'pipa',
	'pipa_eea_global': 'pipa',
	'pipa_ru_global': 'pipa',
	'pipa_in_global': 'pipa',
	'pipa_id_global': 'pipa',
	'pipa_tr_global': 'pipa',
	'yudi': 'yudi',
	'yudi_demo': 'yudi',
	'yuechu': 'yuechu',
	'pearl': 'pearl',
	'ishtar': 'ishtar',
	'ishtar_demo': 'ishtar',
	'ishtar_ep_stdee': 'ishtar',
	'ishtar_tw_global': 'ishtar',
	'ishtar_global': 'ishtar',
	'ishtar_eea_global': 'ishtar',
	'ishtar_ru_global': 'ishtar',
	'sweet_k6a_global': 'sweet_k6a',
	'sweet_k6a_eea_global': 'sweet_k6a',
	'sweet_k6a_ru_global': 'sweet_k6a',
	'sweet_k6a_id_global': 'sweet_k6a',
	'sweet_k6a_tr_global': 'sweet_k6a',
	'liuqin': 'liuqin',
	'liuqin_demo': 'liuqin',
	'liuqin_ep_stdee': 'liuqin',
	'marble': 'marble',
	'marble_demo': 'marble',
	'marble_ep_stdee': 'marble',
	'marble_tw_global': 'marble',
	'marble_global': 'marble',
	'marble_eea_global': 'marble',
	'marble_ru_global': 'marble',
	'marble_in_global': 'marble',
	'marble_id_global': 'marble',
	'marble_tr_global': 'marble',
	'water_tw_global': 'water',
	'water_global': 'water',
	'water_eea_global': 'water',
	'water_eea_sf_global': 'water',
	'water_eea_hg_global': 'water',
	'water_eea_by_global': 'water',
	'water_ru_global': 'water',
	'water_in_global': 'water',
	'water_id_global': 'water',
	'water_cl_en_global': 'water',
	'water_mx_tc_global': 'water',
	'water_mx_at_global': 'water',
	'water_lm_cr_global': 'water',
	'water_za_vc_global': 'water',
	'water_za_mt_global': 'water',
	'tapas_global': 'tapas',
	'tapas_in_global': 'tapas',
	'tapas_tr_global': 'tapas',
	'topaz_global': 'topaz',
	'topaz_eea_global': 'topaz',
	'topaz_ru_global': 'topaz',
	'topaz_id_global': 'topaz',
	'monet_tw_global': 'monet',
	'monet_global': 'monet',
	'monet_eea_global': 'monet',
	'monet_eea_hg_global': 'monet',
	'monet_eea_or_global': 'monet',
	'monet_eea_tf_global': 'monet',
	'monet_eea_vf_global': 'monet',
	'monet_eea_sf_global': 'monet',
	'monet_eea_ti_global': 'monet',
	'monet_jp_kd_global': 'monet',
	'monet_kr_gu_global': 'monet',
	'monet_kr_kt_global': 'monet',
	'monet_kr_sk_global': 'monet',
	'vangogh': 'vangogh',
	'thyme': 'thyme',
	'thyme_demo': 'thyme',
	'venus': 'venus',
	'venus_tw_global': 'venus',
	'venus_global': 'venus',
	'venus_eea_global': 'venus',
	'venus_eea_hg_global': 'venus',
	'venus_eea_or_global': 'venus',
	'venus_eea_tf_global': 'venus',
	'venus_eea_vf_global': 'venus',
	'venus_eea_sf_global': 'venus',
	'venus_eea_ti_global': 'venus',
	'venus_ru_global': 'venus',
	'venus_id_global': 'venus',
	'venus_tr_global': 'venus',
	'venus_mx_tc_global': 'venus',
	'courbet_global': 'courbet',
	'courbet_eea_global': 'courbet',
	'courbet_ru_global': 'courbet',
	'courbet_in_global': 'courbet',
	'courbet_id_global': 'courbet',
	'courbet_tr_global': 'courbet',
	'courbet_lm_cr_global': 'courbet',
	'courbet_mx_tc_global': 'courbet',
	'star': 'star',
	'star_ep_xy': 'star',
	'star_global': 'star',
	'star_eea_global': 'star',
	'star_eea_or_global': 'star',
	'star_eea_vf_global': 'star',
	'star_in_global': 'star',
	'star_id_global': 'star',
	'renoir': 'renoir',
	'renoir_demo': 'renoir',
	'renoir_ep_yy': 'renoir',
	'renoir_tw_global': 'renoir',
	'renoir_global': 'renoir',
	'renoir_eea_global': 'renoir',
	'renoir_eea_hg_global': 'renoir',
	'renoir_eea_or_global': 'renoir',
	'renoir_eea_tf_global': 'renoir',
	'renoir_eea_vf_global': 'renoir',
	'renoir_eea_sf_global': 'renoir',
	'renoir_eea_ti_global': 'renoir',
	'renoir_ru_global': 'renoir',
	'renoir_lm_cr_global': 'renoir',
	'renoir_mx_tc_global': 'renoir',
	'renoir_cl_en_global': 'renoir',
	'renoir_jp_global': 'renoir',
	'agate_tw_global': 'agate',
	'agate_global': 'agate',
	'agate_eea_global': 'agate',
	'agate_eea_hg_global': 'agate',
	'agate_eea_or_global': 'agate',
	'agate_eea_tf_global': 'agate',
	'agate_eea_by_global': 'agate',
	'agate_eea_vf_global': 'agate',
	'agate_eea_sf_global': 'agate',
	'agate_eea_ti_global': 'agate',
	'agate_ru_global': 'agate',
	'agate_id_global': 'agate',
	'agate_tr_global': 'agate',
	'agate_cl_en_global': 'agate',
	'agate_lm_cr_global': 'agate',
	'agate_mx_at_global': 'agate',
	'vili_tw_global': 'vili',
	'vili_global': 'vili',
	'vili_eea_global': 'vili',
	'vili_eea_or_global': 'vili',
	'vili_eea_tf_global': 'vili',
	'vili_eea_vf_global': 'vili',
	'vili_eea_sf_global': 'vili',
	'vili_ru_global': 'vili',
	'vili_in_global': 'vili',
	'vili_id_global': 'vili',
	'vili_tr_global': 'vili',
	'vili_jp_global': 'vili',
	'vili_cl_en_global': 'vili',
	'vili_mx_at_global': 'vili',
	'vili_lm_cr_global': 'vili',
	'lisa': 'lisa',
	'lisa_tw_global': 'lisa',
	'lisa_global': 'lisa',
	'lisa_eea_global': 'lisa',
	'lisa_eea_hg_global': 'lisa',
	'lisa_eea_or_global': 'lisa',
	'lisa_eea_tf_global': 'lisa',
	'lisa_eea_by_global': 'lisa',
	'lisa_eea_vf_global': 'lisa',
	'lisa_eea_sf_global': 'lisa',
	'lisa_eea_ti_global': 'lisa',
	'lisa_ru_global': 'lisa',
	'lisa_in_global': 'lisa',
	'lisa_tr_global': 'lisa',
	'lisa_cl_en_global': 'lisa',
	'lisa_mx_tc_global': 'lisa',
	'lisa_mx_at_global': 'lisa',
	'lisa_lm_cr_global': 'lisa',
	'pissarro_in_fk_global': 'pissarroin',
	'cupid': 'cupid',
	'cupid_ep_xy': 'cupid',
	'cupid_tw_global': 'cupid',
	'cupid_global': 'cupid',
	'cupid_eea_global': 'cupid',
	'cupid_ru_global': 'cupid',
	'cupid_id_global': 'cupid',
	'cupid_tr_global': 'cupid',
	'cupid_lm_cr_global': 'cupid',
	'cupid_mx_at_global': 'cupid',
	'zeus': 'zeus',
	'zeus_ep_xy': 'zeus',
	'zeus_ep_stdee': 'zeus',
	'zeus_tw_global': 'zeus',
	'zeus_global': 'zeus',
	'zeus_eea_global': 'zeus',
	'zeus_ru_global': 'zeus',
	'zeus_in_global': 'zeus',
	'zeus_id_global': 'zeus',
	'zeus_tr_global': 'zeus',
	"uke_demo": "uke",
	"muyu_demo": "muyu",
	"dada_demo": "dada",
	"haotian_demo": "haotian",
	'psyche': 'psyche',
	'psyche_ep_stdee': 'psyche',
	'psyche_tw_global': 'psyche',
	'psyche_global': 'psyche',
	'psyche_eea_global': 'psyche',
	'psyche_ru_global': 'psyche',
	'daumier': 'daumier',
	'mayfly': 'mayfly',
	'mayfly_demo': 'mayfly',
	'unicorn': 'unicorn',
	'unicorn_demo': 'unicorn',
	'unicorn_ep_stdee': 'unicorn',
	'thor': 'thor',
	'thor_demo': 'thor',
	'taoyao_tw_global': 'taoyao',
	'taoyao_global': 'taoyao',
	'taoyao_eea_global': 'taoyao',
	'taoyao_ru_global': 'taoyao',
	'taoyao_id_global': 'taoyao',
	'taoyao_tr_global': 'taoyao',
	'taoyao_lm_cr_global': 'taoyao',
	'taoyao_cl_en_global': 'taoyao',
	'plato_pre_gpp_global': 'plato',
	'plato_tw_global': 'plato',
	'plato_global': 'plato',
	'plato_eea_global': 'plato',
	'plato_ru_global': 'plato',
	'plato_id_global': 'plato',
	'plato_tr_global': 'plato',
	'plato_cl_en_global': 'plato',
	'plato_lm_cr_global': 'plato',
	'fuxi_pre_gpp': 'fuxi',
	'fuxi': 'fuxi',
	'fuxi_demo': 'fuxi',
	'fuxi_ep_stdee': 'fuxi',
	'fuxi_tw_global': 'fuxi',
	'fuxi_global': 'fuxi',
	'fuxi_eea_global': 'fuxi',
	'fuxi_ru_global': 'fuxi',
	'fuxi_tr_global': 'fuxi',
	'nuwa_pre_gpp': 'nuwa',
	'nuwa': 'nuwa',
	'nuwa_demo': 'nuwa',
	'nuwa_ep_stdee': 'nuwa',
	'nuwa_ep_sdlybjcg': 'nuwa',
	'nuwa_tw_global': 'nuwa',
	'nuwa_global': 'nuwa',
	'nuwa_eea_global': 'nuwa',
	'nuwa_ru_global': 'nuwa',
	'nuwa_in_global': 'nuwa',
	'nuwa_tr_global': 'nuwa',
	'toco_global': 'toco',
	'toco_eea_global': 'toco',
	'toco_eea_or_global': 'toco',
	'toco_eea_tf_global': 'toco',
	'toco_eea_vf_global': 'toco',
	'toco_ru_global': 'toco',
	'toco_tr_global': 'toco',
	'cetus': 'cetus',
	'odin': 'odin',
	'odin_demo': 'odin',
	'zizhan': 'zizhan',
	'zizhan_demo': 'zizhan',
	'nabu': 'nabu',
	'nabu_demo': 'nabu',
	'nabu_ep_stdee': 'nabu',
	'nabu_ep_litee': 'nabu',
	'nabu_tw_global': 'nabu',
	'nabu_global': 'nabu',
	'nabu_eea_global': 'nabu',
	'nabu_ru_global': 'nabu',
	'nabu_in_global': 'nabu',
	'nabu_tr_global': 'nabu',
	'elish': 'elish',
	'elish_ep_stdee': 'elish',
	'enuma': 'enuma',
	'enuma_demo': 'enuma',
	'enuma_ep_stdee': 'enuma',
	'enuma_ep_tbkj': 'enuma',
	'dagu': 'dagu',
	'dagu_demo': 'dagu',
	'mona': 'mona',
	'mona_demo': 'mona',
	'zijin': 'zijin',
	'ziyi': 'ziyi',
	'ziyi_demo': 'ziyi',
	'ziyi_tw_global': 'ziyi',
	'ziyi_global': 'ziyi',
	'ziyi_eea_global': 'ziyi',
	'ziyi_ru_global': 'ziyi',
	'ziyi_tr_global': 'ziyi',
	'merlin': 'merlin',
	'merlin_tw_global': 'merlin',
	'merlin_global': 'merlin',
	'merlin_eea_global': 'merlin',
	'merlin_eea_hg_global': 'merlin',
	'merlin_eea_or_global': 'merlin',
	'merlin_eea_tf_global': 'merlin',
	'merlin_eea_vf_global': 'merlin',
	'merlin_eea_sf_global': 'merlin',
	'merlin_eea_ti_global': 'merlin',
	'merlin_ru_global': 'merlin',
	'merlin_in_global': 'merlin',
	'merlin_id_global': 'merlin',
	'merlin_tr_global': 'merlin',
	'merlin_cl_en_global': 'merlin',
	'merlin_mx_tc_global': 'merlin',
	'merlin_mx_at_global': 'merlin',
	'merlin_lm_cr_global': 'merlin',
	"TANZANITEEEAGlobal":"tanzanite",
	"tanzanite_eea_global":"tanzanite",
	"TANZANITETRGlobal":"tanzanite",
	"tanzanite_tr_global":"tanzanite",
	'lancelot': 'lancelot',
	"MALACHITETRGlobal":"malachite",
	"malachite_tr_global":"malachite",
	"beryl_id_global":"beryl",
	"BERYLIDGlobal":"beryl",
	"BERYLTRGlobal":"beryl",
	"beryl_tr_global":"beryl",
	'lancelot_global': 'lancelot',
	'lancelot_eea_global': 'lancelot',
	'lancelot_eea_hg_global': 'lancelot',
	'lancelot_eea_or_global': 'lancelot',
	'lancelot_eea_tf_global': 'lancelot',
	'lancelot_eea_vf_global': 'lancelot',
	'lancelot_eea_sf_global': 'lancelot',
	'lancelot_ru_global': 'lancelot',
	'lancelot_in_global': 'lancelot',
	'lancelot_id_global': 'lancelot',
	'lancelot_tr_global': 'lancelot',
	'lancelot_cl_en_global': 'lancelot',
	'lancelot_mx_tc_global': 'lancelot',
	'lancelot_mx_at_global': 'lancelot',
	'lancelot_lm_cr_global': 'lancelot',
	'dandelion': 'dandelion',
	'dandelion_global': 'dandelion',
	'dandelion_eea_global': 'dandelion',
	'dandelion_eea_tf_global': 'dandelion',
	'dandelion_eea_vf_global': 'dandelion',
	'dandelion_eea_sf_global': 'dandelion',
	'dandelion_eea_ti_global': 'dandelion',
	'dandelion_ru_global': 'dandelion',
	'dandelion_in_global': 'dandelion',
	'dandelion_id_global': 'dandelion',
	'dandelion_tr_global': 'dandelion',
	'dandelion_mx_tc_global': 'dandelion',
	'dandelion_mx_at_global': 'dandelion',
	'dandelion_lm_cr_global': 'dandelion',
	'dandelion_za_mt_global': 'dandelion',
	'angelica_global': 'angelica',
	'angelica_eea_global': 'angelica',
	'angelicain_in_global': 'angelica',
	'angelica_id_global': 'angelica',
	'angelica_tr_global': 'angelica',
	'angelica_mx_tc_global': 'angelica',
	'angelica_mx_at_global': 'angelica',
	'angelica_lm_cr_global': 'angelica',
	'angelican_global': 'angelican',
	'angelican_eea_global': 'angelican',
	'angelican_eea_or_global': 'angelican',
	'angelican_ru_global': 'angelican',
	'cattail_in_global': 'cattail',
	'selene': 'selene',
	'selene_tw_global': 'selene',
	'selene_global': 'selene',
	'selene_eea_global': 'selene',
	'selene_eea_hg_global': 'selene',
	'selene_eea_or_global': 'selene',
	'selene_eea_tf_global': 'selene',
	'selene_eea_by_global': 'selene',
	'selene_eea_vf_global': 'selene',
	'selene_eea_sf_global': 'selene',
	'selene_ru_global': 'selene',
	'selene_in_global': 'selene',
	'selene_id_global': 'selene',
	'selene_tr_global': 'selene',
	'selene_mx_at_global': 'selene',
	'selene_lm_cr_global': 'selene',
	'selene_za_vc_global': 'selene',
	'selene_za_mt_global': 'selene',
	'dandelion_c3l2': 'dandelion_c3l2',
	'dandelion_c3l2_tw_global': 'dandelion_c3l2',
	'dandelion_c3l2_global': 'dandelion_c3l2',
	'dandelion_c3l2_eea_global': 'dandelion_c3l2',
	'dandelion_c3l2_eea_by_global': 'dandelion_c3l2',
	'dandelion_c3l2_eea_sf_global': 'dandelion_c3l2',
	'dandelion_c3l2_ru_global': 'dandelion_c3l2',
	'dandelion_c3l2_in_global': 'dandelion_c3l2',
	'dandelion_c3l2_id_global': 'dandelion_c3l2',
	'dandelion_c3l2_cl_en_global': 'dandelion_c3l2',
	'dandelion_c3l2_mx_at_global': 'dandelion_c3l2',
	'dandelion_c3l2_lm_cr_global': 'dandelion_c3l2',
	'dandelion_c3l2_za_mt_global': 'dandelion_c3l2',
	'fog_tw_global': 'fog',
	'fog_global': 'fog',
	'fog_eea_global': 'fog',
	'fog_eea_hg_global': 'fog',
	'fog_eea_or_global': 'fog',
	'fog_eea_tf_global': 'fog',
	'fog_eea_vf_global': 'fog',
	'fog_eea_sf_global': 'fog',
	'fog_eea_ti_global': 'fog',
	'fog_ru_global': 'fog',
	'fog_in_global': 'fog',
	'fog_id_global': 'fog',
	'fog_tr_global': 'fog',
	'fog_cl_en_global': 'fog',
	'fog_mx_at_global': 'fog',
	'fog_lm_cr_global': 'fog',
	'fog_za_mt_global': 'fog',
	'rock_tw_global': 'rock',
	'rock_global': 'rock',
	'rock_eea_global': 'rock',
	'rock_ru_global': 'rock',
	'rock_in_global': 'rock',
	'rock_id_global': 'rock',
	'rock_tr_global': 'rock',
	'earth': 'earth',
	'earth_ep_stdee': 'earth',
	'earth_tw_global': 'earth',
	'earth_global': 'earth',
	'earth_eea_global': 'earth',
	'earth_eea_hg_global': 'earth',
	'earth_eea_or_global': 'earth',
	'earth_eea_tf_global': 'earth',
	'earth_eea_by_global': 'earth',
	'earth_eea_vf_global': 'earth',
	'earth_eea_sf_global': 'earth',
	'earth_eea_ti_global': 'earth',
	'earth_ru_global': 'earth',
	'earth_in_global': 'earth',
	'earth_id_global': 'earth',
	'earth_tr_global': 'earth',
	'earth_cl_en_global': 'earth',
	'earth_lm_cr_global': 'earth',
	'earth_lm_ms_global': 'earth',
	'earth_mx_at_global': 'earth',
	'earth_gt_tg_global': 'earth',
	'earth_za_mt_global': 'earth',
	'earth_za_vc_global': 'earth',
	'biloba_global': 'biloba',
	'biloba_eea_global': 'biloba',
	'biloba_ru_global': 'biloba',
	'lime': 'lime',
	'lime_demo': 'lime',
	'lime_yunke': 'lime',
	'lime_tl': 'lime',
	'lime_tw_global': 'lime',
	'lime_global': 'lime',
	'lime_eea_global': 'lime',
	'lime_eea_hg_global': 'lime',
	'lime_eea_or_global': 'lime',
	'lime_eea_tf_global': 'lime',
	'lime_eea_vf_global': 'lime',
	'lime_eea_sf_global': 'lime',
	'lime_eea_ti_global': 'lime',
	'lime_ru_global': 'lime',
	'lime_in_global': 'lime',
	'lime_id_global': 'lime',
	'lime_tr_global': 'lime',
	'lime_mx_tc_global': 'lime',
	'lime_lm_cr_global': 'lime',
	'cannon': 'cannon',
	'cannon_yunke': 'cannon',
	'cannong_tw_global': 'cannon',
	'cannong_global': 'cannon',
	'cannong_eea_global': 'cannon',
	'cannong_eea_or_global': 'cannon',
	'cannong_eea_tf_global': 'cannon',
	'cannong_eea_vf_global': 'cannon',
	'cannong_eea_sf_global': 'cannon',
	'cannong_eea_ti_global': 'cannon',
	'cannong_ru_global': 'cannon',
	'cannong_tr_global': 'cannon',
	'cannong_lm_cr_global': 'cannon',
	'gauguin': 'gauguin',
	'gauguin_tw_global': 'gauguin',
	'gauguin_global': 'gauguin',
	'gauguin_eea_global': 'gauguin',
	'gauguin_eea_hg_global': 'gauguin',
	'gauguin_eea_or_global': 'gauguin',
	'gauguin_eea_tf_global': 'gauguin',
	'gauguin_eea_vf_global': 'gauguin',
	'gauguin_eea_sf_global': 'gauguin',
	'gauguin_eea_ti_global': 'gauguin',
	'gauguin_in_global': 'gauguin',
	'gauguin_tr_global': 'gauguin',
	'joyeuse_tw_global': 'joyeuse',
	'joyeuse_global': 'joyeuse',
	'joyeuse_eea_global': 'joyeuse',
	'joyeuse_eea_or_global': 'joyeuse',
	'joyeuse_eea_tf_global': 'joyeuse',
	'joyeuse_eea_vf_global': 'joyeuse',
	'joyeuse_eea_sf_global': 'joyeuse',
	'joyeuse_ru_global': 'joyeuse',
	'joyeuse_id_global': 'joyeuse',
	'joyeuse_tr_global': 'joyeuse',
	'joyeuse_cl_en_global': 'joyeuse',
	'joyeuse_lm_cr_global': 'joyeuse',
	'excalibur_in_global': 'excalibur',
	'curtana_global': 'curtana',
	'curtana_eea_global': 'curtana',
	'curtana_ru_global': 'curtana',
	'curtana_in_global': 'curtana',
	'curtana_tr_global': 'curtana',
	'curtana_mx_at_global': 'curtana',
	'mojito_global': 'mojito',
	'mojito_eea_global': 'mojito',
	'mojito_ru_global': 'mojito',
	'mojito_in_global': 'mojito',
	'mojito_id_global': 'mojito',
	'mojito_tr_global': 'mojito',
	'curtana_in_rf_global': 'curtana_in_rf',
	'sweet_tw_global': 'sweet',
	'sweet_global': 'sweet',
	'sweet_eea_global': 'sweet',
	'sweet_eea_hg_global': 'sweet',
	'sweet_eea_or_global': 'sweet',
	'sweet_eea_tf_global': 'sweet',
	'sweet_eea_vf_global': 'sweet',
	'sweet_eea_sf_global': 'sweet',
	'sweet_eea_ti_global': 'sweet',
	'sweet_ru_global': 'sweet',
	'sweetin_in_global': 'sweet',
	'sweet_id_global': 'sweet',
	'sweet_tr_global': 'sweet',
	'sweet_cl_en_global': 'sweet',
	'sweet_mx_tc_global': 'sweet',
	'sweet_mx_at_global': 'sweet',
	'sweet_lm_cr_global': 'sweet',
	'sweet_za_vc_global': 'sweet',
	'camellia': 'camellia',
	'camellia_ep_stdee': 'camellia',
	'camellia_ep_yunke': 'camellia',
	'camellia_ep_yx': 'camellia',
	'camellian_tw_global': 'camellia',
	'camellian_global': 'camellia',
	'camellian_eea_global': 'camellia',
	'camellian_eea_hg_global': 'camellia',
	'camellian_eea_or_global': 'camellia',
	'camellian_eea_tf_global': 'camellia',
	'camellian_eea_vf_global': 'camellia',
	'camellian_eea_sf_global': 'camellia',
	'camellian_eea_ti_global': 'camellia',
	'camellian_ru_global': 'camellia',
	'camellia_in_global': 'camellia',
	'camellian_id_global': 'camellia',
	'camellian_tr_global': 'camellia',
	'camellian_th_as_global': 'camellia',
	'camellian_cl_en_global': 'camellia',
	'camellian_lm_cr_global': 'camellia',
	'camellian_mx_at_global': 'camellia',
	'chopin': 'chopin',
	'chopin_demo': 'chopin',
	'chopin_ep_kywl': 'chopin',
	'chopin_global': 'chopin',
	'chopin_id_global_': 'chopin',
	'chopin_tr_global': 'chopin',
	'rosemary_tw_global': 'rosemary',
	'rosemary_global': 'rosemary',
	'rosemary_eea_global': 'rosemary',
	'rosemary_eea_or_global': 'rosemary',
	'rosemary_eea_tf_global': 'rosemary',
	'rosemary_eea_vf_global': 'rosemary',
	'rosemary_eea_sf_global': 'rosemary',
	'rosemary_ru_global': 'rosemary',
	'rosemary_in_global': 'rosemary',
	'rosemary_id_global': 'rosemary',
	'rosemary_tr_global': 'rosemary',
	'rosemary_cl_en_global': 'rosemary',
	'rosemary_mx_tc_global': 'rosemary',
	'rosemary_mx_at_global': 'rosemary',
	'rosemary_lm_cr_global': 'rosemary',
	'rosemary_za_vc_global': 'rosemary',
	'rosemary_za_mt_global': 'rosemary',
	'lilac_jp_global': 'lilac',
	'lilac_jp_sb_global': 'lilac',
	'evergo': 'evergo',
	'evergo_ep_yunke': 'evergo',
	'evergo_ep_cqrcb': 'evergo',
	'evergo_ep_ec': 'evergo',
	'evergo_ep_stdee': 'evergo',
	'evergo_ep_sxht': 'evergo',
	'evergo_ep_yfan': 'evergo',
	'evergo_ep_yx': 'evergo',
	'evergo_in_global': 'evergo',
	'pissarro': 'pissarro',
	'pissarro_demo': 'pissarro',
	'pissarro_ep_yunke': 'pissarro',
	'pissarro_tw_global': 'pissarro',
	'pissarro_global': 'pissarro',
	'pissarro_eea_global': 'pissarro',
	'pissarro_ru_global': 'pissarro',
	'pissarro_in_global': 'pissarro',
	'pissarro_tr_global': 'pissarro',
	'spes_global': 'spes',
	'spes_in_global': 'spes',
	'spes_tr_global': 'spes',
	'spes_cl_en_global': 'spes',
	'spes_mx_at_global': 'spes',
	'spes_lm_cr_global': 'spes',
	'spes_lm_ms_global': 'spes',
	'spesn_global': 'spesn',
	'spesn_eea_global': 'spesn',
	'spesn_eea_hg_global': 'spesn',
	'spesn_eea_or_global': 'spesn',
	'spesn_eea_tf_global': 'spesn',
	'spesn_eea_by_global': 'spesn',
	'spesn_eea_vf_global': 'spesn',
	'spesn_eea_sf_global': 'spesn',
	'spesn_eea_ti_global': 'spesn',
	'spesn_ru_global': 'spesn',
	'spesn_id_global': 'spesn',
	'spesn_za_mt_global': 'spesn',
	'veux': 'veux',
	'veux_ep_stdee': 'veux',
	'veux_tw_global': 'veux',
	'veux_global': 'veux',
	'veux_eea_global': 'veux',
	'veux_eea_hg_global': 'veux',
	'veux_eea_or_global': 'veux',
	'veux_eea_tf_global': 'veux',
	'veux_eea_by_global': 'veux',
	'veux_eea_vf_global': 'veux',
	'veux_eea_sf_global': 'veux',
	'veux_eea_ti_global': 'veux',
	'veux_ru_global': 'veux',
	'veux_in_global': 'veux',
	'veux_id_global': 'veux',
	'veux_tr_global': 'veux',
	'veux_jp_global': 'veux',
	'veux_cl_en_global': 'veux',
	'veux_lm_cr_global': 'veux',
	'veux_mx_at_global': 'veux',
	'fleur_tw_global': 'fleur',
	'fleur_global': 'fleur',
	'fleur_eea_global': 'fleur',
	'fleur_eea_or_global': 'fleur',
	'fleur_eea_by_global': 'fleur',
	'fleur_eea_sf_global': 'fleur',
	'fleur_ru_global': 'fleur',
	'fleur_in_global': 'fleur',
	'fleur_id_global': 'fleur',
	'fleur_tr_global': 'fleur',
	'fleur_cl_en_global': 'fleur',
	'fleur_lm_cr_global': 'fleur',
	'fleur_mx_at_global': 'fleur',
	'fleur_lm_ms_global': 'fleur',
	'viva_tw_global': 'viva',
	'viva_global': 'viva',
	'viva_eea_global': 'viva',
	'viva_ru_global': 'viva',
	'viva_id_global': 'viva',
	'viva_tr_global': 'viva',
	'viva_lm_cr_global': 'viva',
	'viva_lm_ms_global': 'viva',
	'viva_za_mt_global': 'viva',
	'vida_in_global': 'vida',
	'light': 'light',
	'light_ep_stdce': 'light',
	'light_ep_xy': 'light',
	'light_ep_xdja': 'light',
	'light_ep_stdee': 'light',
	'light_tw_global': 'light',
	'light_global': 'light',
	'light_eea_global': 'light',
	'light_eea_hg_global': 'light',
	'light_eea_or_global': 'light',
	'light_eea_tf_global': 'light',
	'light_eea_by_global': 'light',
	'light_eea_vf_global': 'light',
	'light_eea_sf_global': 'light',
	'light_eea_ti_global': 'light',
	'light_ru_global': 'light',
	'light_in_global': 'light',
	'light_id_global': 'light',
	'light_tr_global': 'light',
	'light_th_as_global': 'light',
	'light_cl_en_global': 'light',
	'light_lm_cr_global': 'light',
	'lightcm': 'lightcm',
	'lightcm_ep_stdee': 'lightcm',
	'opal_tw_global': 'opal',
	'opal_global': 'opal',
	'opal_eea_global': 'opal',
	'opal_eea_hg_global': 'opal',
	'opal_eea_or_global': 'opal',
	'opal_eea_tf_global': 'opal',
	'opal_eea_by_global': 'opal',
	'opal_eea_vf_global': 'opal',
	'opal_eea_sf_global': 'opal',
	'opal_ru_global': 'opal',
	'opal_cl_en_global': 'opal',
	'opal_mx_at_global': 'opal',
	'opal_lm_cr_global': 'opal',
	'xaga': 'xaga',
	'xaga_tw_global': 'xaga',
	'xaga_global': 'xaga',
	'xaga_eea_global': 'xaga',
	'xaga_ru_global': 'xaga',
	'xaga_in_global': 'xaga',
	'xaga_tr_global': 'xaga',
	'sunstone': 'sunstone',
	'sunstone_demo': 'sunstone',
	'sunstone_ep_stdee': 'sunstone',
	'sunstone_ep_tkgwdl': 'sunstone',
	'sunstone_tw_global': 'sunstone',
	'sunstone_global': 'sunstone',
	'sunstone_eea_global': 'sunstone',
	'sunstone_in_global': 'sunstone',
	'ruby': 'ruby',
	'ruby_demo': 'ruby',
	'ruby_ep_stdee': 'ruby',
	'ruby_tw_global': 'ruby',
	'ruby_global': 'ruby',
	'ruby_eea_global': 'ruby',
	'ruby_ru_global': 'ruby',
	'ruby_in_global': 'ruby',
	'ruby_id_global': 'ruby',
	'ruby_kr_global': 'ruby',
	'ruby_tr_global': 'ruby',
	'ruby_cl_en_global': 'ruby',
	'ruby_lm_cr_global': 'ruby',
	'ruby_mx_at_global': 'ruby',
	'ruby_lm_ms_global': 'ruby',
	'redwood': 'redwood',
	'redwood_tw_global': 'redwood',
	'redwood_global': 'redwood',
	'redwood_eea_global': 'redwood',
	'redwood_ru_global': 'redwood',
	'redwood_in_global': 'redwood',
	'redwood_id_global': 'redwood',
	'redwood_tr_global': 'redwood',
	'apollo': 'apollo',
	'apollo_tw_global': 'apollo',
	'apollo_global': 'apollo',
	'apollo_eea_global': 'apollo',
	'apollo_eea_hg_global': 'apollo',
	'apollo_eea_or_global': 'apollo',
	'apollo_eea_tf_global': 'apollo',
	'apollo_eea_vf_global': 'apollo',
	'apollo_eea_sf_global': 'apollo',
	'apollo_eea_ti_global': 'apollo',
	'apollo_ru_global': 'apollo',
	'apollo_in_global': 'apollo',
	'apollo_id_global': 'apollo',
	'apollo_tr_global': 'apollo',
	'apollo_cl_en_global': 'apollo',
	'apollo_mx_tc_global': 'apollo',
	'apollo_lm_cr_global': 'apollo',
	'alioth': 'alioth',
	'alioth_demo': 'alioth',
	'alioth_ep_yunke': 'alioth',
	'alioth_tw_global': 'alioth',
	'alioth_global': 'alioth',
	'alioth_eea_global': 'alioth',
	'andromeda': 'andromeda',
	'andromeda_global': 'andromeda',
	'andromeda_eea_global': 'andromeda',
	'andromeda_eea_vf_global': 'andromeda',
	'apollo_pre': 'apollo',
	'aqua': 'aqua',
	'aries_alpha': 'aries',
	'aries_beta': 'aries',
	'aries': 'aries',
	'MiTwo': 'aries',
	'MI2': 'aries',
	'aries_global': 'aries',
	'armani': 'armani',
	'armani_global': 'armani',
	'atom': 'atom',
	'atom_pre': 'atom',
	'begonia': 'begonia',
	'begonia_global': 'begonia',
	'begonia_eea_global': 'begonia',
	'begonia_ru_global': 'begonia',
	'begoniain_in_global': 'begonia',
	'begonia_id_global': 'begonia',
	'begonia_mx_tc_global': 'begonia',
	'begonia_lm_cr_global': 'begonia',
	'beryllium_global': 'beryllium',
	'beryllium_ru_global': 'beryllium',
	'bomb': 'bomb',
	'bomb_pre': 'bomb',
	'cactus': 'cactus',
	'cactus_global': 'cactus',
	'cactus_ru_global': 'cactus',
	'cancro_lte_ct_alpha': 'cancro_lte_ct',
	'cancro_lte_ct': 'cancro_lte_ct',
	'cancro_alpha': 'cancro',
	'cancro': 'cancro',
	'MI3-WCDMA': 'cancro',
	'cancro_chinaunicom': 'cancro',
	'cancro_global': 'cancro',
	'cappu': 'cappu',
	'capricorn': 'capricorn',
	'capricorn_global': 'capricorn',
	'cepheus': 'cepheus',
	'cepheus_global': 'cepheus',
	'cepheus_eea_global': 'cepheus',
	'cepheus_eea_or_global': 'cepheus',
	'cepheus_eea_vf_global': 'cepheus',
	'cepheus_ru_global': 'cepheus',
	'cepheus_lm_cr_global': 'cepheus',
	'cepheus_eea_hg_global': 'cepheus',
	'cepheus_mx_tc_global': 'cepheus',
	'cereus': 'cereus',
	'cereus_global': 'cereus',
	'cereus_eea_sf_global': 'cereus',
	'cereus_ru_global': 'cereus',
	'chiron': 'chiron',
	'chiron_global': 'chiron',
	'clover': 'clover',
	'crux': 'crux',
	'daisy_global': 'daisy',
	'davinci': 'davinci',
	'davinci_global': 'davinci',
	'davinci_eea_global': 'davinci',
	'davinci_ru_global': 'davinci',
	'davinciin_in_global': 'davinci',
	'dior': 'dior',
	'dior_global': 'dior',
	'dipper': 'dipper',
	'dipper_global': 'dipper',
	'dipper_ru_global': 'dipper',
	'equuleus': 'equuleus',
	'equuleus_global': 'equuleus',
	'equuleus_ru_global': 'equuleus',
	'ferrari': 'ferrari',
	'ferrari_global': 'ferrari',
	'gemini_alpha': 'gemini',
	'gemini': 'gemini',
	'gemini_global': 'gemini',
	'ginkgo': 'ginkgo',
	'ginkgo_global': 'ginkgo',
	'ginkgo_eea_global': 'ginkgo',
	'ginkgo_ru_global': 'ginkgo',
	'ginkgo_in_global': 'ginkgo',
	'ginkgo_id_global': 'ginkgo',
	'ginkgo_mx_tc_global': 'ginkgo',
	'gram_in_global': 'gram',
	'grus': 'grus',
	'grus_global': 'grus',
	'grus_eea_global': 'grus',
	'grus_eea_or_global': 'grus',
	'grus_ru_global': 'grus',
	'gucci': 'gucci',
	'gucci_global': 'gucci',
	'helium': 'helium',
	'helium_global': 'helium',
	'hennessy': 'hennessy',
	'hermes': 'hermes',
	'hermes_global': 'hermes',
	'wt98007': 'HM2013023',
	'wt96007': 'HM2014501',
	'hydrogen': 'hydrogen',
	'hydrogen_global': 'hydrogen',
	'ido_xhdpi': 'ido_xhdpi',
	'ido_xhdpi_global': 'ido_xhdpi',
	'jasmine_global': 'jasmine',
	'jason': 'jason',
	'jason_global': 'jason',
	'kate_global': 'kate',
	'kenzo': 'kenzo',
	'kenzo_global': 'kenzo',
	'land': 'land',
	"TANZANITEIDGlobal":"tanzanite",
	"tanzanite_id_global":"tanzanite",
	"TANZANITELMCRGlobal" : "tanzanite",
	"tanzanite_lm_cr_global" : "tanzanite",
	"BERYLLMCRGlobal" : "beryl",
	"beryl_lm_cr_global" : "beryl",
	"AMETHYSTLMCRGlobal" : "amethyst",
	"amethyst_lm_cr_global" : "amethyst",
	'land_global': 'land',
	'latte': 'latte',
	'laurel_sprout_global': 'laurel_sprout',
	'laurel_sprout_eea_global': 'laurel_sprout',
	'laurel_sprout_mx_tc_global': 'laurel_sprout',
	'RENOIRDEMO':'renoir',
	'laurus': 'laurus',
	'lavender': 'lavender',
	'lavender_global': 'lavender',
	'lavender_eea_global': 'lavender',
	'lavender_ru_global': 'lavender',
	'lavender_in_global': 'lavender',
	'lavender_mx_tc_global': 'lavender',
	'lcsh92_wet_jb9': 'lcsh92_wet_jb9',
	'lcsh92_wet_jb9_global': 'lcsh92_wet_jb9',
	'lcsh92_wet_xm_td': 'lcsh92_wet_xm_td',
	'leo': 'leo',
	'libra': 'libra',
	'lithium': 'lithium',
	'lithium_global': 'lithium',
	'lmi_pre': 'lmi',
	'lmi': 'lmi',
	'lmi_global': 'lmi',
	'lmi_eea_global': 'lmi',
	'lmi_ru_global': 'lmi',
	'lmi_id_global': 'lmi',
	'lmi_tr_global': 'lmi',
	'lotus': 'lotus',
	'lotus_global': 'lotus',
	'lotus_ru_global': 'lotus',
	'lte26007': 'lte26007',
	'markw': 'markw',
	'markw_global': 'markw',
	'meri': 'meri',
	'mido': 'mido',
	'mido_global': 'mido',
	'mione_plus': 'mione_plus',
	'MI1': 'mione_plus',
	'Mioneplus': 'mione_plus',
	'MiOne': 'mione_plus',
	'MioneplusCDMA': 'mione_plus',
	'MioneplusCU': 'mione_plus',
	'QDS84': 'mione_plus',
	'QDS81': 'mione_plus',
	'QDR68': 'mione_plus',
	'QDR66': 'mione_plus',
	'QDR65': 'mione_plus',
	'QDQ61': 'mione_plus',
	'QDO53': 'mione_plus',
	'QDN43': 'mione_plus',
	'mocha': 'mocha',
	'mocha_global': 'mocha',
	'natrium': 'natrium',
	'natrium_global': 'natrium',
	'nikel': 'nikel',
	'nikel_global': 'nikel',
	'nitrogen': 'nitrogen',
	'nitrogen_global': 'nitrogen',
	'nitrogen_ru_global': 'nitrogen',
	'olive': 'olive',
	'olive_global': 'olive',
	'olive_eea_global': 'olive',
	'olive_eea_hg_global': 'olive',
	'olive_ru_global': 'olive',
	'olive_in_global': 'olive',
	'olive_id_global': 'olive',
	'olivelite': 'olivelite',
	"serenity_id_global":"serenity",
	"SERENITYIDGlobal":"serenity",
	"taiko_tw_global": "taiko",
	"taiko_global": "taiko",
	"koto_global": "koto",
	"koto_tw_global": "koto",
	"koto_eea_global": "koto",
	"taiko_eea_global": "taiko",
	"taiko_in_global": "taiko",
	'olivelite_global': 'olivelite',
	'olivelite_eea_global': 'olivelite',
	'olivelite_ru_global': 'olivelite',
	'olivelite_in_global': 'olivelite',
	'olivelite_id_global': 'olivelite',
	'olivelite_mx_tc_global': 'olivelite',
	'olivelite_lm_cr_global': 'olivelite',
	'olivewood_in_global': 'olivewood',
	'olivewood_id_global': 'olivewood',
	'omega': 'omega',
	'onc_in_global': 'onc',
	'onclite': 'onclite',
	'onclite_global': 'onclite',
	'onclite_eea_global': 'onclite',
	'onclite_ru_global': 'onclite',
	'onclite_in_global': 'onclite',
	'onclite_mx_tc_global': 'onclite',
	'onclite_lm_cr_global': 'onclite',
	'oxygen': 'oxygen',
	'oxygen_global': 'oxygen',
	'perseus': 'perseus',
	"SERENITYINGlobal":"serenity",
	"serenity_in_global":"serenity",
	"SERENITYGTTGGlobal":"serenity",
	"serenity_gt_tg_global":"serenity",
	"BERYLGTTGGlobal":"beryl",
	"beryl_gt_tg_global":"beryl",
	"SERENITYMXATGlobal":"serenity",
	"serenity_mx_at_global":"serenity",
	"SERENITYLMMSGlobal":"serenity",
	"serenity_lm_ms_global":"serenity",
	'perseus_global': 'perseus',
	'perseus_h3g_global': 'perseus',
	'perseus_ru_global': 'perseus',
	'phoenix_pre': 'phoenix',
	'phoenix': 'phoenix',
	'phoenixin_in_global': 'phoenix',
	'picasso_48m': 'picasso_48m',
	'picasso_48m_pre': 'picasso_48m',
	'picasso_pre': 'picasso',
	'picasso': 'picasso',
	'pine': 'pine',
	'pine_global': 'pine',
	'pine_eea_global': 'pine',
	'pine_eea_or_global': 'pine',
	'pine_eea_tf_global': 'pine',
	'pine_eea_vf_global': 'pine',
	'pine_eea_sf_global': 'pine',
	'pine_ru_global': 'pine',
	'pine_in_global': 'pine',
	'pisces_alpha': 'pisces',
	'pisces': 'pisces',
	'MI3-TD': 'pisces',
	'pisces_chinamobile': 'pisces',
	'platina': 'platina',
	'platina_global': 'platina',
	'platina_ru_global': 'platina',
	'polaris': 'polaris',
	'polaris_global': 'polaris',
	'polaris_ru_global': 'polaris',
	'prada': 'prada',
	'prada_global': 'prada',
	'pyxis': 'pyxis',
	'pyxis_global': 'pyxis',
	'pyxis_eea_global': 'pyxis',
	'pyxis_eea_tf_global': 'pyxis',
	'pyxis_eea_vf_global': 'pyxis',
	'pyxis_eea_sf_global': 'pyxis',
	'pyxis_ru_global': 'pyxis',
	"malachite_tw_global" : "malachite",
	"MALACHITETWGlobal" : "malachite",
	"malachite_global" : "malachite",
	"MALACHITEGlobal" : "malachite",
	"malachite_eea_global" : "malachite",
	"MALACHITEEEAGlobal" : "malachite",
	"rodin_demo" : "rodin",
	"LAKE" : "lake",
	"lake" : "lake",
	"MALACHITEDCGlobal":"malachite",
	"malachite_dc_global":"malachite",
	"tanzanite_dc_global":"tanzanite",
	"TANZANITEDCGlobal":"tanzanite",
	"tanzanite_global":"tanzanite",
	"TANZANITEGlobal":"tanzanite",
	"uke_in_global" : "uke",
	"obsidian_eea_global" : "obsidian",
	"obsidian_global" : "obsidian",
	"obsidian_dc_global" : "obsidian",
	"OBSIDIANGlobal" : "obsidian",
	"OBSIDIANDCGlobal" : "obsidian",
	"OBSIDIANEEAGlobal" : "obsidian",
	"obsidian_ru_global" : "obsidian",
	"obsidian_tr_global" : "obsidian",
	"OBSIDIANRUGlobal" : "obsidian",
	"OBSIDIANTRGlobal" : "obsidian",
	"rodin_in_global":"rodin",
	'raphael': 'raphael',
	'raphael_global': 'raphael',
	'raphael_eea_global': 'raphael',
	'raphael_ru_global': 'raphael',
	'raphaelin_in_global': 'raphael',
	'raphaels': 'raphaels',
	'riva': 'riva',
	'riva_global': 'riva',
	'rolex': 'rolex',
	'rolex_global': 'rolex',
	'rosy': 'rosy',
	'rosy_global': 'rosy',
	'rosy_ru_global': 'rosy',
	'sagit': 'sagit',
	'sagit_global': 'sagit',
	'sakura': 'sakura',
	'sakura_india_global': 'sakura',
	'santoni': 'santoni',
	'santoni_global': 'santoni',
	'scorpio': 'scorpio',
	'scorpio_global': 'scorpio',
	'shiva_in_global': 'shiva',
	'sirius': 'sirius',
	'taurus_beta': 'taurus',
	'taurus': 'taurus',
	'MI2A': 'taurus',
	'MiTwoA': 'taurus',
	'tiare_global': 'tiare',
	'tiare_eea_global': 'tiare',
	'tiare_ru_global': 'tiare',
	'tiare_in_global': 'tiare',
	'tiffany': 'tiffany',
	'tissot': 'tissot',
	'tissot_global': 'tissot',
	'tucana': 'tucana',
	'tucana_global': 'tucana',
	'tucana_eea_global': 'tucana',
	'tucana_eea_hg_global': 'tucana',
	'tucana_eea_or_global': 'tucana',
	'tucana_eea_tf_global': 'tucana',
	'tucana_eea_vf_global': 'tucana',
	'tucana_eea_ti_global': 'tucana',
	'tucana_ru_global': 'tucana',
	'tucana_id_global': 'tucana',
	'tucana_mx_tc_global': 'tucana',
	'tulip_global': 'tulip',
	'tulip_ru_global': 'tulip',
	'ugg': 'ugg',
	'ugg_global': 'ugg',
	'ugglite': 'ugglite',
	'ugglite_global': 'ugglite',
	'ursa': 'ursa',
	'vela': 'vela',
	"BERYLRUGlobal":"beryl",
	"beryl_ru_global":"beryl",
	'venus_pre': 'venus',
	'vince': 'vince',
	'vince_global': 'vince',
	'vince_ru_global': 'vince',
	'violet': 'violet',
	'violet_in_global': 'violet',
	'virgo_lte_ct': 'virgo_lte_ct',
	'virgo_alpha': 'virgo',
	'virgo': 'virgo',
	'virgo_global': 'virgo',
	'wayne': 'wayne',
	'whyred': 'whyred',
	"xuanyuan_in_global":"xuanyuan",
	"emerald_r_eea_global":"emerald_r",
	"EMERALDREEAGlobal":"emerald_r",
	"EMERALDRGlobal":"emerald_r",
	"EMERALDRTRGlobal":"emerald_r",
	"emerald_r_tr_global":"emerald_r",
	"EMERALDRGlobal":"emerald_r",
	"emerald_r_global":"emerald_r",
	"EMERALDRGlobal":"emerald_r",
	"malachite_ru_global":"malachite",
	"MALACHITERUGlobal":"malachite",
	'whyred_global': 'whyred',
	'whyred_ru_global': 'whyred',
	'willow_global': 'willow',
	'willow_eea_global': 'willow',
	'willow_eea_hg_global': 'willow',
	'willow_eea_or_global': 'willow',
	'willow_eea_tf_global': 'willow',
	'willow_eea_vf_global': 'willow',
	'willow_eea_ti_global': 'willow',
	'willow_ru_global': 'willow',
	"miro_tw_global":"miro",
	"miro_global":"miro",
	"miro_eea_global":"miro",
	"miro_ru_global":"miro",
	"miro_id_global":"miro",
	"miro_tr_global":"miro",
	"zorn_tw_global":"zorn",
	"zorn_global":"zorn",
	"zorn_eea_global":"zorn",
	"zorn_ru_global":"zorn",
	"zorn_id_global":"zorn",
	"zorn_tr_global":"zorn",
	'wt86047_pro': 'wt86047_pro',
	'wt86047': 'wt86047',
	'wt88047_pro': 'wt88047_pro',
	'ysl': 'ysl',
	'wt88047_pro_global': 'wt88047_pro',
	'wt88047': 'wt88047',
	'wt88047_global': 'wt88047',
	'wt93807': 'wt93807',
	'HM2013023_sg_global': 'wt98007',
	'ysl_global': 'ysl',
	'ysl_ru_global': 'ysl',
	'ysl_cl_Movistar_global': 'ysl',
	'alioth_ru_global': 'alioth',
	'alioth_in_global': 'alioth',
	'alioth_id_global': 'alioth',
	'alioth_tr_global': 'alioth',
	'haydn': 'haydn',
	'haydn_global': 'haydn',
	"chenfeng_demo": "chenfeng",
	"CHENFENGDEMO": "chenfeng",
	'haydn_eea_global': 'haydn',
	'haydn_eea_hg_global': 'haydn',
	'haydn_eea_or_global': 'haydn',
	'haydn_eea_tf_global': 'haydn',
	'haydn_eea_by_global': 'haydn',
	'haydn_eea_vf_global': 'haydn',
	'haydn_eea_sf_global': 'haydn',
	'haydn_eea_ti_global': 'haydn',
	'haydn_in_global': 'haydn',
	'ares': 'ares',
	'ares_in_global': 'ares',
	'munch': 'munch',
	'munch_tw_global': 'munch',
	'munch_global': 'munch',
	'munch_eea_global': 'munch',
	'munch_ru_global': 'munch',
	'munch_in_global': 'munch',
	'munch_id_global': 'munch',
	'munch_tr_global': 'munch',
	'ingres': 'ingres',
	'ingres_tw_global': 'ingres',
	'ingres_global': 'ingres',
	'ingres_eea_global': 'ingres',
	'ingres_ru_global': 'ingres',
	'ingres_id_global': 'ingres',
	'ingres_tr_global': 'ingres',
	'rubens': 'rubens',
	'rubens_demo': 'rubens',
	'rubens_ep_stdee': 'rubens',
	'rubens_ep_yx': 'rubens',
	'matisse': 'matisse',
	'matisse_demo': 'matisse',
	'matisse_ep_stdee': 'matisse',
	'diting': 'diting',
	'diting_demo': 'diting',
	'diting_ep_stdee': 'diting',
	'diting_tw_global': 'diting',
	'diting_global': 'diting',
	'diting_eea_global': 'diting',
	'diting_ru_global': 'diting',
	'diting_tr_global': 'diting',
	'diting_cl_en_global': 'diting',
	"creek_global": "creek",
	'diting_lm_cr_global': 'diting',
	'diting_mx_at_global': 'diting',
	'diting_jp_global': 'diting',
	'THYMEDEMO': 'thyme',
	'mondrian': 'mondrian',
	"creek_tw_global": "creek",
	"flourite_demo" : "flourite",
	"flourite" : "flourite",
	"kunzite" : "kunzite",
	"creek_eea_global": "creek",
	"spring_in_global": "spring",
	"creek_ru_global": "creek",
	"creek_id_global": "creek",
	"dew_tw_global": "dew",
	"dew_global": "dew",
	"dew_dc_global": "dew",
	"dew_eea_global": "dew",
	"dew_ru_global": "dew",
	"dew_id_global": "dew",
	"dew_tr_global": "dew",
	"spring": "spring",
	"KONGHOU": "konghou",
	"konghou": "konghou",
	"tornado_global": "tornado",
	"tornado_dc_global": "tornado",
	"malachite_gt_tg_global": "malachite",
	"piano": "piano",
	"piano_demo": "piano",
	"yupei": "yupei",
	"yupei_demo": "yupei",
	"pudding": "pudding",
	"pudding_demo": "pudding",
	"popsicle": "popsicle",
	"popsicle_demo": "popsicle",
	"pandora": "pandora",
	"pandora_demo": "pandora",
	"tornado": "tornado",
	"tornado_demo": "tornado",
	"creek_lm_cr_global": "creek",
	"klimt_jp_global": "klimt",
	"goya_global": "goya",
	"goya_id_global": "goya",
	"goya_eea_global": "goya",
	"goya_ru_global": "goya",
	"goya_tr_global": "goya",
	"klimt_global": "klimt",
	"klimt_eea_global": "klimt",
	"klimt_id_global": "klimt",
	"klimt_ru_global": "klimt",
	"klimt_tw_global": "klimt",
	"klimt_tr_global": "klimt",
	"flute_eea_global": "flute",
	"goya_tw_global": "goya",
	"goya_dc_global": "goya",
	"klimt_dc_global": "klimt",
	"tornado_eea_global": "tornado",
	"kunzite_demo" : "kunzite",
	"lapis" : "lapis",
	"lapis_demo" : "lapis",
	'mondrian_demo': 'mondrian',
	'mondrian_ep_stdee': 'mondrian',
	'mondrian_tw_global': 'mondrian',
	'mondrian_global': 'mondrian',
	'mondrian_eea_global': 'mondrian',
	'mondrian_ru_global': 'mondrian',
	'mondrian_tr_global': 'mondrian',
	'socrates': 'socrates',
	'socrates_demo': 'socrates',
	'socrates_ep_stdee': 'socrates',
	'rembrandt': 'rembrandt',
	'rembrandt_demo': 'rembrandt',
	'rembrandt_ep_stdee': 'rembrandt',
	'yunluo': 'yunluo',
	'yunluo_ep_stdee': 'yunluo',
	'yunluo_demo': 'yunluo',
	'yunluo_tw_global': 'yunluo',
	'yunluo_global': 'yunluo',
	'yunluo_eea_global': 'yunluo',
	'yunluo_ru_global': 'yunluo',
	'yunluo_in_global': 'yunluo',
	'yunluo_id_global': 'yunluo',
	'yunluo_tr_global': 'yunluo',
	'ice_tw_global': 'ice',
	'ice_global': 'ice',
	'ice_eea_global': 'ice',
	'ice_ru_global': 'ice',
	'ice_in_global': 'ice',
	'ice_id_global': 'ice',
	'ice_mx_tc_global': 'ice',
	'ice_lm_cr_global': 'ice',
	'ice_za_mt_global': 'ice',
	'ice_za_vc_global': 'ice',
	'angelicain_in_rf_global': 'angelicain',
	'frost_tw_global': 'frost',
	'frost_global': 'frost',
	'frost_eea_global': 'frost',
	'frost_ru_global': 'frost',
	'frost_id_global': 'frost',
	'frost_tr_global': 'frost',
	'citrus_tw_global': 'citrus',
	'citrus_global': 'citrus',
	'citrus_eea_global': 'citrus',
	'citrus_ru_global': 'citrus',
	'citrus_in_global': 'citrus',
	'citrus_id_global': 'citrus',
	'citrus_tr_global': 'citrus',
	'evergreen_tw_global': 'evergreen',
	'evergreen_global': 'evergreen',
	'evergreen_eea_global': 'evergreen',
	'evergreen_ru_global': 'evergreen',
	'evergreen_tr_global': 'evergreen',
	'rosemary_p_tw_global': 'rosemary_p',
	'rosemary_p_global': 'rosemary_p',
	'rosemary_p_eea_global': 'rosemary_p',
	'rosemary_p_ru_global': 'rosemary_p',
	'rosemary_p_id_global': 'rosemary_p',
	'rosemary_p_tr_global': 'rosemary_p',
	"lake_ru_global" : "lake",
	"LAKERUGlobal" : "lake",
	'surya_global': 'surya',
	"rodin_tw_global":"rodin",
	"rodin_ru_global":"rodin",
	"RODINTWGlobal":"rodin",
	"RODINRUGlobal":"rodin",
	'surya_eea_global': 'surya',
	'surya_ru_global': 'surya',
	'surya_in_global': 'surya',
	'surya_id_global': 'surya',
	'surya_tr_global': 'surya',
	'vayu_tw_global': 'vayu',
	'vayu_global': 'vayu',
	'vayu_eea_global': 'vayu',
	'vayu_ru_global': 'vayu',
	'vayu_in_global': 'vayu',
	'vayu_id_global': 'vayu',
	'xun_ru_global': 'xun',
	'xun_tr_global': 'xun',
	"ruyi_ru_global": "ruyi",
	"RUYIRUGlobal": "ruyi",
	"FLARETRGlobal": "flare",
	"flare_tr_global": "flare",
	"dada": "dada",
	"haotian": "haotian",
	"beryl_ep_stdee": "beryl",
	"BERYLEPSTDEE": "beryl",
	"rothko_jp_global": "rothko",
	"ROTHKOJPGlobal": "rothko",
	"uke": "uke",
	"muyu": "muyu",
	"amethyst_mx_at_global":"amethyst",
	"AMETHYSTMXATGlobal":"amethyst",
	"TANZANITEMXATGlobal":"tanzanite",
	"tanzanite_mx_at_global": "tanzanite",
	"OBSIDIANMXATGlobal":"obsidian",
	"obsidian_mx_at_global": "obsidian",
	"MALACHITEIDGlobal":"malachite",
	"malachite_id_global":"malachite",
	"rothko_ep_stdee": "rothko",
	"ROTHKOEPSTDEE": "rothko",
	"sapphiren_id_global": "sapphiren",
	"SAPPHIRENIDGlobal": "sapphiren",
	'vayu_tr_global': 'vayu',
	'moonstone_tw_global': 'moonstone',
	'moonstone_global': 'moonstone',
	'moonstone_eea_global': 'moonstone',
	'moonstone_ru_global': 'moonstone',
	'moonstone_in_global': 'moonstone',
	'moonstone_id_global': 'moonstone',
	'moonstone_tr_global': 'moonstone',
	"EMERALDRRUGlobal":"emerald_r",
	"SERENITYEEAGlobal":"serenity",
	"blue_dc_global": "blue",
	"BLUEDCGlobal": "blue",
	"SERENITYEEAORGlobal": "serenity",
	"SERENITYEEAVFGlobal": "serenity",
	"SERENITYEEABYGlobal": "serenity",
	"serenity_eea_or_global": "serenity",
	"serenity_eea_vf_global": "serenity",
	"serenity_eea_by_global": "serenity",
	"dijun":"dijun",
	"dijun_demo":"dijun",
	"jinghu":"jinghu",
	"jinghu_demo":"jinghu",
	"luming":"luming",
	"luming_demo":"luming",
	"serenity_eea_global":"serenity",
	"emerald_r_ru_global":"emerald_r"
}

def parse_version(version):
	try:
		if version.startswith("V") and ".EP" not in version:
			body = version[1:]
		elif ".EP" in version:
			body = version[1:].split(".EP")[0]+".EP"
		elif version.startswith("J"):
			body = version[-3:]
		else:
			body = version
		version_part = body.split(".")
		if len(version_part) == 3:
			vlen = len(body.split("."))
		else:
			vlen = len(body.split("."))-1
		numeric_parts = tuple(map(int, version_part[:vlen]))
		if len(numeric_parts) <5:
			numeric_parts = numeric_parts + (0,) * (5 - len(numeric_parts))
		else:
			numeric_parts = numeric_parts[:5]
		return numeric_parts
	except Exception:
		return None

def compare(v1, v2):
	if type(v1) == type(v2) == tuple or type(v1) == type(v2) == None:
		return False
	else:
		return parse_version(v1) > parse_version(v2)

def localData(codename):
	if platform == 'win32':
		devdata = json.loads(open('public/MRdata/data/devices/' + codename+'.json', 'r', encoding='utf-8').read()).__str__()
	elif platform == 'darwin':
		devdata = json.loads(open('public/MRdata/data/devices/' + codename+'.json', 'r', encoding='utf-8').read()).__str__()
	else:
		devdata = json.loads(open('/sdcard/Codes/NuxtMR/public/MRdata/data/devices/' + codename+'.json', 'r', encoding='utf-8').read()).__str__()
	return devdata


def loadJson(codename):
	if platform == 'win32':
		devdata = json.loads(open('public/MRdata/data/devices/' + codename+'.json', 'r', encoding='utf-8').read())
	elif platform == 'darwin':
		devdata = json.loads(open('public/MRdata/data/devices/' + codename+'.json', 'r', encoding='utf-8').read())
	else:
		devdata = json.loads(open('/sdcard/Codes/NuxtMR/public/MRdata/data/devices/' + codename+'.json', 'r', encoding='utf-8').read())
	return devdata


def writeData(filename):
	print('发现未收录版本')
	if platform == 'win32':
		file = open('public/MRdata/scripts/NewROMs.txt', 'a', encoding='utf-8')
	elif platform == 'darwin':
		file = open('public/MRdata/scripts/NewROMs.txt', 'a', encoding='utf-8')
	else:
		file = open('/sdcard/Codes/NuxtMR/public/MRdata/script/NewROMs.txt', 'a', encoding='utf-8')
	file.write(filename+'\n')
	file.close()


def writeFlag(flag, device):
	if platform == 'win32':
		file = open('public/MRdata/scripts/Flags.json', 'a', encoding='utf-8')
	elif platform == 'darwin':
		file = open('public/MRdata/scripts/Flags.json', 'a', encoding='utf-8')
	else:
		file = open('/sdcard/Codes/NuxtMR/public/MRdata/scripts/Flags.json', 'a', encoding='utf-8')
	file.write(f"\'{flag}\':\'{device}\',\n")
	file.close()


def getDeviceCode(filename):
	if "_" in filename:
		if "zip" in filename:
			if "miui" in filename:
				rec_seperator = "_"
				rec_spot = 1
			else:
				rec_seperator = "-ota_full"
				rec_spot = 0
			flag = filename.split(rec_seperator)[rec_spot]
			if flag in flags:
				codename = flags[flag]
				return codename
			else:
				print(flag)
				writeFlag(flag, "")
				return 0
		elif '.tgz' in filename:
			if "-A1" in filename:
				flag = filename.split('-images')[0]
			else:
				flag = filename.split('_images')[0]
		else:
			return 0
		if flag in flags:
			codename = flags[flag]
			if filename.split('_images')[0]:
				flag = filename.split('_images')[0]
				codename = flags[flag]
				if flag in flags:
					codename = flags[flag]
					return codename
				else:
					writeFlag(flag, "")
					return 0
		elif '.exe' in filename:
			if filename.split('_')[1]:
				flag = filename.split('_')[1]
				codename = flags[flag]
				if flag in flags:
					codename = flags[flag]
					return codename
				else:
					writeFlag(flag, "")
					return 0
		else:
			return 0
	else:
		return 0


def getFastboot(url):
	s = requests.Session()
	s.mount('http://', HTTPAdapter(max_retries=3))
	s.mount('https://', HTTPAdapter(max_retries=3))
	headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
				 'Connection': 'close'}
	try:
		response = s.post(url, headers=headers, json=True)
		if (response.status_code == 200):
			content = response.content.decode('utf8')
			if content == '':
				i = 0
			else:
				data = json.loads(content)['LatestFullRom']
				if len(data) > 0:
					checkExist(data['filename'])
				else:
					i = 0
		else:
			i = 0
	except requests.exceptions.RequestException as e:
		i = 0
	s.close()

def db_job(sql):
	cnx = None
	try:
		cnx = Connection(
			user=config.user,
			password=config.password,
			host=config.host,
			port=config.port,
			database=config.database,
			autocommit=True
			)
		cursor = cnx.cursor()
		cursor.execute(sql)
		return cursor.fetchall()
	except Exception as e:
		print(sql,e)
	finally:
		if cnx:
			cnx.close()

def db_job_latest(sql):
	cnx = None
	try:
		cnx = Connection(
			user=config.user,
			password=config.password,
			host=config.host,
			port=config.port,
			database=config.database,
			autocommit=True
			)
		cursor = cnx.cursor()
		cursor.execute(sql)
		return cursor.fetchone()
	except Exception as e:
		print(sql,e)
	finally:
		if cnx:
			cnx.close()

def stringify(s):
		return f"'{s}'"
def get_time(url):
	try:
		response = requests.head(url, allow_redirects=True)
		if 'Last-Modified' in response.headers:
			last_modified_str = response.headers['Last-Modified']
			date = datetime.strptime(last_modified_str, "%a, %d %b %Y %H:%M:%S %Z") + timedelta(hours=8)
			return date.strftime("%Y-%m-%d")
		else:
			return ""
	except requests.RequestException as e:
		return f"访问URL失败: {e}"
def get_version(filename):
	if ".zip" in filename:
		if "miui" in filename:
			version = filename.split("_")[2]
		else:
			version = filename.split("ota_full-")[1].split("-")[0]
	else:
		version = filename.split("images_")[1].split("_")[0]
	return version
def get_android(filename):
	if ".zip" in filename:
		if "miui" in filename:
			android = filename.split("_")[4].split(".zip")[0]
		else:
			android = filename.split("ota_full-")[1].split("-")[2]
	else:
		android = filename.split("images_")[1].split("_")[2]
	return android
def form_url(filename,version):
	return 'https://bkt-sgp-miui-ota-update-alisgp.oss-ap-southeast-1.aliyuncs.com/'+version+"/"+filename
def get_flag(filename):
	if "_" in filename:
		if "zip" in filename:
			if "miui" in filename:
				rec_seperator = "_"
				rec_spot = 1
			else:
				rec_seperator = "-ota_full"
				rec_spot = 0
			flag = filename.split(rec_seperator)[rec_spot]
		elif '.tgz' in filename:
			flag = filename.split('_images')[0]
	else:
		flag = 0
	return flag

def checkExist(filename):
	if 'blockota' in filename or 'miui-ota' in filename:
		i = 0
	else:
		newROM = open("public/MRData/scripts/NewROMs.txt", 'r', encoding='utf-8').read()
		if '_OS' in filename or '-OS' in filename or "A1" in filename:
			checkOSExist(filename)
		elif getDeviceCode(filename) == 0:
			writeData(filename)
		elif filename in localData(getDeviceCode(filename)) or filename in newROM:
			i = 0
		else:
			device, code, android, version, type, bigver, region,tag,zone, branch, filetype, filename = [item for item in getData(filename)]
			checkDatabase(device, code, android, version, type, bigver, region,tag,zone, branch, filetype, filename)
			writeData(filename)

def getBranchcode(filename):
	if filename.endswith(".zip"):
		if filename.startswith("miui"):
			branchCode = filename.split("_")[1]
			get_sql = "SELECT code FROM devices WHERE branchcode = %s" % (stringify(branchCode))
			if len(db_job(get_sql)) > 0:
				return db_job(get_sql)[0][0]
			else:
				return 0
		else:
			return filename.split("-")[0]
	elif filename.endswith(".tgz"):
		return filename.split('_images')[0]

def getRegion(filename):
	if ".zip" in filename:
		if filename.startswith("miui"):
			branchCode = filename.split("_")[1]
			get_sql = "SELECT region FROM devices WHERE branchcode = %s" % (stringify(branchCode))
			if len(db_job(get_sql)) > 0:
				if db_job(get_sql)[0][0] is None:
					return ""
				else:
					return db_job(get_sql)[0][0]
			else:
				return ""
		else:
			if filename.split("_")[0] == getDeviceCode(filename)+"-ota":
				return "cn"
			else:
				return filename.split("_")[1].split('-')[0]
	else:
		code = filename.split('_images')[0]
		get_sql = f"SELECT region FROM devices WHERE code = %s" % (stringify(code))
		if len(db_job(get_sql)) > 0:
			if db_job(get_sql)[0][0] is None:
				return ""
			else:
				return db_job(get_sql)[0][0]
		else:
			 return ""
	
def getTag(filename):
	if ".zip" in filename:
		if filename.startswith("miui"):
			branchCode = filename.split("_")[1]
			get_sql = "SELECT tag FROM devices WHERE branchcode = %s" % (stringify(branchCode))
			if len(db_job(get_sql)) > 0:
				if db_job(get_sql)[0][0] is None:
					return ""
				else:
					return db_job(get_sql)[0][0]
			else:
				return ""
		else:
			code = filename.split("-")[0]
			if "CNXM" in filename:
				if get_version(filename).split(".")[3] == 0 or get_version(filename).split(".")[3] == "0":
					return "CnOO"
				else:
					return "CnOB"
			else:
				get_sql = f"SELECT tag FROM devices WHERE code = %s" % (stringify(code))
				if len(db_job(get_sql)) > 0:
					if db_job(get_sql)[0][0] is None:
						return ""
					else:
						return db_job(get_sql)[0][0]
				else:
					return ""
	else:
		code = filename.split("-")[0]
		get_sql = f"SELECT tag FROM devices WHERE code = %s" % (stringify(code))
		if len(db_job(get_sql)) > 0:
			if db_job(get_sql)[0][0] is None:
				return ""
			else:
				return db_job(get_sql)[0][0]
		else:
			return ""
def getCode(filename):
	if ".zip" in filename:
		if "-ota_full" in filename:
			return filename.split("-")[0]
		else:
			code = filename.split("_")[1]
		get_sql = f"SELECT code FROM devices WHERE branchcode = '{code}'"
		if len(db_job(get_sql)) > 0:
			return db_job(get_sql)[0][0]
		else:
			return 0
	elif ".tgz" in filename:
		return filename.split('_images')[0]

def getData(filename):
	if "miui" in filename:
		filetype = "recovery"
		android = filename.split("_")[4].split(".zip")[0]
		version = filename.split("_")[2]
		get_sql = "SELECT code,device FROM devices WHERE branchcode = %s" % (stringify(filename.split("_")[1]))
		data = db_job_latest(get_sql)
		if data is not None:
			code = data[0]
			device = data[1]
		else:
			print(filename.split("_")[1])
			if ".EP" in filename:
				devtag = filename.split("_")[1].split("EPS")[0].lower()
			else:
				devtag = version.split(".")[4][1:3]
			ver_code = version[-4:]
			info = db_job_latest("SELECT tag,code,region FROM branches WHERE vercode = %s" % (stringify(ver_code)))
			tag,code,region = [item for item in info]
			device = db_job_latest("SELECT device FROM devices WHERE devtag = %s" % (stringify(devtag)))[0]
			code = device+code
			ins_sql = "INSERT INTO devices(device,devtag,code,tag,region,devcode,branchcode) VALUES (%s,%s,%s,%s,%s,%s,%s)" % (stringify(device),stringify(devtag),stringify(code),stringify(tag),stringify(region),stringify(version[-6:]),stringify(filename.split("_")[1]))
			db_job_latest(ins_sql)
	else:
		if filename.endswith(".tgz"):
			filetype = "fastboot"
			if "-images" in filename:
				android = filename.split("images-")[1].split("-")[3]
				version = filename.split("images-")[1].split("-")[0]
				code = filename.split('-images')[0]
			else:
				android = filename.split("images_")[1].split("_")[2]
				version = filename.split("images_")[1].split("_")[0]
				code = filename.split('_images')[0]
		else:
			filetype = "recovery"
			android = filename.split("ota_full-")[1].split("-")[2]
			version = filename.split("ota_full-")[1].split("-")[0]
			code = filename.split("-ota_full")[0]
		data = db_job_latest("SELECT device FROM roms where code = %s" % (stringify(code)))
		if data is not None:
			device = data[0]
		else:
			device = db_job_latest("SELECT device FROM devices where code = %s" % (stringify(code)))[0]
	if version.startswith('V'):
		type = "MIUI"
		bigver = "MIUI " + version.split('V')[1].split('.')[0]
	elif version.startswith('OS'):
		type = "HyperOS"
		bigver = "HyperOS " + version.split('OS')[1].split('.')[0]
	elif version.startswith('A'):
		type = "STAN"
		bigver = "STAN " + version.split('.')[0]
	if code == 0:
		return 0
	else:
		if "CNXM" in version:
			if version.split(".")[3] == 0 or version.split(".")[3] == "0":
				tag = "CnOO"
			else:
				tag = "CnOB"
			region = "cn"
			zone = 1
		else:
			info_sql = "SELECT region,tag,zone FROM roms WHERE code = %s" % (stringify(code))
			data = db_job_latest(info_sql)
			if data is not None:
				if len(data) > 0:
					region,tag,zone = [item for item in data]
				else:
					region,tag,zone = db_job_latest(info_sql)
			else:
				data = db_job_latest("SELECT region,tag FROM devices WHERE code = %s" % (stringify(code)))
				region,tag = [item for item in data]
				if region == "cn":
					zone = 1
				else:
					zone = 2
	return device, code, android, version, type, bigver, region,tag,zone, "F", filetype, filename
	
def checkDatabase(device, code, android, version, type, bigver, region,tag,zone,branch, filetype, filename):
	if filetype == "recovery":
		checkpoint = "recovery"
	else:
		if "chinatelecom" in filename:
			checkpoint = "ctelecom"
		elif "chinaunicom" in filename:
			checkpoint = "cunicom"
		elif "chinamobile" in filename:
			checkpoint = "cmobile"
		else:
			checkpoint = "fastboot"
	get_sql = f"SELECT id,{checkpoint},others FROM roms WHERE code = %s and version = %s" % (stringify(code), stringify(version))
	data = db_job_latest(get_sql)
	if data is not None:
		if len(data) > 0:
			if data[1] == filename:
				pass
			elif data[1] == None:
				if filetype == "recovery":
					beta_date = stringify(get_time(form_url(filename,version)))
					upd_sql = f"UPDATE roms SET {checkpoint} = %s, beta_date = %s WHERE id = %d" % (stringify(filename),beta_date, data[0])
				else:
					public_date = stringify(get_time(form_url(filename,version)))
					upd_sql = f"UPDATE roms SET {checkpoint} = %s, public_date = %s WHERE id = %d" % (stringify(filename),public_date, data[0])
				db_job_latest(upd_sql)
			else:
				if data[2] == None or data[2] == "":
					others = []
					others.append(filename)
					update_sql = f"UPDATE roms SET others = '{json.dumps(others)}' WHERE id = %d" % (data[0])
					db_job_latest(update_sql)
				elif filename in data[2]:
					pass
				else:
					others = list(json.loads(data[2]))
					others.append(filename)
					update_sql = f"UPDATE roms SET others = '{json.dumps(others)}' WHERE id = %d" % (data[0])
					db_job_latest(update_sql)
		else:
			print(filename)
	else:
		insdate = stringify(date.today().strftime("%Y-%m-%d"))
		release_date = stringify(date.today().strftime("%Y-%m-%d"))
		if filetype == "fastboot":
			public_date = stringify(get_time(form_url(filename,version)))
			ins_sql = f"INSERT INTO roms (zone,device,code,android,version,type,bigver,region,tag,branch,{checkpoint},release_date,insdate, public_date) VALUES (%d,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" % (zone, stringify(device), stringify(code), stringify(android), stringify(version), stringify(type), stringify(bigver), stringify(region), stringify(tag), stringify(branch), stringify(filename), release_date, insdate, public_date)
		else:
			beta_date = stringify(get_time(form_url(filename,version)))
			public_date = stringify(None)
			ins_sql = f"INSERT INTO roms (zone,device,code,android,version,type,bigver,region,tag,branch,{checkpoint},release_date,beta_date,insdate) VALUES (%d,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" % (zone, stringify(device), stringify(code), stringify(android), stringify(version), stringify(type), stringify(bigver), stringify(region), stringify(tag), stringify(branch), stringify(filename), release_date, beta_date, insdate)
		db_job_latest(ins_sql)



def checkOSExist(filename):
	if platform == "win32":
		OSPath = 'D:/Projects/HyperOS.fans/Web/public/data/devices/'
		OSnewROM = open("D:/Projects/HyperOS.fans/Web/public/data/scripts/NewROMs.txt", 'r', encoding='utf-8').read()
		newROM = open("public/MRData/scripts/NewROMs.txt", 'r', encoding='utf-8').read()
	elif platform == "darwin":
		OSPath = '../HyperOS.fans/public/data/devices/'
		OSnewROM = open("../HyperOS.fans/public/data/scripts/NewROMs.txt", 'r', encoding='utf-8').read()
		newROM = open("public/MRData/scripts/NewROMs.txt", 'r', encoding='utf-8').read()
	else:
		OSPath = '/sdcard/Codes/NuxtMR/public/MRdata/data/devices/'
		OSnewROM = open("/sdcard/Codes/NuxtMR/public/MRdata/scripts/NewROMs.txt", 'r', encoding='utf-8').read()
		newROM = open("/sdcard/Codes/NuxtMR/public/MRdata/scripts/NewROMs.txt", 'r', encoding='utf-8').read()
	if "zip" in filename:
		if "miui" in filename:
			rec_seperator = "_"
			rec_spot = 1
		else:
			rec_seperator = "-ota_full"
			rec_spot = 0
		flag = filename.split(rec_seperator)[rec_spot]
	if "tgz" in filename:
		if "-images" in filename:
			flag = filename.split('-images')[0]
		else:
			flag = filename.split('_images')[0]
	if "PISSARROINFKGlobal" in filename:
		devdata = devdata = json.loads(open(OSPath+'pissarro_in.json', 'r', encoding='utf-8').read())
	else:
		devdata = json.loads(open(OSPath+flags[flag]+'.json', 'r', encoding='utf-8').read())
	if filename in str(devdata) or filename in OSnewROM or filename in newROM:
		i = 0
	else:
		device, code, android, version, type, bigver, region,tag,zone, branch, filetype, filename = [item for item in getData(filename)]
		checkDatabase(device, code, android, version, type, bigver, region,tag,zone, branch, filetype, filename)
		writeData(filename)


miui_key = b'miuiotavalided11'
miui_iv = b'0102030405060708'
check_url = 'https://update.miui.com/updates/miotaV3.php'


def miui_decrypt(encrypted_response):
	decipher = AES.new(miui_key, AES.MODE_CBC, miui_iv)
	decrypted = decipher.decrypt(base64.b64decode(encrypted_response))
	plaintext = decrypted.decode('utf-8').strip()
	pos = plaintext.rfind('}')
	if pos != -1:
		return json.loads(plaintext[:pos + 1])
	else:
		return json.loads(plaintext)


def miui_encrypt(json_request):
	cipher = AES.new(miui_key, AES.MODE_CBC, miui_iv)
	cipher_text = cipher.encrypt(
		pad(bytes(str(json_request), encoding='ascii'), AES.block_size))
	encrypted_request = urllib.parse.quote(base64.b64encode(
		cipher_text).decode('utf-8')).replace('/', '%2F')
	return encrypted_request


def MiFirm(url):
	options = Options()
	driver = webdriver.Edge(options=options)
	driver.get(url)
	soup = BeautifulSoup(driver.page_source, 'lxml')
	td_tags = soup.find_all('td')
	filtered_td_tags = [
		td for td in td_tags if 'zip' in td.text or 'tgz' in td.text]
	for tag in filtered_td_tags:
		checkExist(tag.text)


def MiFirm2(url):
	response = requests.post(url)
	if (response.status_code == 200):
		content = response.content.decode("utf8")
		if content == "":
			i = 0
		else:
			soup = BeautifulSoup(content, 'lxml')
			table_tags = soup.find_all("table", class_="firm_data")
			for tag in table_tags:
				tdtags = BeautifulSoup(str(tag), 'lxml')
				tds = tdtags.find_all("td")
				for td in tds:
					if ".tgz" in td.text or ".zip" in td.text:
						checkExist(td.text)
					else:
						i = 0


MiOTAForm = {
	'a': '0',
	'b': 'X',
	'c': '14',
	'unlock': '0',
	'd': 'fuxi',
	'lockZoneChannel': '',
	'f': '1',
	'g': 'a3e178346e97182fa11631a197801c4d',
	'channel': '',
	'i': '4178f5336815cc2a4641611c1619834817ab14bd0b4c7396a55be2f172c95a56',
	'i2': 'b92243889a47bc62dc8b5fb4f50ce60c373553e4221d3ebc4b3bd9791ccaa0a7',
	'isR': '0',
	'l': 'zh_CN',
	'sys': '0',
	'n': '',
	'p': 'fuxi',
	'r': 'CN',
	'bv': '14',
	'v': 'MIUI-V14.0.23.9.12.DEV',
	'id': '',
	'sn': '0x77309938',
	'sdk': '29',
	'pn': 'fuxi',
	'options': {'zone': 1, 'hashId': '2371ef99a72a282c', 'ab': '0', 'previewPlan': '0', 'sv': 3, 'av': '8.3.1', 'cv': 'V14.0.23.9.12.DEV'}}

MiOTAForm2 = {
	'a': '0',
	'b': 'F',
	'c': '10',
	'unlock': '0',
	'd': 'cepheus_eea_or_global',
	'f': '1',
	'g': 'a3e178346e97182fa11631a197801c4d',
	'channel': '',
	'isR': '0',
	'l': 'zh_CN',
	'sys': '0',
	'n': '',
	'r': 'CN',
	'bv': '14',
	'v': 'MIUI-V12.0.6.0.QFAEUOR',
	'id': '',
	'sn': '0x77309938',
	'sdk': '33',
	'pn': 'cepheus_eea',
	'options': {'zone': 2, 'hashId': '2371ef99a72a282c', 'ab': '0', 'previewPlan': '0'}}


def OTAFormer(device, code, region, branch, zone, android, version):
	MiOTAForm2['d'] = code
	if region == 'cn':
		MiOTAForm2['pn'] = code
	else:
		if code == device + "_global":
			MiOTAForm2['pn'] = code
		else:
			MiOTAForm2['pn'] = code.split('_global')[0]
	MiOTAForm2['b'] = branch
	MiOTAForm2['options']['zone'] = zone
	if android == '':
		print(device, version, "请补充安卓版本")
		MiOTAForm2['c'] = '14'
	else:
		MiOTAForm2['c'] = android.split('.0')[0]
	MiOTAForm2['sdk'] = sdk[android.split('.0')[0]]
	MiOTAForm2['v'] = 'MIUI-' + version
	# print(version)
	return json.dumps(MiOTAForm2)


def versionAdd(version, add):
	parts = [version.split('.')[0],version.split('.')[1],str(int(version.split('.')[2])+add),"0",version.split('.')[4]]
	separator = "."
	return separator.join(parts)


def getFromApi(encrypted_data, device):
	headers = {'user-agent': 'Dalvik/2.1.0 (Linux; U; Android 13; MI 9 Build/TKQ1.220829.002)',
				 'Connection': 'Keep-Alive',
				 'Content-Type': 'application/x-www-form-urlencoded',
				 'Cache-Control': 'no-cache',
				 'Host': 'update.miui.com',
				 'Accept-Encoding': 'gzip',
				 'Content-Length': '795',
				 'Cookie': 'serviceToken=;'
				 }
	data = 'q=' + encrypted_data + '&s=1&t='
	devdata = json.loads(open('public/MRdata/data/devices/' +
						 device+'.json', 'r', encoding='utf-8').read())
	session = requests.Session()
	retries = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
	session.mount('http://', HTTPAdapter(max_retries=retries))
	session.mount('https://', HTTPAdapter(max_retries=retries))
	try:
		response = session.post(check_url, headers=headers, data=data, timeout=10)
		print('\r', datetime.now().strftime("%Y-%m-%d %H:%M:%S"), '\t正在抓取' +
				devdata['zh-cn']+'(' + devdata['codename']+')					', end='')
		if response.status_code != 200:
			i = 0
		else:
			resdata = miui_decrypt(response.text.split('q=')[0])
			if 'LatestRom' in resdata:
				package = resdata['LatestRom']['filename'].split('?')[0]
				# print(package)
				checkExist(package)
				return 1
			if 'CrossRom' in resdata:
				package = resdata['CrossRom']['filename'].split('?')[0]
				# print(package)
				checkExist(package)
				return 1
			else:
				return 0
		response.close()
	except requests.exceptions.RequestException as e:
		print(f"请求失败: {e}")


def getFromApi2(encrypted_data, device):
	headers = {'user-agent': 'Dalvik/2.1.0 (Linux; U; Android 13; MI 9 Build/TKQ1.220829.002)',
				 'Connection': 'Keep-Alive',
				 'Content-Type': 'application/x-www-form-urlencoded',
				 'Cache-Control': 'no-cache',
				 'Host': 'update.miui.com',
				 'Accept-Encoding': 'gzip',
				 'Content-Length': '795',
				 'Cookie': 'serviceToken=;'
				 }
	data = 'q=' + encrypted_data + '&s=1&t='
	response = requests.post(check_url, headers=headers, data=data)
	if response.status_code != 200:
		print(json.loads(response.text))
	else:
		data = miui_decrypt(response.text.split('q=')[0])
		print(data)
		if 'LatestRom' in data:
			package = data['LatestRom']['filename'].split('?')[0]
			checkExist(package)
			return 1
		elif 'CrossRom' in data:
			package = data['CrossRom']['filename'].split('?')[0]
			checkExist(package)
			return 1
		else:
			return 0
	response.close()


def getChangelog(encrypted_data, device):
	headers = {'user-agent': 'Dalvik/2.1.0 (Linux; U; Android 13; MI 9 Build/TKQ1.220829.002)',
				 'Connection': 'Keep-Alive',
				 'Content-Type': 'application/x-www-form-urlencoded',
				 'Cache-Control': 'no-cache',
				 'Host': 'update.miui.com',
				 'Accept-Encoding': 'gzip',
				 'Content-Length': '795',
				 'Cookie': 'serviceToken=;'
				 }
	data = 'q=' + encrypted_data + '&s=1&t='
	if platform == 'win32':
		devdata = json.loads(
			open('public/MRdata/data/devices/'+device+'.json', 'r', encoding='utf-8').read())
	else:
		devdata = json.loads(open(
			'/sdcard/Codes/NuxtMR/public/MRdata/data/devices/'+device+'.json', 'r', encoding='utf-8').read())
	response = requests.post(check_url, headers=headers, data=data)
	if response.status_code != 200:
		i = 0
	else:
		data = miui_decrypt(response.text.split('q=')[0])
		if 'LatestRom' in data:
			print("最新版本更新日志：")
			print_log(data["LatestRom"]["changelog"])
		if 'CurrentRom' in data:
			print("\n当前版本更新日志：")
			print_log(data["CurrentRom"]["changelog"])
		else:
			print(data)
			return 0
	response.close()


def print_log(log):
	for module in log:
		print(module)
		for entry in log[module]['txt']:
			print(entry)
