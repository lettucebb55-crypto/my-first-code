from django.core.management.base import BaseCommand
from apps.scenic.models import ScenicCategory, ScenicSpot


class Command(BaseCommand):
    help = '初始化示例景点数据'

    def handle(self, *args, **options):
        self.stdout.write('开始创建示例景点数据...')
        
        # 创建分类
        category1, created = ScenicCategory.objects.get_or_create(
            name='历史文化',
            defaults={'description': '保定历史文化景点'}
        )
        category2, created = ScenicCategory.objects.get_or_create(
            name='自然风光',
            defaults={'description': '保定自然风光景点'}
        )
        category3, created = ScenicCategory.objects.get_or_create(
            name='人文古迹',
            defaults={'description': '保定人文古迹景点'}
        )
        
        # 景点数据
        spots_data = [
            {
                'name': '直隶总督署',
                'category': category1,
                'address': '河北省保定市莲池区裕华西路301号',
                'ticket_price': 30.00,
                'open_time': '08:00-18:00',
                'description': '直隶总督署是中国保存最完整的清代省级衙署，有"一座总督署，半部清史写"的美誉。',
                'phone': '0312-2022574',
                'traffic_info': '可乘坐公交1路、2路、4路、8路、12路、16路、18路、20路、22路、26路、28路、30路、32路、35路、36路、38路、39路、50路、51路、52路、53路、55路、56路、58路、59路、60路、61路、62路、63路、64路、65路、66路、67路、68路、69路、70路、71路、72路、73路、74路、75路、76路、77路、78路、79路、80路、81路、82路、83路、84路、85路、86路、87路、88路、89路、90路、91路、92路、93路、94路、95路、96路、97路、98路、99路、100路到总督署站下车',
                'best_season': '四季皆宜',
                'visit_duration': '2-3小时',
                'tags': '历史,古迹,清代,文化',
                'rating': 4.8,
                'is_hot': True,
                'is_recommended': True,
                'display_order': 1,
            },
            {
                'name': '白洋淀',
                'category': category2,
                'address': '河北省保定市安新县白洋淀景区',
                'ticket_price': 185.00,
                'open_time': '07:00-18:00',
                'description': '白洋淀是华北地区最大的淡水湖，被誉为"华北明珠"。这里荷香苇绿，水天一色，是休闲度假的好去处。',
                'phone': '0312-5116352',
                'traffic_info': '从保定市区可乘坐长途客车到安新县，再转乘景区班车',
                'best_season': '夏季（6-9月）',
                'visit_duration': '1天',
                'tags': '自然,湖泊,荷花,休闲',
                'rating': 4.9,
                'is_hot': True,
                'is_recommended': True,
                'display_order': 2,
            },
            {
                'name': '古莲花池',
                'category': category1,
                'address': '河北省保定市莲池区裕华西路246号',
                'ticket_price': 30.00,
                'open_time': '08:00-18:00',
                'description': '古莲花池是中国北方著名的古典园林，始建于元代，有"城市蓬莱"的美誉。',
                'phone': '0312-2022574',
                'traffic_info': '可乘坐公交1路、2路、4路、8路、12路、16路、18路、20路、22路、26路、28路、30路、32路、35路、36路、38路、39路、50路、51路、52路、53路、55路、56路、58路、59路、60路、61路、62路、63路、64路、65路、66路、67路、68路、69路、70路、71路、72路、73路、74路、75路、76路、77路、78路、79路、80路、81路、82路、83路、84路、85路、86路、87路、88路、89路、90路、91路、92路、93路、94路、95路、96路、97路、98路、99路、100路到古莲花池站下车',
                'best_season': '夏季（6-8月）',
                'visit_duration': '1-2小时',
                'tags': '园林,历史,荷花,文化',
                'rating': 4.7,
                'is_hot': True,
                'is_recommended': True,
                'display_order': 3,
            },
            {
                'name': '野三坡',
                'category': category2,
                'address': '河北省保定市涞水县野三坡镇',
                'ticket_price': 100.00,
                'open_time': '07:00-18:00',
                'description': '野三坡是国家级风景名胜区，以奇山异水、原始森林、民俗风情著称。',
                'phone': '0312-4568106',
                'traffic_info': '从保定市区可乘坐长途客车到涞水县，再转乘景区班车',
                'best_season': '春夏秋三季',
                'visit_duration': '1-2天',
                'tags': '自然,山水,森林,休闲',
                'rating': 4.6,
                'is_hot': True,
                'is_recommended': True,
                'display_order': 4,
            },
            {
                'name': '清西陵',
                'category': category3,
                'address': '河北省保定市易县西陵镇',
                'ticket_price': 120.00,
                'open_time': '08:00-17:30',
                'description': '清西陵是清朝最后一处帝王陵墓建筑群，是中国现存规模最大、保存最完整的皇家陵寝之一。',
                'phone': '0312-4710012',
                'traffic_info': '从保定市区可乘坐长途客车到易县，再转乘景区班车',
                'best_season': '四季皆宜',
                'visit_duration': '半天',
                'tags': '历史,陵墓,清代,文化',
                'rating': 4.5,
                'is_hot': True,
                'is_recommended': False,
                'display_order': 5,
            },
            {
                'name': '狼牙山',
                'category': category2,
                'address': '河北省保定市易县狼牙山镇',
                'ticket_price': 80.00,
                'open_time': '07:00-18:00',
                'description': '狼牙山以"狼牙山五壮士"而闻名，是爱国主义教育基地，也是登山观景的好去处。',
                'phone': '0312-8861888',
                'traffic_info': '从保定市区可乘坐长途客车到易县，再转乘景区班车',
                'best_season': '春夏秋三季',
                'visit_duration': '半天',
                'tags': '红色,登山,自然,教育',
                'rating': 4.4,
                'is_hot': True,
                'is_recommended': False,
                'display_order': 6,
            },
            {
                'name': '满城汉墓',
                'category': category3,
                'address': '河北省保定市满城区陵山',
                'ticket_price': 50.00,
                'open_time': '08:00-17:30',
                'description': '满城汉墓是西汉中山靖王刘胜及其妻窦绾的墓葬，出土了著名的"金缕玉衣"。',
                'phone': '0312-7072035',
                'traffic_info': '从保定市区可乘坐公交或长途客车到满城区',
                'best_season': '四季皆宜',
                'visit_duration': '2-3小时',
                'tags': '历史,汉墓,文物,文化',
                'rating': 4.3,
                'is_hot': False,
                'is_recommended': True,
                'display_order': 7,
            },
            {
                'name': '白石山',
                'category': category2,
                'address': '河北省保定市涞源县白石山镇',
                'ticket_price': 150.00,
                'open_time': '07:00-18:00',
                'description': '白石山是国家级地质公园，以奇峰怪石、云海日出而闻名，是摄影爱好者的天堂。',
                'phone': '0312-7313456',
                'traffic_info': '从保定市区可乘坐长途客车到涞源县，再转乘景区班车',
                'best_season': '春夏秋三季',
                'visit_duration': '1天',
                'tags': '自然,山峰,云海,摄影',
                'rating': 4.8,
                'is_hot': True,
                'is_recommended': True,
                'display_order': 8,
            },
        ]
        
        # 创建景点
        created_count = 0
        for spot_data in spots_data:
            spot, created = ScenicSpot.objects.get_or_create(
                name=spot_data['name'],
                defaults=spot_data
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'[OK] 创建景点: {spot.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'[SKIP] 景点已存在: {spot.name}'))
        
        self.stdout.write(self.style.SUCCESS(f'\n成功创建 {created_count} 个景点！'))

