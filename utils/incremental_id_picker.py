def increment_id_number(model, field:str, digit=10)-> str:
    """
    Function to generate incrementing fixed digit IDs.
    
    parameters
    ------
    model : models.Model
        The model containing incrementing attribute
    
    field : str
        the field that is incrementing
    
    digit: int, optional
        Number of digits of the field
    """
    last = model.objects.all().order_by('id').last()
    if not last:
        return '1' + ("0" * (digit-2)) + '1'

    id = last.__dict__[field]
    new_id = int(id)
    new_id = new_id + 1
    new_id = str(new_id)
    return new_id