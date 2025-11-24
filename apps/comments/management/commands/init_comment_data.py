from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from apps.comments.models import Comment
from apps.users.models import CustomUser
from apps.scenic.models import ScenicSpot
from apps.routes.models import Route
from apps.hotels.models import Hotel
from apps.news.models import News
import random


class Command(BaseCommand):
    help = '初始化示例评论数据'

    def handle(self, *args, **options):
        self.stdout.write('开始创建示例评论数据...')
        
        # 获取或创建测试用户
        users = CustomUser.objects.all()
        if not users.exists():
            self.stdout.write(self.style.ERROR('请先创建用户数据！'))
            return
        
        # 获取各种对象
        scenic_spots = ScenicSpot.objects.all()
        routes = Route.objects.all()
        hotels = Hotel.objects.all()
        news_list = News.objects.all()
        
        comments_data = []
        
        # 景点评论
        for spot in scenic_spots[:5]:
            for i in range(random.randint(3, 8)):
                user = random.choice(users)
                comments_data.append({
                    'user': user,
                    'target_id': spot.id,
                    'target_type': 'scenic',
                    'content': random.choice([
                        f'{spot.name}真的很不错，景色优美，值得一游！',
                        f'去{spot.name}玩了一天，感觉非常好，下次还会再来。',
                        f'{spot.name}的历史文化底蕴深厚，导游讲解很详细，学到了很多知识。',
                        f'{spot.name}的环境很好，适合带家人一起来玩。',
                        f'在{spot.name}拍了很多照片，风景太美了！',
                        f'{spot.name}的门票价格合理，性价比很高。',
                        f'{spot.name}的交通很方便，停车也很方便。',
                    ]),
                    'rating': random.choice([4, 5, 5, 5, 5]),  # 偏向高分
                    'created_at': timezone.now() - timedelta(days=random.randint(1, 30)),
                })
        
        # 路线评论
        for route in routes[:3]:
            for i in range(random.randint(2, 6)):
                user = random.choice(users)
                comments_data.append({
                    'user': user,
                    'target_id': route.id,
                    'target_type': 'route',
                    'content': random.choice([
                        f'{route.name}的行程安排很合理，导游服务也很好。',
                        f'参加了{route.name}，玩得很开心，物超所值！',
                        f'{route.name}的景点选择很棒，每个地方都值得一看。',
                        f'{route.name}的住宿和餐饮都很好，整体体验不错。',
                        f'推荐{route.name}，适合第一次来保定的朋友。',
                    ]),
                    'rating': random.choice([4, 5, 5, 5]),
                    'created_at': timezone.now() - timedelta(days=random.randint(1, 20)),
                })
        
        # 酒店评论
        for hotel in hotels[:4]:
            for i in range(random.randint(2, 7)):
                user = random.choice(users)
                comments_data.append({
                    'user': user,
                    'target_id': hotel.id,
                    'target_type': 'hotel',
                    'content': random.choice([
                        f'{hotel.name}的设施很完善，服务也很周到，住得很舒服。',
                        f'在{hotel.name}住了两晚，房间干净整洁，早餐也很丰富。',
                        f'{hotel.name}的位置很好，交通便利，周边设施齐全。',
                        f'{hotel.name}的价格合理，性价比很高，推荐！',
                        f'{hotel.name}的环境很好，房间宽敞明亮，很满意。',
                        f'{hotel.name}的前台服务很热情，入住体验很好。',
                    ]),
                    'rating': random.choice([4, 4, 5, 5, 5]),
                    'created_at': timezone.now() - timedelta(days=random.randint(1, 25)),
                })
        
        # 资讯评论
        for news in news_list[:4]:
            for i in range(random.randint(1, 5)):
                user = random.choice(users)
                comments_data.append({
                    'user': user,
                    'target_id': news.id,
                    'target_type': 'news',
                    'content': random.choice([
                        f'这篇关于{news.title}的文章很有用，学到了很多。',
                        f'{news.title}的内容很详细，对计划旅行很有帮助。',
                        f'感谢分享{news.title}，信息很实用。',
                        f'{news.title}写得很好，期待更多这样的文章。',
                    ]),
                    'rating': random.choice([4, 5, 5]),
                    'created_at': timezone.now() - timedelta(days=random.randint(1, 15)),
                })
        
        # 创建评论
        created_count = 0
        for comment_data in comments_data:
            comment, created = Comment.objects.get_or_create(
                user=comment_data['user'],
                target_id=comment_data['target_id'],
                target_type=comment_data['target_type'],
                defaults={
                    'content': comment_data['content'],
                    'rating': comment_data['rating'],
                    'created_at': comment_data['created_at'],
                }
            )
            if created:
                created_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'\n成功创建 {created_count} 条评论！'))

