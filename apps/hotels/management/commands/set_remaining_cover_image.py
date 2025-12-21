"""
管理命令：将剩余的图片设置为酒店封面图
用于处理第6张图片
"""
from django.core.management.base import BaseCommand
from django.core.files import File
import os
from apps.hotels.models import Hotel


class Command(BaseCommand):
    help = '将剩余的图片设置为酒店封面图'

    def handle(self, *args, **options):
        # 查找第6张图片
        image_path = 'media/hotel_images_to_add/hotel_room_6.jpg'
        
        if not os.path.exists(image_path):
            self.stdout.write(self.style.ERROR(f'图片文件不存在: {image_path}'))
            return
        
        # 查找还没有封面图的推荐酒店，或者创建一个新的推荐酒店
        hotels_without_cover = Hotel.objects.filter(
            is_recommended=True,
            cover_image__isnull=True
        ).order_by('display_order', 'id')
        
        if hotels_without_cover.exists():
            hotel = hotels_without_cover.first()
            self.stdout.write(f'找到没有封面图的推荐酒店: {hotel.name}')
        else:
            # 如果没有，找第一个推荐酒店（可能已经有封面图，但我们可以替换）
            hotel = Hotel.objects.filter(is_recommended=True).order_by('display_order', 'id').first()
            if hotel:
                self.stdout.write(f'所有推荐酒店都有封面图，将替换第一个酒店的封面图: {hotel.name}')
            else:
                self.stdout.write(self.style.ERROR('没有找到推荐酒店'))
                return
        
        try:
            with open(image_path, 'rb') as f:
                image_file = File(f, name=os.path.basename(image_path))
                hotel.cover_image = image_file
                hotel.save(update_fields=['cover_image'])
                self.stdout.write(
                    self.style.SUCCESS(
                        f'成功设置封面图: {hotel.name} - {os.path.basename(image_path)}'
                    )
                )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'设置封面图失败: {str(e)}')
            )

