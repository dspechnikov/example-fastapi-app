import os
from importlib import import_module
from logging.config import fileConfig
from typing import Optional, cast

from alembic import context
from alembic.context import config
from dotenv import dotenv_values
from sqlalchemy import MetaData, engine_from_config, pool


class Options:
    """Custom options in Alembic config file."""

    BASE_MODEL = "base_model"
    DATA_MODELS = "data_models"


def get_main_option_with_env(option_name: str) -> Optional[str]:
    """Substitute environment variables in an option from Alembic config main section.
    I.e. url={URL_ENVIRONMENT_VARIABLE}.

    Supports following sources (ordered by precedence):
        - .env file in the root of the project
        - shell environment variables
    """

    if not (option_value := config.get_main_option(option_name)):
        return None

    return option_value.format(
        **{
            **dotenv_values(),
            **os.environ,
        }
    )


def run_migrations_offline(target_metadata: Optional[MetaData]) -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL and not an Engine, though an Engine is
    acceptable here as well.  By skipping the Engine creation we don't even need a DBAPI
    to be available.

    Calls to context.execute() here emit the given string to the script output.
    """
    context.configure(
        url=get_main_option_with_env("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        transaction_per_migration=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online(target_metadata: Optional[MetaData]) -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine and associate a connection with the
    context.
    """
    connectable = engine_from_config(
        # cast to pass type check. get_section returns dict(), so it should be safe
        cast(dict[str, str], config.get_section(config.config_ini_section, {})),
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            transaction_per_migration=True,
        )

        with context.begin_transaction():
            context.run_migrations()


def autogenerate_required() -> bool:
    """Check whether migration auto-generation is required.

    The main use case is `alembic revision --autogenerate` command. Some commands like
    alembic check use this as well.
    """
    # in some cases (i.e. alembic check command) autogenerate is not present as command
    # line option and cannot be checked with config.cmd_opts.autogenerate, use
    # environment context proxy instead. _proxy is core attribute for environment
    # context. so getting the option from revision_context should be reliable enough.
    # also ignore mypy errors, because _proxy is added to context module dynamically.
    revision_context = context._proxy.context_opts.get(  # type: ignore[attr-defined]
        "revision_context"
    )

    return (
        # explicit cast to indicate actual type for mypy
        cast(bool, revision_context.command_args.get("autogenerate", False))
        if revision_context
        else False
    )


def get_base_model_metadata() -> MetaData:
    """Get SQLAlchemy base model metadata from the class path specified in config.

    Required for migration auto-generation to work.
    """
    if not (base_model := config.get_main_option(Options.BASE_MODEL)):
        raise ValueError(
            f"For auto generation to work, path to base model must be "
            f"specified in `{Options.BASE_MODEL}` option."
        )

    try:
        base_model_module_path, base_model_name = base_model.rsplit(".", 1)
    except ValueError as e:
        raise ValueError(f"{base_model=} doesn't look like an object path") from e

    try:
        # explicit cast to indicate actual type for mypy
        return cast(
            MetaData,
            getattr(import_module(base_model_module_path), base_model_name).metadata,
        )
    except (ImportError, AttributeError) as e:
        raise ValueError(f"Could not find {base_model=}") from e


def import_child_models() -> None:
    """Import SQLAlchemy child models listed in Alembic config.

    Required for migration auto-generation to work.
    """
    if not (data_models := config.get_main_option(Options.DATA_MODELS)):
        raise ValueError(
            f"For auto generation to work, paths to base model must be "
            f"specified in `{Options.DATA_MODELS}` option."
        )

    for model_module in data_models.split(","):
        try:
            import_module(model_module)
        except ImportError as e:
            raise ValueError(f"Could not import {model_module=}") from e


def run_migrations() -> None:
    """Prepare migration environment and run migrations."""
    # expand env variables in database URL to avoid credentials in alembic config.
    # update URL in config to be able to get expanded URL directly from it
    if database_url := get_main_option_with_env("sqlalchemy.url"):
        config.set_main_option("sqlalchemy.url", database_url)

    # interpret the config file for Python logging
    if config.config_file_name is not None:
        fileConfig(config.config_file_name)

    target_metadata = None
    if autogenerate_required():
        # to auto-generate migrations, alembic needs:
        # - path to base model metadata
        # - import model classes to fill base model metadata
        target_metadata = get_base_model_metadata()
        import_child_models()

    # run migrations
    if context.is_offline_mode():
        run_migrations_offline(target_metadata)
    else:
        run_migrations_online(target_metadata)


run_migrations()
