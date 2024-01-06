from admin.users import UserAdmin


def init_admin_page(admin_app):
    """ Register in admin Page /Model Admin classes/ """
    admin_models = (UserAdmin,
                    )

    for model_view in admin_models:
        admin_app.add_view(model_view)
