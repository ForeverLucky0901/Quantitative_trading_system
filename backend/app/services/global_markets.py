"""
全球股票市场数据 - 热门股票列表
"""

# 全球主要股票市场的热门股票
GLOBAL_POPULAR_STOCKS = {
    # ========== 亚洲市场 ==========
    
    # 日本 🇯🇵
    'JP': {
        'name': '日本',
        'exchange': '东京证券交易所（TSE）',
        'index': '^N225',  # 日经225指数
        'stocks': {
            '7203.T': '丰田汽车',
            '9984.T': '软银集团',
            '6758.T': '索尼',
            '7974.T': '任天堂',
            '6861.T': '基恩士',
            '9433.T': 'KDDI',
            '8306.T': '三菱日联金融',
            '6098.T': '瑞可利',
            '4063.T': '信越化学',
            '6954.T': 'FANUC',
        }
    },
    
    # 韩国 🇰🇷
    'KS': {
        'name': '韩国',
        'exchange': '韩国交易所（KRX）',
        'index': '^KS11',  # KOSPI指数
        'stocks': {
            '005930.KS': '三星电子',
            '000660.KS': 'SK海力士',
            '035420.KS': 'NAVER',
            '035720.KS': '卡卡奥',
            '051910.KS': 'LG化学',
            '005380.KS': '现代汽车',
            '068270.KS': 'Celltrion',
            '006400.KS': '三星SDI',
            '028260.KS': '三星物产',
            '207940.KS': '三星生物',
        }
    },
    
    # 印度 🇮🇳
    'IN': {
        'name': '印度',
        'exchange': '国家证券交易所（NSE）',
        'index': '^NSEI',  # NIFTY 50
        'stocks': {
            'RELIANCE.NS': '信实工业',
            'TCS.NS': '塔塔咨询服务',
            'HDFCBANK.NS': 'HDFC银行',
            'INFY.NS': 'Infosys',
            'HINDUNILVR.NS': '印度斯坦联合利华',
            'ICICIBANK.NS': 'ICICI银行',
            'BHARTIARTL.NS': 'Bharti Airtel',
            'ITC.NS': 'ITC有限公司',
            'KOTAKBANK.NS': 'Kotak Mahindra银行',
            'LT.NS': 'Larsen & Toubro',
        }
    },
    
    # 台湾 🇹🇼
    'TW': {
        'name': '台湾',
        'exchange': '台湾证券交易所（TWSE）',
        'index': '^TWII',  # 台湾加权指数
        'stocks': {
            '2330.TW': '台积电',
            '2317.TW': '鸿海精密',
            '2454.TW': '联发科',
            '2412.TW': '中华电信',
            '1301.TW': '台塑',
            '2882.TW': '国泰金控',
            '2308.TW': '台达电',
            '2891.TW': '中信金',
            '1303.TW': '南亚',
            '3008.TW': '大立光',
        }
    },
    
    # 泰国 🇹🇭
    'TH': {
        'name': '泰国',
        'exchange': '泰国证券交易所（SET）',
        'index': '^SET.BK',
        'stocks': {
            'PTT.BK': 'PTT公共有限公司',
            'CPALL.BK': 'CP ALL',
            'AOT.BK': '泰国机场',
            'ADVANC.BK': 'Advanced Info Service',
            'SCB.BK': '暹罗商业银行',
        }
    },
    
    # ========== 欧洲市场 ==========
    
    # 英国 🇬🇧
    'UK': {
        'name': '英国',
        'exchange': '伦敦证券交易所（LSE）',
        'index': '^FTSE',  # 富时100指数
        'stocks': {
            'HSBA.L': '汇丰控股',
            'BP.L': 'BP石油',
            'SHEL.L': '壳牌',
            'AZN.L': '阿斯利康',
            'ULVR.L': '联合利华',
            'DGE.L': '帝亚吉欧',
            'GSK.L': '葛兰素史克',
            'RIO.L': '力拓',
            'LSEG.L': '伦敦证券交易所集团',
            'BARC.L': '巴克莱银行',
        }
    },
    
    # 德国 🇩🇪
    'DE': {
        'name': '德国',
        'exchange': '法兰克福证券交易所',
        'index': '^GDAXI',  # DAX指数
        'stocks': {
            'VOW3.DE': '大众汽车',
            'SAP.DE': 'SAP',
            'SIE.DE': '西门子',
            'ALV.DE': '安联保险',
            'BAS.DE': '巴斯夫',
            'DAI.DE': '戴姆勒',
            'BMW.DE': '宝马',
            'DTE.DE': '德国电信',
            'MUV2.DE': '慕尼黑再保险',
            'ADS.DE': '阿迪达斯',
        }
    },
    
    # 法国 🇫🇷
    'FR': {
        'name': '法国',
        'exchange': '巴黎证券交易所',
        'index': '^FCHI',  # CAC 40指数
        'stocks': {
            'MC.PA': 'LVMH',
            'OR.PA': '欧莱雅',
            'SAN.PA': '赛诺菲',
            'TTE.PA': '道达尔能源',
            'AIR.PA': '空中客车',
            'BNP.PA': '法国巴黎银行',
            'SU.PA': '施耐德电气',
            'DSY.PA': '达索系统',
            'RMS.PA': '爱马仕',
            'AI.PA': 'Air Liquide',
        }
    },
    
    # 瑞士 🇨🇭
    'CH': {
        'name': '瑞士',
        'exchange': '瑞士证券交易所',
        'index': '^SSMI',  # 瑞士市场指数
        'stocks': {
            'NESN.SW': '雀巢',
            'ROG.SW': '罗氏',
            'NOVN.SW': '诺华',
            'UBSG.SW': '瑞银集团',
            'ZURN.SW': '苏黎世保险',
            'ABBN.SW': 'ABB',
            'GIVN.SW': 'Givaudan',
            'SREN.SW': 'Swiss Re',
            'LONN.SW': 'Lonza',
            'CSGN.SW': '瑞士信贷',
        }
    },
    
    # 荷兰 🇳🇱
    'NL': {
        'name': '荷兰',
        'exchange': '阿姆斯特丹证券交易所',
        'index': '^AEX',
        'stocks': {
            'ASML.AS': 'ASML',
            'PHIA.AS': '飞利浦',
            'HEIA.AS': '喜力',
            'INGA.AS': 'ING集团',
            'SHELL.AS': '壳牌',
        }
    },
    
    # ========== 美洲市场 ==========
    
    # 加拿大 🇨🇦
    'CA': {
        'name': '加拿大',
        'exchange': '多伦多证券交易所（TSX）',
        'index': '^GSPTSE',  # S&P/TSX综合指数
        'stocks': {
            'SHOP.TO': 'Shopify',
            'RY.TO': '加拿大皇家银行',
            'TD.TO': '道明银行',
            'ENB.TO': 'Enbridge',
            'CNQ.TO': 'Canadian Natural Resources',
            'BNS.TO': '丰业银行',
            'BMO.TO': '蒙特利尔银行',
            'CP.TO': '加拿大太平洋铁路',
            'CNR.TO': '加拿大国家铁路',
            'SU.TO': 'Suncor Energy',
        }
    },
    
    # 巴西 🇧🇷
    'BR': {
        'name': '巴西',
        'exchange': '圣保罗证券交易所（B3）',
        'index': '^BVSP',  # Bovespa指数
        'stocks': {
            'PETR4.SA': '巴西石油',
            'VALE3.SA': '淡水河谷',
            'ITUB4.SA': '伊塔乌联合银行',
            'BBDC4.SA': 'Bradesco银行',
            'ABEV3.SA': 'Ambev',
            'B3SA3.SA': 'B3交易所',
            'WEGE3.SA': 'WEG',
            'RENT3.SA': 'Localiza',
            'SUZB3.SA': 'Suzano',
            'MGLU3.SA': 'Magazine Luiza',
        }
    },
    
    # 墨西哥 🇲🇽
    'MX': {
        'name': '墨西哥',
        'exchange': '墨西哥证券交易所',
        'index': '^MXX',
        'stocks': {
            'AMXL.MX': '美洲电信',
            'WALMEX.MX': '沃尔玛墨西哥',
            'GFNORTEO.MX': 'Banorte',
            'CEMEXCPO.MX': 'Cemex',
            'FEMSAUBD.MX': 'Femsa',
        }
    },
    
    # ========== 大洋洲市场 ==========
    
    # 澳大利亚 🇦🇺
    'AU': {
        'name': '澳大利亚',
        'exchange': '澳大利亚证券交易所（ASX）',
        'index': '^AXJO',  # S&P/ASX 200
        'stocks': {
            'BHP.AX': '必和必拓',
            'CBA.AX': '澳洲联邦银行',
            'CSL.AX': 'CSL',
            'NAB.AX': '澳洲国民银行',
            'WBC.AX': '西太平洋银行',
            'ANZ.AX': '澳新银行',
            'WES.AX': 'Wesfarmers',
            'MQG.AX': '麦格理集团',
            'WOW.AX': 'Woolworths',
            'RIO.AX': '力拓',
        }
    },
    
    # 新西兰 🇳🇿
    'NZ': {
        'name': '新西兰',
        'exchange': '新西兰证券交易所（NZX）',
        'index': '^NZ50',
        'stocks': {
            'FPH.NZ': 'Fisher & Paykel Healthcare',
            'AIR.NZ': '新西兰航空',
            'SPK.NZ': 'Spark New Zealand',
            'MCY.NZ': 'Mercury NZ',
            'FBU.NZ': 'Fletcher Building',
        }
    },
    
    # ========== 中东市场 ==========
    
    # 沙特 🇸🇦
    'SA': {
        'name': '沙特阿拉伯',
        'exchange': 'Tadawul',
        'index': '^TASI',
        'stocks': {
            '2222.SAU': '沙特阿美',
            '1180.SAU': 'SABIC',
            '1120.SAU': 'Al Rajhi Bank',
            '2010.SAU': 'Saudi Basic Industries',
        }
    },
    
    # ========== 非洲市场 ==========
    
    # 南非 🇿🇦
    'ZA': {
        'name': '南非',
        'exchange': '约翰内斯堡证券交易所（JSE）',
        'index': '^JN0U.JO',
        'stocks': {
            'NPN.JO': 'Naspers',
            'PRX.JO': 'Prosus',
            'AGL.JO': 'Anglo American',
            'SHP.JO': 'Shoprite',
            'MTN.JO': 'MTN Group',
        }
    },
}

