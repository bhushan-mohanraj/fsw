# FSW

FSW is a collection of tools and guides for building apps with Flask, SQLAlchemy, and WTForms.

# Development

## To Do

- Update for WTForms 3 (released) and eventually SQLAlchemy 2 (not released).
- Add templates with macros like `render_fields` from `lawrenceville-math`.
    - For `render_fields`, see `greyli/bootstrap-flask`.
- Create guides about migrations and commands with `click`.
- When implementing CRUD views, use `request.view_args` instead of `**kwargs` for clarity.
- Extract `_CRUDBaseMixin._fill` to a separate helper function `_fill`.
- Add information about `pip` installation with `git` here.
- Use `model_instance` and `form_instance` instead of `model_object` and `form_object` when building CRUD views.
- Use `import wtforms` instead of `from wtforms import fields` and similarly.

## Before Commit

- Lint with `pylint`.
- Format with `black`.
