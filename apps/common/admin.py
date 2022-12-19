@property
def get_model_fields(class_obj):
    return [field.name for field in class_obj.model._meta.get_fields()]
