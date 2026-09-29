import os
import subprocess
import sys

from app.core.logging import logger


def run_migrations() -> None:
    """
    Run Alembic migrations before starting the API.
    """

    try:
        project_root = os.getcwd()

        if project_root not in sys.path:
            sys.path.insert(0, project_root)

        logger.info("Running Alembic migrations...")

        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "alembic",
                "upgrade",
                "head",
            ],
            cwd=project_root,
            capture_output=True,
            text=True,
            check=True,
        )

        if result.stdout:
            logger.info("Alembic output: %s", result.stdout)

        if result.stderr:
            logger.warning("Alembic stderr: %s", result.stderr)

        logger.info("Migrations completed successfully")

    except subprocess.CalledProcessError as e:
        logger.error("Migration failed")
        logger.error("stdout: %s", e.stdout)
        logger.error("stderr: %s", e.stderr)
        raise

    except Exception as e:
        logger.error("Unexpected error while running migrations: %s", e)
        raise
