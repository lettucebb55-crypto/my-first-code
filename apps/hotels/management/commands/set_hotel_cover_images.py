"""
管理命令：将图片设置为推荐酒店的封面图

使用方法：
1. 将图片文件放到 media/hotel_images_to_add/ 目录下
2. 运行命令：python manage.py set_hotel_cover_images

或者直接指定图片路径：
python manage.py set_hotel_cover_images --image-path /path/to/image1.jpg --image-path /path/to/image2.jpg
"""
from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings
import os
from apps.hotels.models import Hotel


class Command(BaseCommand):
    help = '将图片设置为推荐酒店的封面图'

    def add_arguments(self, parser):
        parser.add_argument(
            '--image-path',
            action='append',
            dest='image_paths',
            help='图片文件路径（可多次使用）',
        )
        parser.add_argument(
            '--from-dir',
            type=str,
            default='media/hotel_images_to_add',
            help='从指定目录读取图片（默认：media/hotel_images_to_add）',
        )

    def handle(self, *args, **options):
        image_paths = options.get('image_paths', [])
        from_dir = options.get('from_dir')
        
        # 如果没有指定图片路径，从目录读取
        if not image_paths:
            if os.path.exists(from_dir):
                image_paths = [
                    os.path.join(from_dir, f)
                    for f in sorted(os.listdir(from_dir))  # 排序确保顺序
                    if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp'))
                ]
                if not image_paths:
                    self.stdout.write(self.style.WARNING(f'目录 {from_dir} 中没有找到图片文件'))
                    return
            else:
                self.stdout.write(self.style.WARNING(f'目录 {from_dir} 不存在'))
                self.stdout.write(self.style.INFO('提示：请将图片文件放到该目录，或使用 --image-path 参数指定图片路径'))
                return
        
        # 获取推荐酒店（按display_order排序）
        hotels = list(Hotel.objects.filter(is_recommended=True).order_by('display_order', 'id'))
        
        if not hotels:
            self.stdout.write(self.style.ERROR('没有找到推荐酒店，请先创建推荐酒店'))
            return
        
        if len(image_paths) > len(hotels):
            self.stdout.write(self.style.WARNING(
                f'图片数量({len(image_paths)})多于推荐酒店数量({len(hotels)})，将只处理前{len(hotels)}张图片'
            ))
            image_paths = image_paths[:len(hotels)]
        elif len(image_paths) < len(hotels):
            self.stdout.write(self.style.WARNING(
                f'图片数量({len(image_paths)})少于推荐酒店数量({len(hotels)})，将只处理前{len(image_paths)}个酒店'
            ))
            hotels = hotels[:len(image_paths)]
        
        self.stdout.write(f'找到 {len(hotels)} 个推荐酒店')
        self.stdout.write(f'准备设置 {len(image_paths)} 张封面图')
        
        # 依次为每个酒店设置封面图
        updated_count = 0
        for i, (hotel, image_path) in enumerate(zip(hotels, image_paths), 1):
            if not os.path.exists(image_path):
                self.stdout.write(self.style.WARNING(f'图片文件不存在: {image_path}'))
                continue
            
            try:
                # 打开图片文件并设置为封面图
                with open(image_path, 'rb') as f:
                    image_file = File(f, name=os.path.basename(image_path))
                    hotel.cover_image = image_file
                    hotel.save(update_fields=['cover_image'])
                    updated_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'[{i}/{len(hotels)}] 设置封面图: {hotel.name} - {os.path.basename(image_path)}'
                        )
                    )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'设置封面图失败: {hotel.name} - {str(e)}')
                )
        
        self.stdout.write(self.style.SUCCESS(f'\n成功为 {updated_count} 个酒店设置封面图！'))
        
        # 显示结果
        self.stdout.write('\n酒店封面图设置情况：')
        for hotel in hotels:
            if hotel.cover_image:
                self.stdout.write(f'  [OK] {hotel.name}: {hotel.cover_image.name}')
            else:
                self.stdout.write(f'  [NO] {hotel.name}: 无封面图')

