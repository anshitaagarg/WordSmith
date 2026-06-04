import pandas as pd
from datetime import datetime
import os

HISTORY_FILE = "history/translations.csv"


def save_translation(source, target, original, translated):

    new_record = pd.DataFrame([
        {
            "Timestamp": datetime.now(),
            "Source": source,
            "Target": target,
            "Original Text": original,
            "Translated Text": translated
        }
    ])

    if os.path.exists(HISTORY_FILE):
        existing = pd.read_csv(HISTORY_FILE)
        updated = pd.concat([existing, new_record], ignore_index=True)
    else:
        updated = new_record

    updated.to_csv(HISTORY_FILE, index=False)


def load_history():

    if os.path.exists(HISTORY_FILE):
        return pd.read_csv(HISTORY_FILE)

    return pd.DataFrame()