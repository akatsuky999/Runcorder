from datetime import datetime


class DatabaseHandler:
    @staticmethod
    def add_training_record(runner, date, distance, pace, assessment, morning_run):
        data = runner._load_data()
        data["training_records"][date] = {
            "distance": float(distance),
            "pace": float(pace),
            "assessment": assessment,
            "morning_run": morning_run.lower() == "y"
        }
        runner._save_data(data)

    @staticmethod
    def add_training_mode(runner, date, mode):
        data = runner._load_data()
        data["training_modes"][date] = mode
        runner._save_data(data)

    @staticmethod
    def get_sorted_dates(data):
        return sorted(data.keys(), key=lambda x: datetime.strptime(x, "%Y-%m-%d"))