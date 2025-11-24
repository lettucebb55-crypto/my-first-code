from django import template

register = template.Library()


@register.filter
def stars(value):
    """将评分转换为星星显示"""
    try:
        rating = float(value)
        full_stars = int(rating)
        has_half = (rating - full_stars) >= 0.5
        return {
            'full': full_stars,
            'has_half': has_half,
            'empty': 5 - full_stars - (1 if has_half else 0),
            'rating': rating
        }
    except (ValueError, TypeError):
        return {
            'full': 0,
            'has_half': False,
            'empty': 5,
            'rating': 0
        }

