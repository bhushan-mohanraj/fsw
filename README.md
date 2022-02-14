# FSW

FSW is a collection of tools and guides for building apps with Flask, SQLAlchemy, and WTForms.

# Development

## To Do

- Update for WTForms 3 (released) and eventually SQLAlchemy 2 (not released).
- Add information about `pip` installation with `git` here.
- Create guides about migrations with `alembic` and commands with `click`.
- Use `import wtforms` instead of `from wtforms import fields` and similarly.
- Add templates with macros like `render_fields` from `lawrenceville-math`.
    - For `render_fields` with Bootstrap, see `greyli/bootstrap-flask`.
- When implementing CRUD views, use `request.view_args` instead of `**kwargs` for clarity.
- Use `model_instance` and `form_instance` instead of `model_object` and `form_object` when building CRUD views.
- For `ModelMixin`, use a dictionary of functions instead of `type()` equality checks.
- Use `import flask.views` rather than `from flask import views`.
- Add type annotations and fix `pylint` errors.

## Before Commit

- Lint with `pylint`.
- Format with `black`.
