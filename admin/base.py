from typing import Type

from wtforms import Form
from sqladmin import Admin
from sqladmin.models import ModelView
from starlette.requests import Request
from starlette.responses import Response
from starlette.exceptions import HTTPException
from sqladmin.authentication import login_required


class CustomAdmin(Admin):

    def _calculate_mapping_key_pair(self, model, child_model):
        """
            Calculate mapping property key pair between `model` and inline model,
                including the forward one for `model` and the reverse one for inline model.
                Override the method to map your own inline models.
        """
        mapper = model._sa_class_manager.mapper

        # Find property from target model to current model
        # Use the base mapper to support inheritance
        target_mapper = child_model._sa_class_manager.mapper.base_mapper

        reverse_prop = None

        for prop in target_mapper.iterate_properties:
            if (hasattr(prop, 'direction') and prop.direction.name in ('MANYTOONE', 'MANYTOMANY') and
                    issubclass(model, prop.mapper.class_)):
                reverse_prop = prop
                break
        else:
            raise Exception(f'Cannot find reverse relation for model {child_model}')

        # Find forward property
        forward_prop = None

        candidate = 'ONETOMANY' if prop.direction.name == 'MANYTOONE' else 'MANYTOMANY'

        for prop in mapper.iterate_properties:
            if (hasattr(prop, 'direction') and prop.direction.name == candidate and
                    prop.mapper.class_ == target_mapper.class_):
                forward_prop = prop
                break
        else:
            raise Exception(f'Cannot find forward relation for model {model}')

        return forward_prop.key, reverse_prop.key

    def _find_model_view(self, identity: str) -> ModelView:
        for view in self.views:
            if isinstance(view, ModelView) and (view.identity == identity or view.model == identity):
                return view
        raise HTTPException(status_code=404)

    @login_required
    async def details(self, request: Request) -> Response:
        """Details route."""

        await self._details(request)

        model_view = self._find_model_view(request.path_params["identity"])

        model = await model_view.get_object_for_details(request.path_params["pk"])
        if not model:
            raise HTTPException(status_code=404)

        inline_views = []
        for model_name, fields in model_view.inline_models:
            inline_model = self._find_model_view(model_name)
            model_relation, _ = self._calculate_mapping_key_pair(model.__class__, model_name)
            inline_objects = getattr(model, model_relation)
            inline_views.append({
                'model': inline_model,
                'objects': inline_objects,
                'fields': fields
            })

        context = {
            "request": request,
            "model_view": model_view,
            "model": model,
            "title": model_view.name,
            "inline_views": inline_views
        }

        return self.templates.TemplateResponse(model_view.details_template, context)


class AuthModelView(ModelView):
    inline_models = []

    def is_accessible(self, request) -> bool:
        if user := request.session.get("user"):
            return user["is_active"] and user["is_superuser"]
        return False

    def is_visible(self, request) -> bool:
        if user := request.session.get("user"):
            return user["is_active"] and user["is_superuser"]
        return False

    async def scaffold_form(self) -> Type[Form]:
        """Fix form with multipart"""

        form = await super().scaffold_form()
        form.has_file_field = (
            self.has_file_field if hasattr(self, "has_file_field") else False
        )
        return form
