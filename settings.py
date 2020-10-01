# -*- coding: utf-8 -*-
from util import TextStartsWithFilter

# A trigger to send user a random post.
random_post_trigger = TextStartsWithFilter("рандом")

# A trigger to welcome user.
welcome_trigger = TextStartsWithFilter("начать") | TextStartsWithFilter("/start")
