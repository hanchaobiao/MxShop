from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'
    # xadmin 一级菜单为中文， settings 中引apps是需使用 'user_operation.apps.UserOperationConfig'
    verbose_name = '用户管理'

    def ready(self):
        # 引入信号量
        import users.signals
