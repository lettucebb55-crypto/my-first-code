from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from apps.routes.models import RouteCategory, Route, RouteItinerary


class Command(BaseCommand):
    help = '初始化示例路线数据'

    def handle(self, *args, **options):
        self.stdout.write('开始创建示例路线数据...')
        
        # 创建分类
        category1, created = RouteCategory.objects.get_or_create(
            name='历史文化',
            defaults={'description': '历史文化主题旅游路线'}
        )
        category2, created = RouteCategory.objects.get_or_create(
            name='自然风光',
            defaults={'description': '自然风光主题旅游路线'}
        )
        category3, created = RouteCategory.objects.get_or_create(
            name='亲子游',
            defaults={'description': '适合家庭亲子出游的路线'}
        )
        
        # 路线数据
        routes_data = [
            {
                'name': '保定2日历史文化游',
                'category': category1,
                'price': 580.00,
                'days': 2,
                'group_size': 20,
                'deadline': timezone.now().date() + timedelta(days=7),
                'itinerary_summary': '游览直隶总督署、古莲花池等历史文化景点，感受保定深厚的历史底蕴。',
                'cost_include': '景点门票、住宿（1晚）、早餐、导游服务、旅游保险',
                'cost_exclude': '午餐、晚餐、个人消费、往返交通',
                'notes': '请提前7天报名，需携带身份证。',
                'departure_city': '保定',
                'meeting_point': '保定火车站广场',
                'tags': '历史,文化,深度游,2日',
                'rating': 4.8,
                'is_hot': True,
                'is_recommended': True,
                'display_order': 1,
                'itineraries': [
                    {
                        'day_number': 1,
                        'title': '直隶总督署 + 古莲花池',
                        'description': '上午参观直隶总督署，了解清代官署文化；下午游览古莲花池，欣赏古典园林之美。'
                    },
                    {
                        'day_number': 2,
                        'title': '满城汉墓 + 清西陵',
                        'description': '上午参观满城汉墓，观赏金缕玉衣；下午游览清西陵，感受皇家陵寝的庄严。'
                    },
                ]
            },
            {
                'name': '保定植物园1日休闲游',
                'category': category2,
                'price': 268.00,
                'days': 1,
                'group_size': 30,
                'deadline': timezone.now().date() + timedelta(days=3),
                'itinerary_summary': '畅游保定植物园，打卡温室花卉馆、林荫步道与亲子活动区。',
                'cost_include': '景点门票、午餐、导游服务、旅游保险',
                'cost_exclude': '晚餐、个人消费、往返交通',
                'notes': '请提前3天报名，建议携带防晒用品。',
                'departure_city': '保定',
                'meeting_point': '保定汽车站',
                'tags': '自然,休闲,1日,花卉',
                'rating': 4.9,
                'is_hot': True,
                'is_recommended': True,
                'display_order': 2,
                'itineraries': [
                    {
                        'day_number': 1,
                        'title': '保定植物园一日游',
                        'description': '游览保定植物园主景区，参观温室展馆与主题花园，体验轻松休闲的城市微度假。'
                    },
                ]
            },
            {
                'name': '野三坡2日自然风光游',
                'category': category2,
                'price': 680.00,
                'days': 2,
                'group_size': 25,
                'deadline': timezone.now().date() + timedelta(days=10),
                'itinerary_summary': '探秘野三坡，感受大自然的鬼斧神工，体验原始森林的魅力。',
                'cost_include': '景点门票、住宿（1晚）、早餐、午餐、导游服务、旅游保险',
                'cost_exclude': '晚餐、个人消费、往返交通',
                'notes': '请提前10天报名，建议穿着舒适的登山鞋。',
                'departure_city': '保定',
                'meeting_point': '保定汽车站',
                'tags': '自然,登山,2日,森林',
                'rating': 4.7,
                'is_hot': True,
                'is_recommended': True,
                'display_order': 3,
                'itineraries': [
                    {
                        'day_number': 1,
                        'title': '野三坡百里峡',
                        'description': '游览百里峡景区，欣赏奇峰异石，体验峡谷风光。'
                    },
                    {
                        'day_number': 2,
                        'title': '野三坡龙门天关',
                        'description': '参观龙门天关，感受大自然的壮美，体验民俗文化。'
                    },
                ]
            },
            {
                'name': '保定3日深度游',
                'category': category1,
                'price': 980.00,
                'days': 3,
                'group_size': 15,
                'deadline': timezone.now().date() + timedelta(days=14),
                'itinerary_summary': '深度游览保定历史文化景点，全面了解保定历史文化。',
                'cost_include': '景点门票、住宿（2晚）、早餐、导游服务、旅游保险',
                'cost_exclude': '午餐、晚餐、个人消费、往返交通',
                'notes': '请提前14天报名，适合历史文化爱好者。',
                'departure_city': '保定',
                'meeting_point': '保定火车站广场',
                'tags': '历史,文化,深度游,3日',
                'rating': 4.6,
                'is_hot': False,
                'is_recommended': True,
                'display_order': 4,
                'itineraries': [
                    {
                        'day_number': 1,
                        'title': '直隶总督署 + 古莲花池',
                        'description': '参观直隶总督署和古莲花池，了解保定历史文化。'
                    },
                    {
                        'day_number': 2,
                        'title': '满城汉墓 + 清西陵',
                        'description': '参观满城汉墓和清西陵，感受古代文明和皇家文化。'
                    },
                    {
                        'day_number': 3,
                        'title': '狼牙山',
                        'description': '游览狼牙山，接受爱国主义教育，欣赏自然风光。'
                    },
                ]
            },
            {
                'name': '白石山1日摄影游',
                'category': category2,
                'price': 320.00,
                'days': 1,
                'group_size': 20,
                'deadline': timezone.now().date() + timedelta(days=5),
                'itinerary_summary': '专为摄影爱好者设计的路线，捕捉白石山最美瞬间。',
                'cost_include': '景点门票、缆车票、午餐、专业摄影指导、旅游保险',
                'cost_exclude': '晚餐、个人消费、往返交通、摄影器材',
                'notes': '请提前5天报名，建议携带专业摄影器材。',
                'departure_city': '保定',
                'meeting_point': '保定汽车站',
                'tags': '自然,摄影,1日,云海',
                'rating': 4.8,
                'is_hot': True,
                'is_recommended': False,
                'display_order': 5,
                'itineraries': [
                    {
                        'day_number': 1,
                        'title': '白石山摄影一日游',
                        'description': '游览白石山，拍摄奇峰怪石、云海日出等自然美景，专业摄影师现场指导。'
                    },
                ]
            },
            {
                'name': '保定亲子2日游',
                'category': category3,
                'price': 650.00,
                'days': 2,
                'group_size': 20,
                'deadline': timezone.now().date() + timedelta(days=7),
                'itinerary_summary': '适合家庭亲子出游，寓教于乐，让孩子在游玩中学习历史文化。',
                'cost_include': '景点门票、住宿（1晚）、早餐、午餐、导游服务、旅游保险',
                'cost_exclude': '晚餐、个人消费、往返交通',
                'notes': '请提前7天报名，适合3-12岁儿童家庭。',
                'departure_city': '保定',
                'meeting_point': '保定火车站广场',
                'tags': '亲子,教育,2日,家庭',
                'rating': 4.7,
                'is_hot': True,
                'is_recommended': True,
                'display_order': 6,
                'itineraries': [
                    {
                        'day_number': 1,
                        'title': '古莲花池 + 直隶总督署',
                        'description': '游览古莲花池和直隶总督署，通过互动体验了解历史文化。'
                    },
                    {
                        'day_number': 2,
                        'title': '保定植物园',
                        'description': '游览保定植物园，参与自然科普与亲子互动活动，感受城市生态之美。'
                    },
                ]
            },
            {
                'name': '保定古城夜游1日体验',
                'category': category1,
                'price': 238.00,
                'days': 1,
                'group_size': 25,
                'deadline': timezone.now().date() + timedelta(days=2),
                'itinerary_summary': '夜游保定古城核心地标，感受历史建筑夜景与地道小吃文化。',
                'cost_include': '讲解服务、夜游接驳、小吃体验券、旅游保险',
                'cost_exclude': '正餐、个人消费、往返交通',
                'notes': '请提前2天报名，建议穿舒适步行鞋。',
                'departure_city': '保定',
                'meeting_point': '古莲花池南门',
                'tags': '历史,夜游,古城,1日',
                'rating': 4.7,
                'is_hot': True,
                'is_recommended': True,
                'display_order': 7,
                'itineraries': [
                    {
                        'day_number': 1,
                        'title': '古城夜景 + 非遗街区',
                        'description': '傍晚打卡古城墙周边夜景，随后步行游览非遗街区，体验保定本地夜市与传统手作文化。'
                    },
                ]
            },
            {
                'name': '白石山云海2日徒步游',
                'category': category2,
                'price': 699.00,
                'days': 2,
                'group_size': 20,
                'deadline': timezone.now().date() + timedelta(days=6),
                'itinerary_summary': '深入白石山核心景区，体验轻徒步、观云海与高山摄影。',
                'cost_include': '景点门票、住宿（1晚）、早餐、导游服务、旅游保险',
                'cost_exclude': '午餐、晚餐、个人消费、往返交通',
                'notes': '请提前6天报名，建议携带防风外套和登山杖。',
                'departure_city': '保定',
                'meeting_point': '保定火车站东广场',
                'tags': '自然,徒步,云海,2日',
                'rating': 4.8,
                'is_hot': True,
                'is_recommended': True,
                'display_order': 8,
                'itineraries': [
                    {
                        'day_number': 1,
                        'title': '白石山轻徒步',
                        'description': '上午入园后进行轻徒步路线，下午前往观景台拍摄山景，晚上入住景区周边酒店。'
                    },
                    {
                        'day_number': 2,
                        'title': '日出观景 + 返回保定',
                        'description': '清晨观云海日出，早餐后自由活动，午后统一返程。'
                    },
                ]
            },
            {
                'name': '保定植物园亲子科普1日游',
                'category': category3,
                'price': 199.00,
                'days': 1,
                'group_size': 30,
                'deadline': timezone.now().date() + timedelta(days=3),
                'itinerary_summary': '围绕植物园设计亲子科普任务，边玩边学，轻松不赶路。',
                'cost_include': '景点门票、亲子研学手册、讲解服务、旅游保险',
                'cost_exclude': '正餐、个人消费、往返交通',
                'notes': '请提前3天报名，建议携带水壶与防晒用品。',
                'departure_city': '保定',
                'meeting_point': '保定植物园东门游客中心',
                'tags': '亲子,科普,植物园,1日',
                'rating': 4.9,
                'is_hot': True,
                'is_recommended': True,
                'display_order': 9,
                'itineraries': [
                    {
                        'day_number': 1,
                        'title': '温室探索 + 自然课堂',
                        'description': '上午探索温室花卉馆，下午参与自然课堂和亲子互动任务，完成打卡后返程。'
                    },
                ]
            },
            {
                'name': '易县红色文化2日研学游',
                'category': category1,
                'price': 620.00,
                'days': 2,
                'group_size': 35,
                'deadline': timezone.now().date() + timedelta(days=5),
                'itinerary_summary': '融合红色教育与历史文化讲解，适合团队和学生群体研学。',
                'cost_include': '景点门票、住宿（1晚）、早餐、讲解服务、旅游保险',
                'cost_exclude': '午餐、晚餐、个人消费、往返交通',
                'notes': '请提前5天报名，建议携带学生证或团体证明。',
                'departure_city': '保定',
                'meeting_point': '保定客运中心',
                'tags': '历史,红色,研学,2日',
                'rating': 4.7,
                'is_hot': True,
                'is_recommended': True,
                'display_order': 10,
                'itineraries': [
                    {
                        'day_number': 1,
                        'title': '狼牙山红色教育基地',
                        'description': '参观狼牙山红色教育基地，开展主题学习活动，晚间进行研学复盘。'
                    },
                    {
                        'day_number': 2,
                        'title': '清西陵历史文化研学',
                        'description': '结合清西陵讲解进行历史文化拓展，午后返程。'
                    },
                ]
            },
        ]
        
        # 创建路线
        created_count = 0
        for route_data in routes_data:
            itineraries = route_data.pop('itineraries', [])
            route, created = Route.objects.get_or_create(
                name=route_data['name'],
                defaults=route_data
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'[OK] 创建路线: {route.name}'))
                
                # 创建行程
                for itinerary_data in itineraries:
                    RouteItinerary.objects.create(
                        route=route,
                        **itinerary_data
                    )
                    self.stdout.write(f'  [行程] {itinerary_data["title"]}')
            else:
                self.stdout.write(self.style.WARNING(f'[SKIP] 路线已存在: {route.name}'))
        
        self.stdout.write(self.style.SUCCESS(f'\n成功创建 {created_count} 条路线！'))