# 按地区分组
MARKETS_BY_REGION = {
    '亚洲': ['JP', 'KS', 'IN', 'TW', 'TH', 'MY', 'ID', 'PH', 'VN', 'HK', 'CN', 'SZ', 'SG'],
    '欧洲': ['UK', 'DE', 'FR', 'CH', 'NL', 'IT', 'ES', 'SE', 'NO', 'DK', 'FI', 'BE', 'AT', 'IE', 'PT', 'GR', 'RU'],
    '美洲': ['US', 'CA', 'BR', 'MX', 'AR', 'CL'],
    '大洋洲': ['AU', 'NZ'],
    '中东': ['SA', 'AE', 'IL', 'TR'],
    '非洲': ['ZA', 'EG'],
}

# 主要指数列表
MAJOR_INDICES = {
    # 美国
    '^GSPC': 'S&P 500',
    '^DJI': '道琼斯工业平均指数',
    '^IXIC': '纳斯达克综合指数',
    '^RUT': '罗素2000指数',
    
    # 亚洲
    '^HSI': '恒生指数',
    '^N225': '日经225指数',
    '^KS11': 'KOSPI指数',
    '^NSEI': 'NIFTY 50',
    '^TWII': '台湾加权指数',
    '^STI': '海峡时报指数',
    '000001.SS': '上证指数',
    '399001.SZ': '深证成指',
    
    # 欧洲
    '^FTSE': '富时100指数',
    '^GDAXI': 'DAX指数',
    '^FCHI': 'CAC 40指数',
    '^SSMI': '瑞士市场指数',
    '^AEX': 'AEX指数',
    '^IBEX': 'IBEX 35指数',
    '^FTMIB': '富时MIB指数',
    
    # 美洲
    '^GSPTSE': 'S&P/TSX综合指数',
    '^BVSP': 'Bovespa指数',
    '^MXX': 'IPC指数',
    
    # 大洋洲
    '^AXJO': 'S&P/ASX 200',
    '^NZ50': 'NZX 50指数',
}
