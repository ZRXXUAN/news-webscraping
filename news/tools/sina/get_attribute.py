SPORTS = 2512
ENTERTAINMENT = 2513
TECHNOLOGY = 2515
FINANCE = 2516
NEWS = 2974
ATTRIBUTE_DICT = {
    SPORTS: "体育", ENTERTAINMENT: "娱乐", TECHNOLOGY: "科技", FINANCE: "财经", NEWS: "新闻",
}


def get_attribute(lid):  # lid就是属性
    attribute = ATTRIBUTE_DICT.get(lid)
    return attribute
