# AGENTS.md – Campaigns App Maintenance Guide

> **Purpose:** This file provides context and instructions for AI agents (LLMs) maintaining the `campaigns` Django app. It complements project-wide rules in `CURSOR.md` and focuses on app-specific architecture, conventions, and workflows.

---

## 1. Architecture Overview

### Domain Model

```
Campaign (1) ──────────────< (N) Setting
```

- **Campaign**: Marketing/event sales campaign with pricing and timing.
- **Setting**: Configuration per campaign (max price, enabled flag). One campaign has many settings.

### Key Relationships

- `Setting.campaign` → `ForeignKey(Campaign, on_delete=CASCADE)`
- Reverse access: `campaign.setting_set.all()` (Django default, no custom `related_name`)

### Stack

- **Framework:** Django 6.x + Django REST Framework
- **Auth:** JWT via `rest_framework_simplejwt`
- **Docs:** OpenAPI via `drf-spectacular`

---

## 2. File Map

| File | Purpose |
|------|---------|
| `models.py` | `Campaign`, `Setting` models |
| `serializers.py` | `CampaignSerializer`, `SettingSerializer` |
| `views.py` | `CampaignViewSet`, `SettingViewSet` |
| `urls.py` | DRF router for `/api/campaigns/campaign/` and `/api/campaigns/setting/` |
| `admin.py` | Admin for Campaign (with Setting inline) and Setting |
| `tests.py` | Model, serializer, and API tests |

---

## 3. API Structure

### Base URL

- Mounted at: `/api/campaigns/` (see `entities/urls.py`)

### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/campaigns/campaign/` | List campaigns |
| POST | `/api/campaigns/campaign/` | Create campaign |
| GET | `/api/campaigns/campaign/{id}/` | Retrieve campaign (with nested settings) |
| PUT/PATCH | `/api/campaigns/campaign/{id}/` | Update campaign |
| DELETE | `/api/campaigns/campaign/{id}/` | Delete campaign (cascades to settings) |
| GET | `/api/campaigns/setting/` | List settings |
| POST | `/api/campaigns/setting/` | Create setting |
| GET/PUT/PATCH/DELETE | `/api/campaigns/setting/{id}/` | CRUD for setting |

### Serialization

- **CampaignSerializer**: `id`, `name`, `override_price`, `start_date`, `settings` (read-only nested list)
- **SettingSerializer**: `id`, `max_price`, `enabled`, `campaign`
- Nested `settings` use `source="setting_set"` (Django default reverse name)

---

## 4. Conventions for Modifications

### Models

- Add docstrings for models and fields.
- Use `DecimalField` for money (`max_digits`, `decimal_places`).
- Run `python manage.py makemigrations` after changes.
- Keep migrations reversible when possible.

### Serializers

- Use `ModelSerializer` unless custom logic is needed.
- For nested relations, use `source` to match Django’s reverse relation name.
- Mark nested fields as `read_only=True` when they are not writable.

### ViewSets

- Use `@extend_schema` / `@extend_schema_view` from `drf-spectacular` for OpenAPI.
- Tag endpoints with `tags=["Campaigns"]` or `tags=["Settings"]`.
- Document auth requirements in schema descriptions.

### Code Style

- Follow `CURSOR.md`: no inline comments, descriptive names, docstrings in English.
- Use absolute imports for clarity; relative imports only within the same package.

---

## 5. Common Maintenance Tasks

### Add a new field to Campaign

1. Add field in `models.py`.
2. Run `makemigrations campaigns`.
3. Add field to `CampaignSerializer.Meta.fields`.
4. Add `@extend_schema`/OpenAPI docs if needed.
5. Update `admin.py` `list_display` if relevant.
6. Add or update tests.

### Add a new field to Setting

1. Add field in `models.py`.
2. Run `makemigrations campaigns`.
3. Add field to `SettingSerializer.Meta.fields`.
4. Update `admin.py` `list_display` if relevant.
5. Add or update tests.

### Add a new endpoint or filter

1. Extend the appropriate ViewSet or add a new one.
2. Register in `urls.py` router.
3. Add `@extend_schema`/OpenAPI docs.
4. Add tests.

### Change the reverse relation name

- If `related_name` is added to `Setting.campaign`, update `CampaignSerializer` `source` accordingly (e.g. `source="settings"`).

---

## 6. Debugging

### Common issues

| Issue | Likely cause | Fix |
|-------|--------------|-----|
| `AttributeError: 'Campaign' has no attribute 'settings'` | Using wrong reverse name | Use `setting_set` |
| 401 on API calls | Missing JWT | Use `Authorization: Bearer <token>` |
| Serializer validation errors | Wrong field types or missing required fields | Check payload vs schema |
| Migration conflicts | Out-of-order migrations | Run `migrate` and resolve conflicts |

### Useful commands

```bash
# Run migrations
python manage.py migrate

# Create test data
python create_test_data.py

# Run tests
python manage.py test campaigns

# Validate schema
python manage.py spectacular --file schema.yml
```

---

## 7. Testing

- Tests live in `campaigns/tests.py`.
- Run tests before committing significant changes.
- Use JWT auth when testing protected endpoints.
- Add tests for new models, serializers, and views.

---

## 8. OpenAPI

- Schema: `/api/schema/`
- Swagger UI: `/api/docs/`
- ReDoc: `/api/redoc/`

Keep `@extend_schema` / `@extend_schema_view` in sync with actual behavior when changing endpoints.

---

## 9. Dependencies

- `django`, `djangorestframework`, `djangorestframework-simplejwt`, `drf-spectacular`
- See `requirements.txt` or `pyproject.toml` for versions.

---

## 10. References

- Project rules: `CURSOR.md`
- Session log: `C.md`
- Project overview: `README.md`
- Django admin: `/admin/`
