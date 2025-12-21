"""
管理命令：将6张图片依次设置为6个酒店的封面图
如果推荐酒店不足6个，会将非推荐酒店设置为推荐
"""
from django.core.management.base import BaseCommand
from django.core.files import File
import os
from apps.hotels.models import Hotel


class Command(BaseCommand):
    help = '将6张图片依次设置为6个酒店的封面图'

    def handle(self, *args, **options):
        # 获取6张图片
        image_dir = 'media/hotel_images_to_add'
        image_files = [
            'hotel_room_1.jpg',
            'hotel_room_2.jpg',
            'hotel_room_3.jpg',
            'hotel_room_4.jpg',
            'hotel_room_5.jpg',
            'hotel_room_6.jpg',
        ]
        
        image_paths = [os.path.join(image_dir, f) for f in image_files]
        
        # 检查图片是否存在
        missing_images = [p for p in image_paths if not os.path.exists(p)]
        if missing_images:
            self.stdout.write(self.style.ERROR(f'以下图片文件不存在: {missing_images}'))
            return
        
        # 获取推荐酒店
        recommended_hotels = list(Hotel.objects.filter(is_recommended=True).order_by('display_order', 'id'))
        
        # 如果推荐酒店不足6个，从非推荐酒店中补充
        if len(recommended_hotels) < 6:
            needed = 6 - len(recommended_hotels)
            non_recommended = list(Hotel.objects.filter(is_recommended=False).order_by('id')[:needed])
            
            if len(non_recommended) < needed:
                self.stdout.write(self.style.ERROR(
                    f'推荐酒店({len(recommended_hotels)}) + 非推荐酒店({len(non_recommended)}) = {len(recommended_hotels) + len(non_recommended)} < 6'
                ))
                self.stdout.write(self.style.INFO('需要创建更多酒店或手动设置推荐酒店'))
                return
            
            # 将非推荐酒店设置为推荐
            for hotel in non_recommended:
                hotel.is_recommended = True
                hotel.display_order = len(recommended_hotels) + 1
                hotel.save(update_fields=['is_recommended', 'display_order'])
                self.stdout.write(self.style.SUCCESS(f'已将 {hotel.name} 设置为推荐酒店'))
                recommended_hotels.append(hotel)
        
        # 确保有6个酒店
        hotels = recommended_hotels[:6]
        
        self.stdout.write(f'准备为 {len(hotels)} 个酒店设置封面图')
        
        # 依次为每个酒店设置封面图
        for i, (hotel, image_path) in enumerate(zip(hotels, image_paths), 1):
            try:
                with open(image_path, 'rb') as f:
                    image_file = File(f, name=os.path.basename(image_path))
                    hotel.cover_image = image_file
                    hotel.save(update_fields=['cover_image'])
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'[{i}/6] {hotel.name} <- {os.path.basename(image_path)}'
                        )
                    )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'设置失败: {hotel.name} - {str(e)}')
                )
        
        self.stdout.write(self.style.SUCCESS('\n完成！6张图片已依次设置为6个酒店的封面图'))

