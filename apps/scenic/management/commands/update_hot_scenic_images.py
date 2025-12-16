from django.core.management.base import BaseCommand
from apps.scenic.models import ScenicSpot
import os
from django.conf import settings


class Command(BaseCommand):
    help = '更新热门景点的封面图片'

    def handle(self, *args, **options):
        self.stdout.write('开始更新热门景点封面图片...')
        
        # 景点名称和对应的图片文件名映射
        scenic_image_map = {
            '直隶总督署': 'zhili_governor_office1.jpg',
            '古莲花池': 'gulianhuachi1.jpg',
            '野三坡': 'yesanpo1.jpg',
            '清西陵': 'qingxiling1.jpg',
            '狼牙山': 'langyashan1.jpg',
            '白石山': 'baishishan1.jpg',
            '满城汉墓': 'manchenghanmu1.jpg',
        }
        
        # 确保 scenic_covers 目录存在
        scenic_covers_dir = os.path.join(settings.MEDIA_ROOT, 'scenic_covers')
        os.makedirs(scenic_covers_dir, exist_ok=True)
        
        updated_count = 0
        not_found_count = 0
        
        for scenic_name, image_filename in scenic_image_map.items():
            try:
                spot = ScenicSpot.objects.get(name=scenic_name)
                
                # 检查图片文件是否存在
                image_path = os.path.join(scenic_covers_dir, image_filename)
                
                if os.path.exists(image_path):
                    # 更新封面图片路径（相对路径）
                    spot.cover_image = f'scenic_covers/{image_filename}'
                    spot.is_hot = True  # 确保是热门景点
                    spot.save()
                    updated_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'[OK] 更新 {scenic_name} 的封面图片: {image_filename}')
                    )
                else:
                    not_found_count += 1
                    self.stdout.write(
                        self.style.WARNING(
                            f'[WARN] {scenic_name} 的图片文件不存在: {image_path}\n'
                            f'       请将图片文件放到: {scenic_covers_dir}/'
                        )
                    )
                    
            except ScenicSpot.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'[ERROR] 景点不存在: {scenic_name}')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'[ERROR] 更新 {scenic_name} 时出错: {str(e)}')
                )
        
        self.stdout.write(self.style.SUCCESS(f'\n成功更新 {updated_count} 个景点的封面图片！'))
        if not_found_count > 0:
            self.stdout.write(
                self.style.WARNING(
                    f'\n有 {not_found_count} 个景点的图片文件未找到。\n'
                    f'请将图片文件放到以下目录: {scenic_covers_dir}/\n'
                    f'图片文件名应该为:\n'
                    f'  - zhili_governor_office1.jpg (直隶总督署)\n'
                    f'  - gulianhuachi1.jpg (古莲花池)\n'
                    f'  - yesanpo1.jpg (野三坡)\n'
                    f'  - qingxiling1.jpg (清西陵)\n'
                    f'  - langyashan1.jpg (狼牙山)\n'
                    f'  - baishishan1.jpg (白石山)\n'
                    f'  - manchenghanmu1.jpg (满城汉墓)'
                )
            )

