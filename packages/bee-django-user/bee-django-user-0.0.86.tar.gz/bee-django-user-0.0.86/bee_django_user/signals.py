# -*- coding:utf-8 -*-
__author__ = 'bee'
from django.dispatch import Signal

# 费用审核后的信号
update_user_expire_signal = Signal(providing_args=["leave_record"])

# 禁用/暂停/恢复用户的信号
update_user_active_pause_signal = Signal(providing_args=["user","active","pause","info"])

create_user_signal = Signal(providing_args=["user"])

#转班后的信号
add_user_class_remove_record = Signal(providing_args=["user","info"])