import unittest
import pandas as pd


def clean_events(df):
    """Apply the core CareFlow cleaning rules to a DataFrame."""
    df = df.copy()

    df = df.rename(columns={
        "case:concept:name": "case_id",
        "concept:name": "activity",
        "time:timestamp": "timestamp"
    })

    required = ["case_id", "activity", "timestamp"]
    missing = [col for col in required if col not in df.columns]

    if missing:
        raise ValueError(f"Required columns missing: {missing}")

    df["timestamp"] = pd.to_datetime(
        df["timestamp"], errors="coerce", utc=True
    )
    df["activity"] = df["activity"].astype("string").str.strip()

    df = df.drop_duplicates()

    invalid = (
        df["case_id"].isna()
        | df["activity"].isna()
        | df["timestamp"].isna()
    )

    excluded = df.loc[invalid].copy()
    cleaned = df.loc[~invalid].copy()

    cleaned = cleaned.sort_values(
        ["case_id", "timestamp"], kind="stable"
    ).reset_index(drop=True)

    return cleaned, excluded


class TestCareFlowCleaning(unittest.TestCase):

    def setUp(self):
        self.sample = pd.DataFrame({
            "case:concept:name": ["C1", "C1", "C2", None, "C2"],
            "concept:name": [
                " Registration ",
                " Registration ",
                " Discharge ",
                "Admission",
                None
            ],
            "time:timestamp": [
                "2025-01-02 10:00:00",
                "2025-01-02 10:00:00",
                "2025-01-01 09:00:00",
                "2025-01-01 08:00:00",
                "2025-01-03 09:00:00"
            ]
        })

    def test_column_names_are_standardized(self):
        cleaned, _ = clean_events(self.sample)
        self.assertTrue(
            {"case_id", "activity", "timestamp"}.issubset(cleaned.columns)
        )

    def test_exact_duplicates_are_removed(self):
        cleaned, _ = clean_events(self.sample)
        self.assertEqual(len(cleaned), 2)

    def test_missing_required_fields_are_excluded(self):
        cleaned, excluded = clean_events(self.sample)
        self.assertEqual(len(excluded), 2)
        self.assertEqual(len(cleaned), 2)

    def test_activity_whitespace_is_trimmed(self):
        cleaned, _ = clean_events(self.sample)
        self.assertTrue(
            cleaned["activity"].eq(cleaned["activity"].str.strip()).all()
        )

    def test_timestamps_are_parsed(self):
        cleaned, _ = clean_events(self.sample)
        self.assertTrue(
            isinstance(cleaned["timestamp"].dtype, pd.DatetimeTZDtype)
        )

    def test_events_are_sorted(self):
        cleaned, _ = clean_events(self.sample)

        keys = list(zip(cleaned["case_id"], cleaned["timestamp"]))
        self.assertEqual(keys, sorted(keys))

    def test_missing_required_column_raises_error(self):
        with self.assertRaises(ValueError):
            clean_events(pd.DataFrame({"case_id": ["C1"]}))


if __name__ == "__main__":
    unittest.main(verbosity=2)
