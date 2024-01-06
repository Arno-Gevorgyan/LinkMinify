from admin.base import AuthModelView
from db.models._links import ShortLinkModel, UserShortLinkModel


class ShortLinkAdmin(AuthModelView, model=ShortLinkModel):
    name = "Link"
    name_plural = "Links"
    icon = "fa-solid fa-link"

    form_columns = [
        ShortLinkModel.full_url,
        ShortLinkModel.short_url,
    ]

    column_list = [
        ShortLinkModel.short_url,
        ShortLinkModel.created_at,
    ]

    column_details_list = [
        ShortLinkModel.full_url,
        ShortLinkModel.short_url,
    ]

    column_sortable_list = [
        ShortLinkModel.created_at,
    ]


class UserShortLinkAdmin(AuthModelView, model=UserShortLinkModel):
    name = "User Link"
    name_plural = "User Links"
    icon = "fa-solid fa-person-walking-dashed-line-arrow-right"

    form_columns = [
        UserShortLinkModel.user,
        UserShortLinkModel.short_link,
    ]

    column_list = [
        UserShortLinkModel.user,
        UserShortLinkModel.short_link,
        UserShortLinkModel.created_at,
    ]

    column_details_list = [
        UserShortLinkModel.user,
        UserShortLinkModel.short_link,
        UserShortLinkModel.created_at,
    ]

    column_sortable_list = [
        UserShortLinkModel.created_at,
    ]
