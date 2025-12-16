from django.core.management.base import BaseCommand
from django.core.files import File
from apps.routes.models import Route
import os
from django.conf import settings


class Command(BaseCommand):
    help = '更新路线封面图片'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--image-dir',
            type=str,
            default=None,
            help='图片文件所在目录（如果不指定，默认使用 media/route_covers/）'
        )

    def handle(self, *args, **options):
        self.stdout.write('开始更新路线封面图片...')
        
        # 路线封面图片映射
        # 根据用户要求：
        # 第二张图片（山景）-> 保定2日历史文化游
        # 第三张图片（河流湖泊）-> 白洋淀1日休闲游
        # 以此类推...
        
        route_covers = {
            '保定2日历史文化游': 'route_cover_2.jpg',  # 第二张图片（山景）
            '白洋淀1日休闲游': 'route_cover_3.jpg',   # 第三张图片（河流湖泊）
            '野三坡2日自然风光游': 'route_cover_4.jpg',  # 第四张图片（河流和城镇）
            '保定3日深度游': 'route_cover_5.jpg',      # 第五张图片（山景）
            '白石山1日摄影游': 'route_cover_6.jpg',    # 第六张图片（山景）
            '保定亲子2日游': 'route_cover_7.jpg',      # 第七张图片（海滩）
        }
        
        # 确定图片目录
        if options['image_dir']:
            image_dir = options['image_dir']
        else:
            media_root = settings.MEDIA_ROOT
            image_dir = os.path.join(media_root, 'route_covers')
        
        # 如果目录不存在，创建它
        if not os.path.exists(image_dir):
            os.makedirs(image_dir)
            self.stdout.write(self.style.WARNING(f'创建目录: {image_dir}'))
        
        updated_count = 0
        skipped_count = 0
        error_count = 0
        
        for route_name, cover_filename in route_covers.items():
            try:
                route = Route.objects.get(name=route_name)
                
                # 尝试多个可能的文件名（支持不同扩展名）
                possible_names = [
                    cover_filename,
                    cover_filename.replace('.jpg', '.jpeg'),
                    cover_filename.replace('.jpg', '.png'),
                    f'image_{list(route_covers.keys()).index(route_name) + 2}.jpg',
                    f'image_{list(route_covers.keys()).index(route_name) + 2}.jpeg',
                    f'image_{list(route_covers.keys()).index(route_name) + 2}.png',
                ]
                
                cover_path = None
                for name in possible_names:
                    test_path = os.path.join(image_dir, name)
                    if os.path.exists(test_path):
                        cover_path = test_path
                        cover_filename = name
                        break
                
                if cover_path:
                    with open(cover_path, 'rb') as f:
                        route.cover_image.save(cover_filename, File(f), save=True)
                    self.stdout.write(self.style.SUCCESS(f'[OK] 更新封面: {route_name} -> {cover_filename}'))
                    updated_count += 1
                else:
                    self.stdout.write(self.style.WARNING(f'[SKIP] 图片不存在: {route_name} (查找目录: {image_dir})'))
                    skipped_count += 1
            except Route.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'[ERROR] 路线不存在: {route_name}'))
                error_count += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'[ERROR] 更新失败 {route_name}: {str(e)}'))
                error_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'\n完成！成功更新 {updated_count} 条路线，跳过 {skipped_count} 条，错误 {error_count} 条'))
        
        if skipped_count > 0:
            self.stdout.write(self.style.WARNING('\n提示：请将图片文件放置在以下目录：'))
            self.stdout.write(f'  {image_dir}')
            self.stdout.write(self.style.WARNING('\n支持的图片文件名：'))
            for route_name, cover_filename in route_covers.items():
                self.stdout.write(f'  - {cover_filename} 或 image_{list(route_covers.keys()).index(route_name) + 2}.jpg -> {route_name}')

