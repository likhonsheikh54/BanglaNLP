NEWS_SOURCES = {
    'prothomalo': {
        'base_url': 'https://www.prothomalo.com',
        'article_selector': 'article.story-card',
        'link_selector': 'a.link-overlay',
        'list_urls': [
            '/international',
            '/sports',
            '/technology'
        ]
    },
    'ittefaq': {
        'base_url': 'https://www.ittefaq.com.bd',
        'article_selector': 'div.news-item',
        'link_selector': 'h3.title a',
        'list_urls': [
            '/international',
            '/sports-news',
            '/technology'
        ]
    },
    'banglatribune': {
        'base_url': 'https://www.banglatribune.com',
        'article_selector': 'div.article-box',
        'link_selector': 'h3.title a',
        'list_urls': [
            '/world',
            '/sports',
            '/technology'
        ]
    },
    'bdpratidin': {
        'base_url': 'https://www.bd-pratidin.com',
        'article_selector': 'div.all-news-content',
        'link_selector': 'h3.news-title a',
        'list_urls': [
            '/first-page',
            '/country',
            '/world',
            '/sports',
            '/entertainment',
            '/tech'
        ]
    },
    'janakantha': {
        'base_url': 'https://www.dailyjanakantha.com',
        'article_selector': 'div.news-card',
        'link_selector': 'h2.title a',
        'list_urls': [
            '/bangladesh',
            '/international',
            '/sports',
            '/tech',
            '/entertainment'
        ]
    },
    'jaijaidin': {
        'base_url': 'https://www.jaijaidinbd.com',
        'article_selector': 'div.news-box',
        'link_selector': '.news-title a',
        'list_urls': [
            '/national',
            '/international',
            '/sports',
            '/technology',
            '/entertainment'
        ]
    }
}

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
