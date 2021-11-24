# Changes

## Version 0.2.2

- Add `__init__.py` files for packages.

## Version 0.2.1

- Add back `IDMixin` and `ClassNameMixin`.
- Add `__init__.py` to fix package bug.

## Version 0.2.0

- Add `CRUDMixin` for models.
- Remove `IDMixin` and `ClassNameMixin`.

## Version 0.1.1

- Use `secrets.token_hex` instead of `os.urandom` in `CSRFMixin` for CSRF secret.

## Version 0.1.0

- Add `CSRFMixin` to add CSRF protection to WTForms forms.
- Add `ModelMixin` to create forms directly from SQLAlchemy models based on their columns.
- Add `IDMixin` and `ClassNameMixin` for models.
