from datetime import date, datetime

from dateutil.relativedelta import relativedelta
from googleapiclient.discovery import build

from .model.data_type import DataType
from .model.source import Source


def get_data(credentials, user, data_type):
    output = []
    today = date.today()
    start_date = today - relativedelta(days=60, hour=00, minute=00, second=00)
    end_date = today - relativedelta(second=0)
    data_source_id = None
    data = search(credentials, data_type.data_type_name, data_source_id, start_date, end_date)
    for bucket in data["bucket"]:
        for data_set in bucket["dataset"]:
            points = data_set["point"]
            for point in points:
                if "dataTypeName" in point and point["dataTypeName"] == data_type.data_type_name_summary:
                    start_time = datetime.fromtimestamp(int(int(point["startTimeNanos"]) / 1000000000))
                    end_time = datetime.fromtimestamp(int(int(point["endTimeNanos"]) / 1000000000))
                    output.append({
                        '_user_id': user['_id'],
                        'registered_from': start_time.isoformat(),
                        'registered_to': end_time.isoformat(),
                        'value': point['value'][0]['fpVal'],
                        'source': Source.google_fit,
                        'type': data_type.model_type,
                    })
    return output


def get_heart_minutes(credentials, user):
    return get_data(credentials, user, DataType.HeartMinute)


def get_activity_minutes(credentials, user):
    return get_data(credentials, user, DataType.ActiveMinute)


def get_distances(credentials, user):
    return get_data(credentials, user, DataType.Distance)


def search(credentials, data_type_name, data_source_id, start, end, bucket_by_time=86400000):
    google_fit = build('fitness', 'v1', credentials=credentials)
    # Convert to nanoseconds
    start_id = int(start.timestamp() * 1000.0)
    end_id = int(end.timestamp() * 1000.0)

    # Go get the data!
    data = google_fit.users().dataset().aggregate(
        userId="me",
        body={
            "aggregateBy": [{
                "dataTypeName": data_type_name,
                "dataSourceId": data_source_id
            }],
            "bucketByTime": {"durationMillis": bucket_by_time},  # One day = 86400000
            "startTimeMillis": start_id,
            "endTimeMillis": end_id
        }).execute()
    return data
