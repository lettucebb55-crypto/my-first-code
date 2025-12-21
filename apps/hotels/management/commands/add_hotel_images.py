"""
管理命令：将图片添加到推荐酒店

使用方法：
1. 将图片文件放到 media/hotel_images_to_add/ 目录下
2. 运行命令：python manage.py add_hotel_images

或者直接指定图片路径：
python manage.py add_hotel_images --image-path /path/to/image1.jpg --image-path /path/to/image2.jpg
"""
from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings
import os
from apps.hotels.models import Hotel, HotelImage


class Command(BaseCommand):
    help = '将图片添加到推荐酒店'

    def add_arguments(self, parser):
        parser.add_argument(
            '--image-path',
            action='append',
            dest='image_paths',
            help='图片文件路径（可多次使用）',
        )
        parser.add_argument(
            '--hotel-id',
            type=int,
            help='指定酒店ID（如果不指定，将自动分配到推荐酒店）',
        )
        parser.add_argument(
            '--from-dir',
            type=str,
            default='media/hotel_images_to_add',
            help='从指定目录读取图片（默认：media/hotel_images_to_add）',
        )

    def handle(self, *args, **options):
        image_paths = options.get('image_paths', [])
        hotel_id = options.get('hotel_id')
        from_dir = options.get('from_dir')
        
        # 如果没有指定图片路径，从目录读取
        if not image_paths:
            if os.path.exists(from_dir):
                image_paths = [
                    os.path.join(from_dir, f)
                    for f in os.listdir(from_dir)
                    if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp'))
                ]
                if not image_paths:
                    self.stdout.write(self.style.WARNING(f'目录 {from_dir} 中没有找到图片文件'))
                    return
            else:
                self.stdout.write(self.style.WARNING(f'目录 {from_dir} 不存在'))
                self.stdout.write(self.style.INFO('提示：请将图片文件放到该目录，或使用 --image-path 参数指定图片路径'))
                return
        
        # 获取推荐酒店
        if hotel_id:
            try:
                hotels = [Hotel.objects.get(id=hotel_id)]
            except Hotel.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'酒店ID {hotel_id} 不存在'))
                return
        else:
            hotels = list(Hotel.objects.filter(is_recommended=True).order_by('display_order', '-rating'))
            if not hotels:
                self.stdout.write(self.style.ERROR('没有找到推荐酒店，请先创建推荐酒店'))
                return
        
        self.stdout.write(f'找到 {len(hotels)} 个推荐酒店')
        self.stdout.write(f'准备添加 {len(image_paths)} 张图片')
        
        # 分配图片到酒店（循环分配）
        added_count = 0
        for i, image_path in enumerate(image_paths):
            if not os.path.exists(image_path):
                self.stdout.write(self.style.WARNING(f'图片文件不存在: {image_path}'))
                continue
            
            # 选择酒店（循环分配）
            hotel = hotels[i % len(hotels)]
            
            # 创建图片记录
            try:
                with open(image_path, 'rb') as f:
                    image_file = File(f, name=os.path.basename(image_path))
                    hotel_image = HotelImage.objects.create(
                        hotel=hotel,
                        image=image_file,
                        title=f'酒店房间图片 {i+1}',
                        description=f'来自 {os.path.basename(image_path)}',
                        display_order=i
                    )
                    added_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'[OK] 添加图片到酒店: {hotel.name} - {os.path.basename(image_path)}'
                        )
                    )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'添加图片失败: {image_path} - {str(e)}')
                )
        
        self.stdout.write(self.style.SUCCESS(f'\n成功添加 {added_count} 张图片到推荐酒店！'))
        
        # 显示统计信息
        for hotel in hotels:
            image_count = HotelImage.objects.filter(hotel=hotel).count()
            self.stdout.write(f'  {hotel.name}: {image_count} 张图片')

