# 主视觉图标库：viewBox 0 0 100 100，三种颜色由主视觉区底色决定
# {M} 主色（蓝底时为白色）、{A} 强调色（蓝底时为信号黄）、{B} 主视觉区底色（用来在主色上挖出细节）

ICONS = {
    "image": ("图片、照片、生图、设计", """
<circle cx="72" cy="28" r="10" fill="{A}"/>
<path d="M14 82 L40 44 L56 64 L65 54 L86 82 Z" fill="{M}" stroke="{M}" stroke-width="8" stroke-linejoin="round"/>"""),
    "clock": ("时间、截止、到期、倒计时", """
<path d="M20 24 L31 15 M80 24 L69 15" stroke="{A}" stroke-width="9" stroke-linecap="round"/>
<circle cx="50" cy="55" r="31" fill="{M}"/>
<path d="M50 38 V55 L62 63" fill="none" stroke="{B}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>"""),
    "chat": ("对话、聊天、AI 助手、评论", """
<rect x="12" y="18" width="70" height="50" rx="16" fill="{M}"/>
<path d="M28 64 L24 86 L48 66 Z" fill="{M}" stroke="{M}" stroke-width="4" stroke-linejoin="round"/>
<circle cx="33" cy="43" r="6" fill="{B}"/><circle cx="47" cy="43" r="6" fill="{B}"/><circle cx="61" cy="43" r="6" fill="{A}"/>"""),
    "bolt": ("快、效率、新功能、更新", """
<path d="M58 8 L22 56 H47 L40 92 L80 40 H55 Z" fill="{A}" stroke="{A}" stroke-width="6" stroke-linejoin="round"/>"""),
    "chart": ("数据、增长、对比、排行", """
<rect x="16" y="56" width="16" height="28" rx="4" fill="{M}"/>
<rect x="42" y="42" width="16" height="42" rx="4" fill="{M}"/>
<rect x="68" y="28" width="16" height="56" rx="4" fill="{M}"/>
<path d="M14 40 L36 24 L52 32 L82 12" fill="none" stroke="{A}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M68 11 H84 V27" fill="none" stroke="{A}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>"""),
    "gift": ("福利、免费、活动、优惠", """
<path d="M50 32 C42 12 22 18 34 32 Z M50 32 C58 12 78 18 66 32 Z" fill="{A}" stroke="{A}" stroke-width="5" stroke-linejoin="round"/>
<rect x="14" y="32" width="72" height="16" rx="5" fill="{M}"/>
<rect x="20" y="50" width="60" height="34" rx="5" fill="{M}"/>
<rect x="45" y="32" width="10" height="52" fill="{A}"/>"""),
    "book": ("学习、教程、阅读、知识", """
<path d="M50 28 C38 19 24 19 12 23 V80 C24 76 38 76 50 84 Z" fill="{M}"/>
<path d="M50 28 C62 19 76 19 88 23 V80 C76 76 62 76 50 84 Z" fill="{M}"/>
<path d="M50 30 V82" stroke="{B}" stroke-width="4"/>
<path d="M66 18 H76 V40 L71 35 L66 40 Z" fill="{A}"/>"""),
    "camera": ("拍照、摄影、相机、视觉", """
<rect x="34" y="20" width="28" height="14" rx="4" fill="{M}"/>
<rect x="12" y="30" width="76" height="54" rx="12" fill="{M}"/>
<circle cx="50" cy="57" r="17" fill="{B}"/><circle cx="50" cy="57" r="9" fill="{A}"/>"""),
    "video": ("视频、剪辑、播放、直播", """
<rect x="10" y="20" width="80" height="54" rx="12" fill="{M}"/>
<path d="M43 35 L43 59 L62 47 Z" fill="{B}" stroke="{B}" stroke-width="5" stroke-linejoin="round"/>
<rect x="32" y="80" width="36" height="8" rx="4" fill="{A}"/>"""),
    "money": ("赚钱、价格、收入、省钱", """
<circle cx="50" cy="50" r="36" fill="{A}"/>
<path d="M37 30 L50 47 L63 30 M50 47 V72 M39 52 H61 M39 62 H61" fill="none" stroke="{B}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>"""),
    "checklist": ("清单、步骤、待办、攻略", """
<rect x="20" y="12" width="60" height="76" rx="10" fill="{M}"/>
<path d="M30 32 L35 37 L44 27 M30 52 L35 57 L44 47 M30 72 L35 77 L44 67" fill="none" stroke="{A}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>
<rect x="50" y="29" width="22" height="6" rx="3" fill="{B}"/><rect x="50" y="49" width="22" height="6" rx="3" fill="{B}"/><rect x="50" y="69" width="16" height="6" rx="3" fill="{B}"/>"""),
    "search": ("搜索、查找、测评、发现", """
<circle cx="43" cy="43" r="25" fill="none" stroke="{M}" stroke-width="11"/>
<path d="M62 62 L84 84" stroke="{M}" stroke-width="13" stroke-linecap="round"/>
<path d="M30 40 A14 14 0 0 1 42 29" fill="none" stroke="{A}" stroke-width="6" stroke-linecap="round"/>"""),
    "code": ("编程、开发、代码、工具", """
<path d="M34 28 L14 50 L34 72 M66 28 L86 50 L66 72" fill="none" stroke="{M}" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M57 20 L43 80" stroke="{A}" stroke-width="10" stroke-linecap="round"/>"""),
    "mic": ("配音、播客、录音、口播", """
<rect x="36" y="10" width="28" height="50" rx="14" fill="{M}"/>
<path d="M24 46 C24 76 76 76 76 46" fill="none" stroke="{M}" stroke-width="8" stroke-linecap="round"/>
<path d="M50 72 V86 M36 88 H64" stroke="{M}" stroke-width="8" stroke-linecap="round"/>
<rect x="44" y="22" width="12" height="5" rx="2.5" fill="{A}"/><rect x="44" y="33" width="12" height="5" rx="2.5" fill="{A}"/>"""),
    "star": ("推荐、精选、好评、收藏", """
<path d="M50 10 L61 36 L89 38 L67 56 L74 84 L50 69 L26 84 L33 56 L11 38 L39 36 Z" fill="{A}" stroke="{A}" stroke-width="6" stroke-linejoin="round"/>"""),
    "heart": ("喜欢、情感、健康、关怀", """
<path d="M50 84 C20 64 10 46 14 32 C18 16 40 12 50 30 C60 12 82 16 86 32 C90 46 80 64 50 84 Z" fill="{M}"/>
<path d="M27 36 C29 29 34 26 39 26" fill="none" stroke="{A}" stroke-width="6" stroke-linecap="round"/>"""),
    "calendar": ("日期、日程、活动时间、计划", """
<rect x="14" y="20" width="72" height="66" rx="12" fill="{M}"/>
<path d="M14 32 Q14 20 26 20 H74 Q86 20 86 32 V38 H14 Z" fill="{A}"/>
<path d="M32 12 V26 M68 12 V26" stroke="{M}" stroke-width="8" stroke-linecap="round"/>
<rect x="26" y="48" width="12" height="10" rx="3" fill="{B}"/><rect x="44" y="48" width="12" height="10" rx="3" fill="{B}"/><rect x="62" y="48" width="12" height="10" rx="3" fill="{A}"/>
<rect x="26" y="66" width="12" height="10" rx="3" fill="{B}"/><rect x="44" y="66" width="12" height="10" rx="3" fill="{B}"/>"""),
    "bulb": ("灵感、技巧、方法、点子", """
<path d="M50 4 V12 M18 18 L24 24 M82 18 L76 24 M8 48 H16 M84 48 H92" stroke="{A}" stroke-width="7" stroke-linecap="round"/>
<circle cx="50" cy="44" r="26" fill="{M}"/>
<rect x="38" y="62" width="24" height="16" rx="4" fill="{M}"/>
<rect x="41" y="82" width="18" height="8" rx="4" fill="{A}"/>"""),
    "phone": ("手机、App、小程序、移动端", """
<rect x="28" y="8" width="44" height="84" rx="12" fill="{M}"/>
<rect x="34" y="20" width="32" height="58" rx="5" fill="{B}"/>
<rect x="39" y="28" width="22" height="16" rx="3" fill="{A}"/>
<rect x="39" y="50" width="22" height="5" rx="2.5" fill="{M}"/><rect x="39" y="60" width="15" height="5" rx="2.5" fill="{M}"/>"""),
    "robot": ("AI、模型、智能体、机器人", """
<path d="M50 30 V18" stroke="{M}" stroke-width="7" stroke-linecap="round"/>
<circle cx="50" cy="14" r="7" fill="{A}"/>
<rect x="8" y="46" width="10" height="20" rx="4" fill="{A}"/><rect x="82" y="46" width="10" height="20" rx="4" fill="{A}"/>
<rect x="18" y="30" width="64" height="52" rx="16" fill="{M}"/>
<circle cx="37" cy="54" r="7" fill="{B}"/><circle cx="63" cy="54" r="7" fill="{B}"/>
<rect x="40" y="68" width="20" height="5" rx="2.5" fill="{B}"/>"""),
    "pet": ("宠物、猫、狗、萌宠", """
<path d="M18 46 L20 14 L42 32 Z M82 46 L80 14 L58 32 Z" fill="{M}" stroke="{M}" stroke-width="6" stroke-linejoin="round"/>
<ellipse cx="50" cy="56" rx="36" ry="30" fill="{M}"/>
<circle cx="37" cy="52" r="5" fill="{B}"/><circle cx="63" cy="52" r="5" fill="{B}"/>
<path d="M44 63 L56 63 L50 70 Z" fill="{A}" stroke="{A}" stroke-width="4" stroke-linejoin="round"/>
<path d="M8 58 H24 M8 68 H24 M76 58 H92 M76 68 H92" stroke="{A}" stroke-width="4" stroke-linecap="round"/>"""),
    "food": ("美食、做饭、外卖、探店", """
<path d="M70 8 L48 46 M84 14 L58 46" stroke="{A}" stroke-width="6" stroke-linecap="round"/>
<path d="M10 46 H90 C90 70 72 86 50 86 C28 86 10 70 10 46 Z" fill="{M}"/>
<rect x="32" y="86" width="36" height="6" rx="3" fill="{M}"/>
<path d="M24 56 C34 62 66 62 76 56" fill="none" stroke="{B}" stroke-width="4" stroke-linecap="round"/>"""),
    "travel": ("旅行、出行、机票、度假", """
<path d="M50 8 C56 8 58 16 58 24 V40 L88 58 V68 L58 58 V76 L68 84 V92 L50 86 L32 92 V84 L42 76 V58 L12 68 V58 L42 40 V24 C42 16 44 8 50 8 Z" fill="{M}" stroke="{M}" stroke-width="4" stroke-linejoin="round"/>
<circle cx="50" cy="30" r="5" fill="{A}"/>"""),
    "cart": ("购物、好物、电商、种草", """
<path d="M6 16 H18 L28 66 H78 L88 30 H24" fill="none" stroke="{M}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M27 30 H86 L78 60 H33 Z" fill="{M}"/>
<rect x="44" y="38" width="8" height="14" rx="3" fill="{B}"/><rect x="60" y="38" width="8" height="14" rx="3" fill="{B}"/>
<circle cx="34" cy="82" r="8" fill="{A}"/><circle cx="72" cy="82" r="8" fill="{A}"/>"""),
    "fitness": ("健身、运动、减脂、跑步", """
<rect x="6" y="34" width="14" height="32" rx="5" fill="{M}"/><rect x="80" y="34" width="14" height="32" rx="5" fill="{M}"/>
<rect x="18" y="24" width="14" height="52" rx="5" fill="{A}"/><rect x="68" y="24" width="14" height="52" rx="5" fill="{A}"/>
<rect x="30" y="44" width="40" height="12" rx="4" fill="{M}"/>"""),
    "shield": ("安全、防骗、隐私、保障", """
<path d="M50 8 L84 20 V46 C84 68 70 84 50 92 C30 84 16 68 16 46 V20 Z" fill="{M}"/>
<path d="M34 50 L46 62 L68 38" fill="none" stroke="{A}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>"""),
    "grad": ("学习、考试、教育、上岸", """
<path d="M50 14 L94 34 L50 54 L6 34 Z" fill="{M}" stroke="{M}" stroke-width="4" stroke-linejoin="round"/>
<path d="M24 44 V66 C24 76 76 76 76 66 V44 L50 56 Z" fill="{M}"/>
<path d="M88 36 V64" stroke="{A}" stroke-width="5" stroke-linecap="round"/>
<circle cx="88" cy="68" r="6" fill="{A}"/>"""),
    "house": ("家居、租房、装修、买房", """
<path d="M50 10 L92 46 H80 V88 H20 V46 H8 Z" fill="{M}" stroke="{M}" stroke-width="6" stroke-linejoin="round"/>
<rect x="40" y="58" width="20" height="30" rx="4" fill="{A}"/>
<rect x="66" y="16" width="10" height="18" rx="2" fill="{M}"/>"""),
    "trophy": ("成就、比赛、排名、获奖", """
<path d="M26 12 H74 V40 C74 56 62 64 50 64 C38 64 26 56 26 40 Z" fill="{A}"/>
<path d="M26 22 H12 C12 38 20 44 28 44 M74 22 H88 C88 38 80 44 72 44" fill="none" stroke="{A}" stroke-width="7" stroke-linecap="round"/>
<rect x="44" y="62" width="12" height="14" fill="{M}"/>
<rect x="28" y="76" width="44" height="12" rx="4" fill="{M}"/>
<path d="M50 24 L54 32 L62 33 L56 38 L58 46 L50 42 L42 46 L44 38 L38 33 L46 32 Z" fill="{B}"/>"""),
    "rocket": ("启动、创业、增长、起飞", """
<path d="M50 6 C66 18 72 38 68 62 H32 C28 38 34 18 50 6 Z" fill="{M}"/>
<circle cx="50" cy="34" r="9" fill="{B}"/>
<path d="M32 46 L16 64 L32 66 Z M68 46 L84 64 L68 66 Z" fill="{M}" stroke="{M}" stroke-width="4" stroke-linejoin="round"/>
<path d="M38 70 C38 80 44 88 50 94 C56 88 62 80 62 70 Z" fill="{A}"/>"""),
    "coffee": ("职场、日常、咖啡、打工", """
<path d="M38 8 C32 14 44 18 38 26 M56 8 C50 14 62 18 56 26" fill="none" stroke="{A}" stroke-width="5" stroke-linecap="round"/>
<path d="M12 34 H74 V60 C74 76 62 86 46 86 H40 C24 86 12 76 12 60 Z" fill="{M}"/>
<path d="M74 42 H80 C88 42 92 48 92 54 C92 62 86 66 78 66 H72" fill="none" stroke="{M}" stroke-width="8"/>
<rect x="22" y="44" width="42" height="6" rx="3" fill="{B}"/>"""),
    "pin": ("地点、本地、探店、城市", """
<path d="M50 92 C50 92 18 60 18 38 C18 20 32 8 50 8 C68 8 82 20 82 38 C82 60 50 92 50 92 Z" fill="{M}"/>
<circle cx="50" cy="38" r="13" fill="{A}"/>"""),
    "music": ("音乐、歌单、听歌、BGM", """
<path d="M40 70 V20 L84 10 V60" fill="none" stroke="{M}" stroke-width="9" stroke-linejoin="round"/>
<path d="M40 20 L84 10 V26 L40 36 Z" fill="{M}"/>
<ellipse cx="28" cy="72" rx="14" ry="11" fill="{A}"/><ellipse cx="72" cy="62" rx="14" ry="11" fill="{A}"/>"""),
    "game": ("游戏、娱乐、电竞、玩", """
<path d="M24 26 H76 C88 26 96 38 94 54 L90 74 C88 86 74 88 66 76 L60 66 H40 L34 76 C26 88 12 86 10 74 L6 54 C4 38 12 26 24 26 Z" fill="{M}"/>
<path d="M28 40 V56 M20 48 H36" stroke="{B}" stroke-width="6" stroke-linecap="round"/>
<circle cx="66" cy="44" r="5" fill="{A}"/><circle cx="76" cy="54" r="5" fill="{A}"/>"""),
    "doc": ("文档、报告、简历、合同", """
<path d="M20 8 H60 L82 30 V92 H20 Z" fill="{M}" stroke="{M}" stroke-width="4" stroke-linejoin="round"/>
<path d="M60 8 V30 H82 Z" fill="{A}" stroke="{A}" stroke-width="4" stroke-linejoin="round"/>
<rect x="32" y="46" width="38" height="6" rx="3" fill="{B}"/><rect x="32" y="60" width="38" height="6" rx="3" fill="{B}"/><rect x="32" y="74" width="24" height="6" rx="3" fill="{B}"/>"""),
    "mail": ("邮件、通知、私信、订阅", """
<rect x="8" y="20" width="84" height="60" rx="10" fill="{M}"/>
<path d="M12 26 L50 54 L88 26" fill="none" stroke="{B}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>
<circle cx="84" cy="22" r="12" fill="{A}"/>"""),
    "warning": ("避坑、风险、注意、提醒", """
<path d="M50 10 L92 86 H8 Z" fill="{A}" stroke="{A}" stroke-width="10" stroke-linejoin="round"/>
<rect x="45" y="36" width="10" height="28" rx="5" fill="{B}"/>
<circle cx="50" cy="74" r="6" fill="{B}"/>"""),
    "palette": ("设计、绘画、配色、创作", """
<path d="M50 8 C76 8 94 26 94 48 C94 62 84 66 74 64 C64 62 60 70 64 78 C68 86 62 92 50 92 C26 92 6 74 6 50 C6 26 24 8 50 8 Z" fill="{M}"/>
<circle cx="30" cy="40" r="7" fill="{A}"/><circle cx="48" cy="26" r="7" fill="{B}"/><circle cx="70" cy="32" r="7" fill="{A}"/><circle cx="28" cy="62" r="7" fill="{B}"/>"""),
    "plant": ("成长、习惯、养成、坚持", """
<path d="M50 88 V44" stroke="{M}" stroke-width="8" stroke-linecap="round"/>
<path d="M50 50 C50 30 36 18 14 18 C14 40 28 52 50 50 Z" fill="{A}"/>
<path d="M50 44 C50 22 64 10 86 10 C86 32 72 46 50 44 Z" fill="{M}"/>
<rect x="28" y="82" width="44" height="10" rx="5" fill="{M}"/>"""),
    "family": ("家庭、亲子、父母、人际", """
<circle cx="34" cy="26" r="13" fill="{M}"/><circle cx="68" cy="34" r="10" fill="{A}"/>
<path d="M12 84 C12 60 22 46 34 46 C46 46 56 60 56 84 Z" fill="{M}"/>
<path d="M50 84 C50 66 58 54 68 54 C78 54 88 66 88 84 Z" fill="{A}"/>"""),
    "briefcase": ("求职、工作、职场、面试", """
<path d="M36 26 V18 C36 14 38 12 42 12 H58 C62 12 64 14 64 18 V26" fill="none" stroke="{M}" stroke-width="8"/>
<rect x="8" y="26" width="84" height="60" rx="10" fill="{M}"/>
<rect x="8" y="48" width="84" height="6" fill="{B}"/>
<rect x="42" y="44" width="16" height="16" rx="3" fill="{A}"/>"""),
    "car": ("汽车、自驾、通勤、新能源", """
<path d="M22 44 L32 22 C34 18 38 16 42 16 H58 C62 16 66 18 68 22 L78 44" fill="none" stroke="{M}" stroke-width="8" stroke-linejoin="round"/>
<rect x="8" y="42" width="84" height="32" rx="10" fill="{M}"/>
<circle cx="26" cy="58" r="6" fill="{A}"/><circle cx="74" cy="58" r="6" fill="{A}"/>
<rect x="14" y="72" width="16" height="14" rx="4" fill="{M}"/><rect x="70" y="72" width="16" height="14" rx="4" fill="{M}"/>"""),
}

# 主视觉区底色 → 图标三色
PANEL_COLORS = {
    "blue": {"bg": "#315cff", "M": "#ffffff", "A": "#dfff45", "B": "#315cff"},
    "black": {"bg": "#141519", "M": "#ffffff", "A": "#dfff45", "B": "#141519"},
    "yellow": {"bg": "#dfff45", "M": "#141519", "A": "#315cff", "B": "#dfff45"},
    "paper": {"bg": "#ebe8de", "M": "#315cff", "A": "#141519", "B": "#ebe8de"},
}


def icon_svg(name, panel):
    c = PANEL_COLORS[panel]
    body = ICONS[name][1].replace("{M}", c["M"]).replace("{A}", c["A"]).replace("{B}", c["B"])
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100%" height="100%">{body}</svg>'
