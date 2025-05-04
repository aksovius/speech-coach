import asyncio
import os
import subprocess
from pathlib import Path

from shared.logging import get_log_level, setup_logger

# Configure logger with Loki formatter
logger = setup_logger(
    name="bytewax",
    level=get_log_level(os.getenv("LOG_LEVEL", "INFO")),
    service=os.getenv("LOG_SERVICE", "speech-coach"),
    component="bytewax",
    use_loki=True,
)


async def run_workflow(workflow_name: str):
    """Run a single workflow with recovery settings"""
    recovery_dir = Path(f"recovery/{workflow_name}")
    recovery_dir.mkdir(parents=True, exist_ok=True)

    # Add bytewax directory to PYTHONPATH
    env = os.environ.copy()
    env["PYTHONPATH"] = f"{os.getcwd()}:{env.get('PYTHONPATH', '')}"

    cmd = [
        "python",
        "-m",
        "bytewax.run",
        f"bytewax.workflows.{workflow_name}:flow",  # Updated module path
        "-r",
        str(recovery_dir),
        "-s",
        "30",  # snapshot interval
        "-b",
        "60",  # batch size
    ]

    logger.info(
        f"Starting {workflow_name} flow",
        extra={
            "event": "flow_start",
            "flow": workflow_name,
            "recovery_dir": str(recovery_dir),
            "pythonpath": env["PYTHONPATH"],
            "command": " ".join(cmd),
        },
    )

    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=env,
    )

    # Log output in real-time
    while True:
        output = process.stdout.readline()
        if output == "" and process.poll() is not None:
            break
        if output:
            logger.info(
                output.strip(),
                extra={"event": "flow_output", "flow": workflow_name},
            )

    # Check for errors
    if process.returncode != 0:
        error = process.stderr.read()
        logger.error(
            f"Flow {workflow_name} failed",
            extra={
                "event": "flow_error",
                "flow": workflow_name,
                "error": error,
                "return_code": process.returncode,
            },
        )
        # Don't raise error for NoPartitionsError as it's expected on first run
        if "NoPartitionsError" not in error:
            raise RuntimeError(f"Flow {workflow_name} failed: {error}")


async def run_workflows():
    """Run all workflows in parallel"""
    logger.info("Starting Bytewax workflows", extra={"event": "startup"})

    try:
        # Run workflows in parallel
        await asyncio.gather(
            run_workflow("cleanup"),
            run_workflow("answer_ttr"),
        )
        logger.info("All workflows completed", extra={"event": "shutdown"})
    except Exception as e:
        logger.error(
            "Failed to run workflows",
            extra={
                "event": "error",
                "error": str(e),
            },
        )
        raise


if __name__ == "__main__":
    asyncio.run(run_workflows())
