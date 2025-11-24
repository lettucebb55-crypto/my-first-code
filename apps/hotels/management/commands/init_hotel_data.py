from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.hotels.models import Hotel, RoomType
import random


class Command(BaseCommand):
    help = '初始化示例酒店数据'

    def handle(self, *args, **options):
        self.stdout.write('开始创建示例酒店数据...')
        
        # 酒店数据
        hotels_data = [
            {
                'name': '保定国际大酒店',
                'address': '河北省保定市竞秀区东风中路888号',
                'phone': '0312-8888888',
                'brief': '五星级豪华酒店，位于保定市中心，交通便利，设施完善。',
                'description': '''
                保定国际大酒店是一家五星级豪华酒店，位于保定市中心繁华地段，交通便利。
                酒店拥有各类豪华客房和套房，配备先进的设施设备，提供高品质的住宿体验。
                酒店内设有多家餐厅，提供中餐、西餐、日式料理等多种美食选择。
                此外，酒店还设有健身中心、游泳池、商务中心等配套设施，满足不同客人的需求。
                ''',
                'is_recommended': True,
                'rating': 4.8,
                'views_count': random.randint(500, 2000),
                'display_order': 1,
                'room_types': [
                    {'name': '标准间', 'price': 388.00, 'capacity': 2, 'remaining_count': 10, 'description': '温馨舒适的标准间，配备双床或大床，适合商务和休闲旅客。'},
                    {'name': '豪华间', 'price': 588.00, 'capacity': 2, 'remaining_count': 8, 'description': '宽敞明亮的豪华间，配备高品质家具和设施，提供更舒适的住宿体验。'},
                    {'name': '行政套房', 'price': 1288.00, 'capacity': 4, 'remaining_count': 3, 'description': '豪华行政套房，配备独立客厅和卧室，适合商务和家庭旅客。'},
                ]
            },
            {
                'name': '白洋淀度假酒店',
                'address': '河北省保定市安新县白洋淀景区内',
                'phone': '0312-6666666',
                'brief': '位于白洋淀景区内的度假酒店，环境优美，是休闲度假的理想选择。',
                'description': '''
                白洋淀度假酒店位于白洋淀景区内，环境优美，空气清新。
                酒店采用中式建筑风格，与周围自然景观完美融合。
                客房宽敞舒适，大部分房间可欣赏到湖景或园景。
                酒店提供丰富的娱乐设施，包括垂钓、游船、篝火晚会等活动。
                餐厅提供当地特色美食，让您品尝到正宗的保定风味。
                ''',
                'is_recommended': True,
                'rating': 4.6,
                'views_count': random.randint(400, 1500),
                'display_order': 2,
                'room_types': [
                    {'name': '湖景标准间', 'price': 288.00, 'capacity': 2, 'remaining_count': 15, 'description': '可欣赏白洋淀湖景的标准间，环境优美，价格实惠。'},
                    {'name': '湖景豪华间', 'price': 488.00, 'capacity': 2, 'remaining_count': 10, 'description': '宽敞的湖景豪华间，配备落地窗，可欣赏到美丽的湖光山色。'},
                    {'name': '家庭套房', 'price': 888.00, 'capacity': 4, 'remaining_count': 5, 'description': '适合家庭入住的套房，配备两间卧室，空间宽敞。'},
                ]
            },
            {
                'name': '保定古城精品酒店',
                'address': '河北省保定市莲池区裕华西路200号',
                'phone': '0312-5555555',
                'brief': '位于保定古城区的精品酒店，融合传统与现代，展现古城魅力。',
                'description': '''
                保定古城精品酒店位于保定市古城区，毗邻直隶总督署、古莲花池等著名景点。
                酒店采用传统中式建筑风格，内部装修融合现代元素，既保留了古城韵味，又提供了现代化的舒适体验。
                酒店客房设计精美，每间客房都经过精心布置，营造出温馨舒适的住宿氛围。
                酒店餐厅提供保定传统美食，让您在品味美食的同时，感受古城文化。
                ''',
                'is_recommended': True,
                'rating': 4.7,
                'views_count': random.randint(300, 1200),
                'display_order': 3,
                'room_types': [
                    {'name': '精品标准间', 'price': 268.00, 'capacity': 2, 'remaining_count': 12, 'description': '设计精美的标准间，融合传统与现代元素，舒适温馨。'},
                    {'name': '古城景观房', 'price': 368.00, 'capacity': 2, 'remaining_count': 8, 'description': '可欣赏古城景观的房间，视野开阔，环境优雅。'},
                ]
            },
            {
                'name': '保定商务酒店',
                'address': '河北省保定市竞秀区七一路100号',
                'phone': '0312-3333333',
                'brief': '商务型酒店，位置优越，设施齐全，是商务出行的理想选择。',
                'description': '''
                保定商务酒店位于保定市商业中心，交通便利，周边配套设施完善。
                酒店专为商务旅客设计，提供高速网络、商务中心、会议室等商务设施。
                客房简洁舒适，配备齐全的办公设施，满足商务办公需求。
                酒店餐厅提供营养丰富的早餐和商务套餐，让您在忙碌的商务行程中也能享受美食。
                ''',
                'is_recommended': False,
                'rating': 4.3,
                'views_count': random.randint(200, 800),
                'display_order': 4,
                'room_types': [
                    {'name': '商务标准间', 'price': 198.00, 'capacity': 2, 'remaining_count': 20, 'description': '简洁实用的商务标准间，配备办公桌椅，适合商务出行。'},
                    {'name': '商务大床房', 'price': 228.00, 'capacity': 2, 'remaining_count': 15, 'description': '配备大床的商务房间，空间宽敞，舒适安静。'},
                ]
            },
            {
                'name': '野三坡度假村',
                'address': '河北省保定市涞水县野三坡景区',
                'phone': '0312-2222222',
                'brief': '位于野三坡景区的度假村，环境优美，是亲近自然的好去处。',
                'description': '''
                野三坡度假村位于野三坡景区内，被群山环抱，环境优美，空气清新。
                度假村采用生态建筑理念，与自然环境和谐共存。
                客房设计简约自然，大部分房间可欣赏到山景或园景。
                度假村提供丰富的户外活动，包括徒步、登山、漂流等，让您充分感受大自然的魅力。
                餐厅提供农家菜和山珍野味，让您品尝到地道的山区美食。
                ''',
                'is_recommended': True,
                'rating': 4.5,
                'views_count': random.randint(350, 1300),
                'display_order': 5,
                'room_types': [
                    {'name': '山景标准间', 'price': 228.00, 'capacity': 2, 'remaining_count': 18, 'description': '可欣赏山景的标准间，环境清幽，价格实惠。'},
                    {'name': '山景豪华间', 'price': 388.00, 'capacity': 2, 'remaining_count': 12, 'description': '宽敞的山景豪华间，配备观景阳台，视野开阔。'},
                    {'name': '木屋别墅', 'price': 888.00, 'capacity': 4, 'remaining_count': 4, 'description': '独立的木屋别墅，私密性好，适合家庭或小团体入住。'},
                ]
            },
            {
                'name': '保定温泉度假酒店',
                'address': '河北省保定市涞水县温泉度假区',
                'phone': '0312-1111111',
                'brief': '拥有天然温泉的度假酒店，是放松身心的理想选择。',
                'description': '''
                保定温泉度假酒店位于温泉度假区内，拥有丰富的天然温泉资源。
                酒店客房配备温泉泡池，让您足不出户即可享受温泉的舒适。
                酒店还设有大型温泉中心，提供多种温泉池和SPA服务，让您彻底放松身心。
                酒店餐厅提供养生美食，结合温泉养生理念，让您在享受美食的同时，调理身体。
                ''',
                'is_recommended': True,
                'rating': 4.9,
                'views_count': random.randint(600, 2500),
                'display_order': 6,
                'room_types': [
                    {'name': '温泉标准间', 'price': 488.00, 'capacity': 2, 'remaining_count': 10, 'description': '配备温泉泡池的标准间，可随时享受温泉的舒适。'},
                    {'name': '温泉豪华间', 'price': 688.00, 'capacity': 2, 'remaining_count': 8, 'description': '宽敞的温泉豪华间，配备大型温泉泡池，体验更佳。'},
                    {'name': '温泉套房', 'price': 1288.00, 'capacity': 4, 'remaining_count': 3, 'description': '豪华温泉套房，配备独立温泉泡池和客厅，适合家庭入住。'},
                ]
            },
        ]

        for hotel_data in hotels_data:
            room_types_data = hotel_data.pop('room_types', [])
            
            hotel, created = Hotel.objects.get_or_create(
                name=hotel_data['name'],
                defaults=hotel_data
            )
            
            if created:
                self.stdout.write(f'[OK] 创建酒店: {hotel.name}')
                
                # 创建房间类型
                for room_data in room_types_data:
                    RoomType.objects.create(
                        hotel=hotel,
                        **room_data
                    )
                    self.stdout.write(f'  [OK] 创建房型: {room_data["name"]}')
            else:
                self.stdout.write(self.style.WARNING(f'[SKIP] 酒店已存在: {hotel.name}'))

        self.stdout.write(self.style.SUCCESS('\n成功创建酒店数据！'))

