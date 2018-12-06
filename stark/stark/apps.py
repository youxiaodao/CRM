from django.apps import AppConfig


class StarkConfig(AppConfig):
    name = 'stark'

    # 写在这里，在Django启动之前就运行
    def ready(self):
        # 引入
        from django.utils.module_loading import autodiscover_modules
        autodiscover_modules('stark')
        # 在其他APP中添加stark.py，然后添加自己的代码，就会在程序启动前执行
