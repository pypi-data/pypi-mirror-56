import asyncio
from tqdm import tqdm
from jsonschema import validate
from jsonschema.exceptions import ValidationError
import ddmonitoring.utils.constants as const

def setup_background_jobs(scheduler, model):
    """Configure background jobs for the HTTP requests"""
    check_data = model.check_data

    def configure_metrics_job(run_interval, data_interval):
        scheduler.add_job(
            model.make_global_metrics,
            trigger=None,
            args=[data_interval]
        )
        scheduler.add_job(
            model.make_global_metrics,
            'interval',
            seconds=run_interval,
            args=[data_interval]
        )

    for website in check_data:
        intervals = check_data[website]
        for check_interval in intervals:
            scheduler.add_job(
                model.check,
                trigger=None,
                args=[website, const.DATA_INTERVAL_SHORT]
            )
            scheduler.add_job(
                model.check,
                trigger='interval',
                seconds=check_interval,
                args=[website, check_interval]
            )
    #every 10s compute metrics for last 10 minutes of data (to be displayed)
    configure_metrics_job(run_interval=const.REFRESH_SHORT, data_interval=const.DATA_INTERVAL_SHORT)

    #every minute compute metrics for last hour of data (to be displayed)
    configure_metrics_job(run_interval=const.REFRESH_LONG, data_interval=const.DATA_INTERVAL_LONG)

    #every 10s compute metrics for the last 2 minutes of data (for the alerts!)
    configure_metrics_job(run_interval=const.REFRESH_SHORT, data_interval=const.ALERTS_INTERVAL)

async def populate_metrics_data(model, user_data):
    """Used to make the first requests before drawing the UI"""
    loop = asyncio.get_event_loop()
    futures = [
        loop.run_in_executor(
            None,
            model.check,
            website,
            const.DATA_INTERVAL_SHORT
        )
        for website in user_data
    ]
    for _ in tqdm(asyncio.as_completed(futures), total=len(futures)):
        await _

def validate_input(user_data, logger):
    """Validate input data from JSON file against the required template"""
    url_mask = r"^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$"
    success = False

    input_file_schema = {
        "type": "object",
        "patternProperties": {
            url_mask: {
                "type": "array",
                "items": {
                    "type": "number",
                    "minimum": const.FASTEST_REQUEST_TIME
                }
            }
        },
        "additionalProperties": False
    }
    try:
        validate(user_data, input_file_schema)
    except ValidationError as valid_err:
        logger.warning("The input file format is wrong. Reason: %s. \
            Reminder: the configuration JSON file must be a single JSON object,\
            with each key being the website's URL you want to check, and each value being an array \
            of check intervals in seconds, greater than 2 seconds.", valid_err.message)
    else:
        logger.debug("Valid JSON input file")
        success = True

    if not user_data:
        logger.warning("Please provide a non empty json file.")
        success = False
    return success
