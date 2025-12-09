import sys
import os
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.hashers import make_password, is_password_usable
# 务必替换为你的SysUser模型实际路径！！！
from user.models import SysUser

# 强制设置Python终端输出编码为UTF-8（解决Windows中文显示乱码）
if sys.platform == 'win32':
    # 切换控制台代码页为UTF-8（隐藏执行输出）
    os.system('chcp 65001 >nul 2>&1')
    # 兼容Python 3.7+ 输出编码
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        # 兼容Python 3.6及以下版本
        import io

        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


class Command(BaseCommand):
    """
    增强版密码哈希工具（适配Windows PowerShell中文，修复编码报错）
    用法1：修改单个用户密码（核心功能）
      python manage.py hash_password single python222 123456
    用法2：批量修改用户密码（支持中文用户名/密码）
      python manage.py hash_password batch "python222:123456,张三:654321,李四:888888"
    用法3：全库扫描明文密码并批量哈希
      python manage.py hash_password update-all
    用法4：仅生成哈希（不写库，支持中文密码）
      python manage.py hash_password gen-hash 123456
    用法5：仅生成批量哈希（不写库，支持中文密码）
      python manage.py hash_password gen-batch "123456,管理员888,测试密码"
    """
    help = __doc__

    def add_arguments(self, parser):
        """重新设计参数（避免PowerShell解析冲突）"""
        # 子命令分组（解决参数互斥问题）
        subparsers = parser.add_subparsers(dest='command', help='操作类型')

        # 子命令1：修改单个用户（支持中文用户名/密码）
        single_parser = subparsers.add_parser('single', help='修改单个用户密码')
        single_parser.add_argument('username', type=str, help='用户名（支持中文）')
        single_parser.add_argument('password', type=str, help='明文密码（支持中文）')

        # 子命令2：批量修改用户（支持中文）
        batch_parser = subparsers.add_parser('batch', help='批量修改用户密码')
        batch_parser.add_argument('user_pwd_str', type=str,
                                  help='格式：用户名1:密码1,用户名2:密码2（支持中文）')

        # 子命令3：全库更新明文密码
        all_parser = subparsers.add_parser('update-all', help='全库扫描明文密码并哈希')

        # 子命令4：仅生成单哈希（不写库，支持中文）
        gen_hash_parser = subparsers.add_parser('gen-hash', help='仅生成单密码哈希（不写库）')
        gen_hash_parser.add_argument('password', type=str, help='明文密码（支持中文）')

        # 子命令5：仅生成批量哈希（不写库，支持中文）
        gen_batch_parser = subparsers.add_parser('gen-batch', help='仅生成批量密码哈希（不写库）')
        gen_batch_parser.add_argument('passwords', type=str, help='格式：密码1,密码2,密码3（支持中文）')

    def is_plain_password(self, password: str) -> bool:
        """判断是否为明文密码（非Django标准哈希）"""
        if not password:
            return False
        # Django内置方法+哈希前缀校验
        if not is_password_usable(password):
            return True
        hash_prefixes = ['pbkdf2_sha256$', 'bcrypt$', 'argon2$', 'sha1$', 'md5$']
        return not any(password.startswith(p) for p in hash_prefixes)

    def handle_single_user(self, username: str, password: str):
        """修改单个用户密码（支持中文，修复编码报错）"""
        try:
            # 直接使用原生字符串，无需额外转码（PowerShell已传递正确的Unicode）
            user = SysUser.objects.get(username=username)
            old_pwd = user.password
            # 核心更新逻辑（和你验证过的一致）
            user.password = make_password(password)
            user.save(force_update=True)
            # 验证结果
            if user.check_password(password):
                self.stdout.write(self.style.SUCCESS(f'✅ 单个用户更新成功！'))
                self.stdout.write(f'用户名：{username}')
                self.stdout.write(f'旧密码：{old_pwd[:50]}...')
                self.stdout.write(f'新哈希：{user.password}')
            else:
                self.stdout.write(self.style.ERROR(f'❌ {username} 密码更新后校验失败！'))
        except SysUser.DoesNotExist:
            raise CommandError(f'❌ 用户 {username} 不存在！')
        except Exception as e:
            raise CommandError(f'❌ 单个用户更新失败：{str(e)}')

    def handle_batch_user(self, user_pwd_str: str):
        """批量修改用户密码（支持中文，修复编码报错）"""
        try:
            # 直接分割原生字符串
            user_pwd_list = [item.strip() for item in user_pwd_str.split(',') if item.strip()]
            if not user_pwd_list:
                raise CommandError('❌ 批量参数为空！示例："python222:123456,张三:654321"')

            self.stdout.write(self.style.SUCCESS('=== 批量更新开始 ==='))
            success = 0
            fail = []

            for idx, item in enumerate(user_pwd_list, 1):
                if ':' not in item:
                    fail.append(f'[{idx}] 格式错误：{item}（正确：用户名:密码）')
                    continue
                # 分割用户名和密码（仅分割一次，兼容密码含:）
                username, pwd = item.split(':', 1)
                username = username.strip()
                pwd = pwd.strip()

                try:
                    user = SysUser.objects.get(username=username)
                    old_pwd = user.password
                    user.password = make_password(pwd)
                    user.save(force_update=True)
                    # 校验
                    if user.check_password(pwd):
                        success += 1
                        self.stdout.write(f'[{idx}] ✅ {username} 更新成功（旧值：{old_pwd[:20]}...）')
                    else:
                        fail.append(f'[{idx}] ❌ {username} 更新后校验失败')
                except SysUser.DoesNotExist:
                    fail.append(f'[{idx}] ❌ {username} 用户不存在')
                except Exception as e:
                    fail.append(f'[{idx}] ❌ {username} 失败：{str(e)}')

            # 汇总
            self.stdout.write(self.style.SUCCESS(f'\n=== 批量更新汇总 ==='))
            self.stdout.write(f'成功：{success} 个 | 失败：{len(fail)} 个')
            if fail:
                self.stdout.write(self.style.ERROR('失败详情：'))
                for f in fail:
                    self.stdout.write(f'  {f}')
        except Exception as e:
            raise CommandError(f'❌ 批量更新失败：{str(e)}')

    def handle_update_all(self):
        """全库扫描明文密码并批量哈希（支持中文用户名）"""
        try:
            # 筛选所有明文密码用户
            all_users = SysUser.objects.all()
            plain_users = [u for u in all_users if self.is_plain_password(u.password)]
            total = len(plain_users)

            if total == 0:
                self.stdout.write(self.style.WARNING('⚠️  未找到明文密码用户，无需更新'))
                return

            # 二次确认（防止误操作）
            confirm = input(f'⚠️  检测到 {total} 个明文密码用户，是否确认更新？(y/n)：')
            if confirm.lower() != 'y':
                self.stdout.write(self.style.SUCCESS('✅ 已取消操作'))
                return

            self.stdout.write(self.style.SUCCESS('=== 全库明文密码更新开始 ==='))
            success = 0
            fail = []

            for user in plain_users:
                try:
                    old_pwd = user.password
                    # 直接使用原生明文密码生成哈希（PowerShell已传递正确编码）
                    user.password = make_password(old_pwd)
                    user.save(force_update=True)
                    # 校验
                    if user.check_password(old_pwd):
                        success += 1
                        self.stdout.write(f'✅ {user.username}（旧明文：{old_pwd} → 新哈希：{user.password[:20]}...）')
                    else:
                        fail.append(f'{user.username} 更新后校验失败')
                except Exception as e:
                    fail.append(f'{user.username} 失败：{str(e)}')

            # 汇总
            self.stdout.write(self.style.SUCCESS(f'\n=== 全库更新汇总 ==='))
            self.stdout.write(f'总明文用户：{total} | 成功：{success} | 失败：{len(fail)}')
            if fail:
                self.stdout.write(self.style.ERROR('失败详情：'))
                for f in fail:
                    self.stdout.write(f'  {f}')
        except Exception as e:
            raise CommandError(f'❌ 全库更新失败：{str(e)}')

    def handle_gen_hash(self, password: str):
        """仅生成单密码哈希（不写库，支持中文）"""
        try:
            hashed = make_password(password)
            self.stdout.write(self.style.SUCCESS('=== 仅生成哈希（不写库）==='))
            self.stdout.write(f'明文：{password} → 哈希：{hashed}')
        except Exception as e:
            raise CommandError(f'❌ 生成哈希失败：{str(e)}')

    def handle_gen_batch(self, passwords: str):
        """仅生成批量哈希（不写库，支持中文）"""
        try:
            pwd_list = [p.strip() for p in passwords.split(',') if p.strip()]
            if not pwd_list:
                raise CommandError('❌ 批量密码为空！示例："123456,管理员888,测试密码"')

            self.stdout.write(self.style.SUCCESS('=== 仅生成批量哈希（不写库）==='))
            for idx, pwd in enumerate(pwd_list, 1):
                hashed = make_password(pwd)
                self.stdout.write(f'[{idx}] 明文：{pwd} → 哈希：{hashed}')
        except Exception as e:
            raise CommandError(f'❌ 生成批量哈希失败：{str(e)}')

    def handle(self, *args, **options):
        """核心执行逻辑（子命令模式，避免参数冲突）"""
        command = options.get('command')

        # 无参数 → 输出帮助
        if not command:
            self.stdout.write(self.help)
            return

        # 分支1：修改单个用户
        if command == 'single':
            username = options['username']
            password = options['password']
            self.handle_single_user(username, password)

        # 分支2：批量修改用户
        elif command == 'batch':
            user_pwd_str = options['user_pwd_str']
            self.handle_batch_user(user_pwd_str)

        # 分支3：全库更新明文密码
        elif command == 'update-all':
            self.handle_update_all()

        # 分支4：仅生成单哈希
        elif command == 'gen-hash':
            password = options['password']
            self.handle_gen_hash(password)

        # 分支5：仅生成批量哈希
        elif command == 'gen-batch':
            passwords = options['passwords']
            self.handle_gen_batch(passwords)

        # 未知命令
        else:
            raise CommandError(f'❌ 未知命令：{command}，执行 python manage.py hash_password 查看帮助')