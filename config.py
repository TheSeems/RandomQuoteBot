import os

raw_wall_token = os.getenv("RQ_WT")
raw_bot_token = os.getenv("RQ_BT")
group_id = os.getenv("RQ_GID")

welcome_template = """
    {}, здравствуйте!
    Я могу выдавать рандомные цитатки из этого паблика.
    
    Просто напишите: 'рандом'
    Также, мы поддерживаем выдачу рандомных постов по хештегам, например, 'рандом #danger'
    (без кавычек)
    
    По общим вопросам пишите в телеграм: @splendee (https://t.me/splendee)
    По вопросам, связанным именно с ботом: @theseems (https://t.me/theseems)
"""

selection_types = {
    'all': 'Все посты',
    'custom': "{}"
}
post_template = """
    Ссылка на пост: {}
    Выборка: {}
    
    {}
"""
no_posts_template = """
    К сожалению, постов по вашему запросу не найдено.
"""
