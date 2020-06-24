from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test


def client_required(function=None,redirect_field_name=REDIRECT_FIELD_NAME,login_url='login'):
    actual_decorator=user_passes_test(
        lambda u: u.is_active and u.user_type==1,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )

    if function:
        return actual_decorator
    return actual_decorator


def writer_required(function=None,redirect_field_name=REDIRECT_FIELD_NAME,login_url='login'):
    actual_decorator=user_passes_test(
        lambda u: u.is_active and u.user_type==2,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )

    if function:
        return actual_decorator
    return actual_decorator


def admin_required(function=None,redirect_field_name=REDIRECT_FIELD_NAME,login_url='login'):
    actual_decorator=user_passes_test(
        lambda u: u.is_active and u.user_type==3,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )

    if function:
        return actual_decorator
    return actual_decorator







