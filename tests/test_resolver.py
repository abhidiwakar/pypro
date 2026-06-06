from pathlib import Path

import pytest

from project_initializer.config import Database, ProjectConfig, ProjectType, ToolingOptions
from project_initializer.errors import PackError
from project_initializer.pack import PackManifest, resolve_packs


def _config(project_type: ProjectType, *, sqlalchemy: bool = False, alembic: bool = False):
    return ProjectConfig(
        project_name="Customer API",
        project_slug="customer-api",
        package_name="customer_api",
        target_dir=Path("customer-api"),
        project_type=project_type,
        database=Database.POSTGRESQL,
        tooling=ToolingOptions(use_docker=True, use_pytest=True, use_ruff=True),
        use_sqlalchemy=sqlalchemy,
        use_alembic=alembic,
    )


def test_resolve_fastapi_sqlalchemy_alembic_packs():
    packs = resolve_packs(_config(ProjectType.FASTAPI, sqlalchemy=True, alembic=True))

    assert [pack.name for pack in packs] == [
        "common",
        "fastapi",
        "database_postgres",
        "orm_sqlalchemy",
        "migrations_alembic",
        "tooling_pytest",
        "tooling_ruff",
        "docker",
    ]


def test_resolve_django_drf_packs():
    packs = resolve_packs(_config(ProjectType.DJANGO_DRF))

    assert [pack.name for pack in packs] == [
        "common",
        "django",
        "django_drf",
        "database_postgres",
        "tooling_pytest",
        "tooling_ruff",
        "docker",
    ]


def test_validate_pack_conflict():
    with pytest.raises(PackError, match="conflicts with selected pack"):
        resolve_packs(
            _config(ProjectType.DJANGO),
            available_packs={
                "common": PackManifest(name="common"),
                "django": PackManifest(name="django", conflicts=("fastapi",)),
                "fastapi": PackManifest(name="fastapi", conflicts=("django",)),
            },
            explicit_names=["common", "django", "fastapi"],
        )


def test_resolve_respects_empty_available_packs():
    with pytest.raises(PackError, match="Required pack 'common' is not available"):
        resolve_packs(_config(ProjectType.FASTAPI), available_packs={})


def test_resolve_respects_empty_explicit_names():
    assert resolve_packs(_config(ProjectType.FASTAPI), explicit_names=[]) == []


def test_validate_pack_requires_selected_pack():
    with pytest.raises(PackError, match="requires pack 'missing'"):
        resolve_packs(
            _config(ProjectType.FASTAPI),
            available_packs={
                "common": PackManifest(name="common", requires=("missing",)),
            },
            explicit_names=["common"],
        )
