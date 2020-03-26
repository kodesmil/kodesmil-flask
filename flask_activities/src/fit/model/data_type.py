class Type:
    activity = 'activity'
    steps = 'steps'
    active_minute = 'active_minute'
    distance = 'distance'
    heart_minute = 'heart_minute'


class DataType:
    class ActiveMinute:
        data_type_name = "com.google.active_minutes"
        data_type_name_summary = "com.google.active_minutes"
        model_type = Type.active_minute

    class HeartMinute:
        data_type_name = "com.google.heart_minutes"
        data_type_name_summary = "com.google.heart_minutes.summary"
        model_type = Type.heart_minute
        

    class ActivitySegment:
        data_type_name = "com.google.activity.segment"
        data_type_name_summary = "com.google.activity.summary"
        model_type = Type.activity

    class Distance:
        data_type_name = "com.google.distance.delta"
        data_type_name_summary = "com.google.distance.delta"
        model_type = Type.distance

    class Steps:
        data_type_name = "com.google.step_count.delta"
        data_type_name_summary = "com.google.step_count.delta"
        model_type = Type.steps
