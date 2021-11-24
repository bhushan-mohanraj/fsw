# FSW

FSW is a collection of tools and guides for building apps with Flask, SQLAlchemy, and WTForms.

# Development

## To Do

- Update for WTForms 3 (released) and SQLAlchemy 2 (not released).
- Use warning instead of error in `fsw.models.mixins.crud`.
- Rename `_CRUDBaseMixin` to `_BaseCRUDMixin` in `fsw.models.mixins.crud`.
- Rename `ModelMixin.from_model` to `ModelMixin.model_form` in `fsw.forms.mixins.model`.
- Change `exclude_names` parameter default argument to `None` in `ModelMixin.from_model`.
- Automatically adding a submit field in `ModelMixin.from_model` is problematic.
If a user wants to add extra fields to the model form, these fields are after the submit field.
Maybe, add a `ModelMixin.add_submit_field` classmethod instead.
- Add templates with macros like `render_fields` from `lawrenceville-math`.
- Create guides about migrations and commands with `click`.
- When implementing CRUD views, use `request.view_args` instead of `**kwargs` for clarity.
- Extract `_CRUDBaseMixin._fill` to a separate helper function `_fill`.
- Add information about `pip` installation with `git` here.
- Use `model_instance` and `form_instance` instead of `model_object` and `form_object` when building CRUD views.
