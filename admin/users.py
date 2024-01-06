from admin.forms import UserForm
from admin.base import AuthModelView
from db.models._users import UserModel


class UserAdmin(AuthModelView, model=UserModel):
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user"

    form_columns = [
        UserModel.first_name,
        UserModel.last_name,
        UserModel.email,
        UserModel.is_active,
        UserModel.is_superuser,
    ]

    form_base_class = UserForm

    column_list = [
        UserModel.first_name,
        UserModel.last_name,
        UserModel.email,
        UserModel.is_active,
        UserModel.created_at,
    ]

    column_details_list = [
        UserModel.first_name,
        UserModel.last_name,
        UserModel.email,
        UserModel.is_active,
        UserModel.is_superuser,
        UserModel.created_at,
        UserModel.updated_at,
    ]

    column_searchable_list = [
        UserModel.first_name,
        UserModel.last_name,
        UserModel.email,
    ]

    column_sortable_list = [
        UserModel.first_name,
        UserModel.last_name,
        UserModel.email
    ]

