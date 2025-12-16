from django.core.management.base import BaseCommand
from apps.foods.models import FoodCategory, Food, FoodImage


class Command(BaseCommand):
    help = '初始化美食数据'

    def handle(self, *args, **options):
        self.stdout.write('开始创建美食数据...')
        
        # 创建分类
        category1, created = FoodCategory.objects.get_or_create(
            name='传统小吃',
            defaults={
                'description': '保定传统小吃，历史悠久，口味独特',
                'icon': 'fa-drumstick-bite',
                'display_order': 1
            }
        )
        category2, created = FoodCategory.objects.get_or_create(
            name='地方特色菜',
            defaults={
                'description': '保定地方特色菜品，传承经典',
                'icon': 'fa-utensils',
                'display_order': 2
            }
        )
        category3, created = FoodCategory.objects.get_or_create(
            name='水乡美食',
            defaults={
                'description': '白洋淀等水乡地区的特色美食',
                'icon': 'fa-fish',
                'display_order': 3
            }
        )
        category4, created = FoodCategory.objects.get_or_create(
            name='宫廷美食',
            defaults={
                'description': '传承宫廷风味的经典美食',
                'icon': 'fa-crown',
                'display_order': 4
            }
        )
        
        # 美食数据
        foods_data = [
            {
                'name': '保定驴肉火烧',
                'english_name': 'Baoding Donkey Meat Sandwich',
                'category': category1,
                'description': '''保定驴肉火烧是河北省保定市的传统名小吃，被誉为"保定三宝"之一。
历史悠久，早在明代就已经在保定地区流传。驴肉火烧选用优质驴肉，配以酥脆的火烧饼皮，口感层次丰富。

火烧饼皮金黄酥脆，内里松软；驴肉肉质鲜嫩，香味浓郁，营养丰富。传统的制作工艺代代相传，是保定人早餐的首选，也是外地游客必尝的特色小吃。''',
                'ingredients': '优质驴肉、面粉、葱、姜、蒜、花椒、八角、桂皮、香叶等',
                'cooking_method': '''1. 将驴肉洗净，用调料腌制入味
2. 用慢火炖煮至肉质软烂
3. 将面粉和成面团，擀成圆饼
4. 在平底锅中烙制火烧饼，至两面金黄
5. 将炖好的驴肉切碎，夹入火烧饼中
6. 可根据个人口味加入青椒、香菜等配菜''',
                'cultural_background': '''保定驴肉火烧起源于明代，已有数百年的历史。传说当年保定府有一位姓王的师傅，用驴肉制作火烧，深受当地人喜爱，从此流传开来。

在保定，驴肉火烧不仅是一种美食，更是一种文化传承。每逢重要节日，家家户户都会制作驴肉火烧，寓意着团圆和幸福。这道美食承载着保定人对家乡的深深眷恋。''',
                'price_range': '15-30元/个',
                'average_price': 20.00,
                'is_hot': True,
                'is_recommended': True,
                'is_traditional': True,
                'rating': 4.9,
                'tags': '传统,小吃,早餐,地方特色',
                'recommended_restaurants': '''老槐树驴肉火烧（保定老字号）
闫家驴肉火烧（连锁品牌）
高建良驴肉火烧（传统老店）''',
                'display_order': 1,
            },
            {
                'name': '白洋淀全鱼宴',
                'english_name': 'Baiyangdian Fish Banquet',
                'category': category3,
                'description': '''白洋淀全鱼宴是白洋淀地区的特色美食，以新鲜的湖鱼为原料，采用多种烹饪方式制作而成。
全鱼宴包括鱼头、鱼身、鱼尾等不同部位的多种做法，如清蒸、红烧、糖醋、酸菜鱼等。

白洋淀水质优良，出产的鱼类肉质鲜嫩，营养丰富。全鱼宴不仅展现了当地渔民的烹饪技艺，更是对白洋淀丰富水产资源的充分利用。''',
                'ingredients': '白洋淀湖鱼（草鱼、鲤鱼、鲢鱼等）、豆腐、粉条、酸菜、辣椒、葱、姜、蒜、料酒、酱油等',
                'cooking_method': '''1. 选用新鲜的白洋淀湖鱼，处理干净
2. 根据不同做法准备配料：清蒸需葱姜丝，红烧需糖色，酸菜鱼需酸菜和辣椒
3. 清蒸鱼：鱼身划花刀，加调料蒸制15-20分钟
4. 红烧鱼：先煎至两面金黄，再加调料炖煮
5. 酸菜鱼：鱼肉片薄片，与酸菜同煮，麻辣鲜香
6. 搭配豆腐、粉条等配菜，丰富口感''',
                'cultural_background': '''白洋淀是华北地区最大的淡水湖，水产资源丰富。当地渔民世代以捕鱼为生，对鱼的烹饪有着独特的技艺。

全鱼宴是白洋淀地区的传统宴席，体现了当地人对水资源的珍视和对美食的追求。每逢重要节日或招待客人，当地人都会准备丰盛的全鱼宴，表达对客人的热情欢迎。''',
                'price_range': '200-500元/桌',
                'average_price': 350.00,
                'is_hot': True,
                'is_recommended': True,
                'is_traditional': True,
                'rating': 4.8,
                'tags': '水乡,鱼类,宴席,特色菜',
                'recommended_restaurants': '''白洋淀景区内餐厅
安新县渔家乐
白洋淀度假酒店餐厅''',
                'display_order': 2,
            },
            {
                'name': '保定糖葫芦',
                'english_name': 'Baoding Candied Hawthorn',
                'category': category1,
                'description': '''保定糖葫芦是保定的传统小吃，以山楂为主料，裹上糖浆制作而成。
糖葫芦的制作工艺独特，糖浆要熬制到恰到好处，既要有脆脆的糖壳，又要保持山楂的酸甜口感。

保定的糖葫芦品种丰富，除了传统的山楂，还有草莓、葡萄、小番茄等多种水果口味，深受各年龄段人群的喜爱。''',
                'ingredients': '山楂（或草莓、葡萄等水果）、白砂糖、冰糖、芝麻',
                'cooking_method': '''1. 将山楂洗净，去核，用竹签串好
2. 将白砂糖和冰糖按比例混合，加少量水
3. 用小火熬制糖浆，至糖浆呈金黄色，能拉丝
4. 将串好的山楂快速在糖浆中滚动，均匀裹上糖浆
5. 将裹好糖浆的糖葫芦放在涂有油的板子上冷却
6. 待糖壳凝固后即可食用''',
                'cultural_background': '''糖葫芦是中国北方的传统小吃，有着悠久的历史。保定作为历史文化名城，糖葫芦的制作技艺也得到了很好的传承。

在保定的大街小巷，经常可以看到制作糖葫芦的摊贩。特别是在冬季，一串串红彤彤的糖葫芦成为街头一道亮丽的风景线。糖葫芦不仅是美食，更是保定人童年的美好回忆。''',
                'price_range': '5-15元/串',
                'average_price': 8.00,
                'is_hot': False,
                'is_recommended': True,
                'is_traditional': True,
                'rating': 4.6,
                'tags': '传统,小吃,甜食,零食',
                'recommended_restaurants': '''街头小摊（传统制作）
保定古城区小吃街
各景区门口摊位''',
                'display_order': 3,
            },
            {
                'name': '保定锅包肘子',
                'english_name': 'Baoding Braised Pork Knuckle',
                'category': category2,
                'description': '''保定锅包肘子是保定的传统名菜，选用优质猪肘，经过精心炖煮而成。
肘子经过长时间的慢火炖制，肉质软烂，肥而不腻，入口即化。汤汁浓郁，香味扑鼻，是一道老少皆宜的美食。

这道菜的制作工艺复杂，需要掌握火候和调料的配比，是保定厨师技艺的体现。''',
                'ingredients': '猪肘子、冰糖、老抽、生抽、料酒、葱、姜、八角、桂皮、香叶、草果等',
                'cooking_method': '''1. 将猪肘子洗净，用沸水焯水去血沫
2. 锅中放油，加冰糖炒出糖色
3. 将肘子放入锅中，翻炒上色
4. 加入葱、姜、料酒和各种香料
5. 倒入老抽、生抽，加足量水
6. 用小火慢炖2-3小时，至肉质软烂
7. 最后收汁，使汤汁浓稠''',
                'cultural_background': '''锅包肘子是保定地区的传统名菜，有着深厚的历史文化底蕴。在保定的传统宴席上，这道菜是不可或缺的主菜之一。

这道菜体现了保定人对美食的精致追求，也是对传统烹饪技艺的传承。制作锅包肘子需要耐心和技艺，体现了保定人的工匠精神。''',
                'price_range': '80-150元/份',
                'average_price': 120.00,
                'is_hot': True,
                'is_recommended': True,
                'is_traditional': True,
                'rating': 4.7,
                'tags': '传统,肉类,特色菜,宴席',
                'recommended_restaurants': '''保定老字号餐厅
直隶总督署附近餐厅
古城美食街''',
                'display_order': 4,
            },
            {
                'name': '保定熏肉',
                'english_name': 'Baoding Smoked Meat',
                'category': category2,
                'description': '''保定熏肉是保定的传统特色美食，选用优质猪肉，经过腌制、熏制等工艺制作而成。
熏肉色泽红润，香味独特，肉质紧实，有嚼劲。既可以单独食用，也可以作为配菜，是保定人餐桌上的常客。

保定的熏肉制作工艺独特，熏制时使用的木料和火候都有讲究，使得熏肉具有独特的香味。''',
                'ingredients': '优质猪肉（五花肉或瘦肉）、盐、花椒、八角、桂皮、香叶、糖、茶叶等',
                'cooking_method': '''1. 将猪肉洗净，切成大块
2. 用盐、花椒等调料腌制24小时以上
3. 将腌制好的肉用清水冲洗，去除多余的盐分
4. 将肉放入锅中，加调料和清水，煮至八成熟
5. 准备熏锅，在锅底铺上茶叶、糖等熏料
6. 将煮好的肉放在熏架上，盖上锅盖
7. 用小火熏制20-30分钟，至肉色红润
8. 取出晾凉，切片即可食用''',
                'cultural_background': '''熏肉是中国传统的肉制品加工方法，有着悠久的历史。保定作为历史文化名城，熏肉制作技艺也得到了很好的传承和发展。

在保定，熏肉不仅是家常菜，也是招待客人的上等菜肴。熏肉的独特香味和口感，使其成为保定美食文化的重要组成部分。''',
                'price_range': '60-120元/斤',
                'average_price': 85.00,
                'is_hot': False,
                'is_recommended': True,
                'is_traditional': True,
                'rating': 4.5,
                'tags': '传统,肉类,熏制,特色',
                'recommended_restaurants': '''保定老字号熏肉店
传统肉制品专营店
古城美食街''',
                'display_order': 5,
            },
        ]
        
        # 创建美食
        created_count = 0
        for food_data in foods_data:
            food, created = Food.objects.get_or_create(
                name=food_data['name'],
                defaults=food_data
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'[OK] 创建美食: {food.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'[SKIP] 美食已存在: {food.name}'))
        
        self.stdout.write(self.style.SUCCESS(f'\n成功创建 {created_count} 道美食！'))

