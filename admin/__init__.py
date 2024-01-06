from admin.users import UserAdmin
from admin.links import ShortLinkAdmin, UserShortLinkAdmin


def init_admin_page(admin_app):
    """ Register in admin Page /Model Admin classes/ """
    admin_models = (UserAdmin,
                    ShortLinkAdmin,
                    UserShortLinkAdmin
                    )

    for model_view in admin_models:
        admin_app.add_view(model_view)
