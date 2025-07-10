"""Validation checks for user and login datasets."""
import logging
import pandas as pd

logger = logging.getLogger(__name__)

def validate_user_visits(users_df: pd.DataFrame, logins_df: pd.DataFrame) -> None:
    login_count = (
        logins_df.groupby('username')
        .count()
        .reset_index()
        .rename(columns={'username': 'email', 'login_timestamp': 'login_count'})
    )
    users_login_count = users_df.merge(login_count, on='email', how='left').fillna({'login_count': 0})
    total_n = len(users_login_count)
    count_match = (users_login_count['website_visits_last_30_days'] == users_login_count['login_count']).sum()

    if total_n == count_match:
        logger.info("All visits match login count")
    elif count_match == 0:
        logger.error("No visits match login count")
    else:
        logger.warning("%0.2f%% match of visits to login count", 100 * count_match / total_n)

    return

def check_duplicates(df: pd.DataFrame, subset: list[str] = None, label: str = "data"):
    """
    Check for duplicate rows in a DataFrame.
    """
    if subset:
        dups = df.duplicated(subset=subset)
    else:
        dups = df.duplicated()

    num_dups = dups.sum()
    if num_dups > 0:
        logger.warning(f"{num_dups} duplicate rows found in {label}.")
    else:
        logger.info(f"No duplicates found in {label}.")
    return num_dups


def check_required_columns(df: pd.DataFrame, required: list[str], label: str = "data"):
    """
    Ensure required columns exist in the DataFrame.
    """
    missing = [col for col in required if col not in df.columns]
    if missing:
        logger.error(f"Missing required columns in {label}: {missing}")
    else:
        logger.info(f"All required columns present in {label}.")
    return missing


def validate_email_uniqueness(df: pd.DataFrame, label: str = "users"):
    """
    Ensure no duplicate email addresses.
    """
    if 'email' not in df.columns:
        logger.warning(f"No 'email' column in {label} to validate uniqueness.")
        return None

    num_dups = df.duplicated(subset=['email']).sum()
    if num_dups > 0:
        logger.warning(f"{num_dups} duplicate emails found in {label}.")
    else:
        logger.info(f"All emails in {label} are unique.")
    return num_dups