from ...models.events import Event

def check_if_can_be_added(owner, start_date_time, end_date_time, venue, priority, is_all_day):
    # Define Your strategy here
    '''
    This is the sample strategy: if the user tries tries to add the event
    and there already exists some event which has higher priority than the
    event or its priority is HIGH, then, user will not be able to add this
    event.
    '''
    overlapping_events = Event.objects.filter(owner=owner,
                                             is_all_day=False,
                                             end_date_time__gt=start_date_time,
                                             start_date_time__lt=end_date_time)
    can_add = False
    overlapping_event_names_same = []
    overlapping_event_names_higher = []
    overlapping_event_names_lower = []
    warning = ""
    for event in overlapping_events:
        if priority== event.priority:
            overlapping_event_names_same.append(event.event_name) 
        elif event.priority > priority:
            overlapping_event_names_higher.append(event.event_name)
        else:
            overlapping_event_names_lower.append(event.event_name)

    if len(overlapping_event_names_higher) > 0:
        warning = "Event(s) with higher priority already exists!! Do you still want to add"
        # can add the names of the events afterwards
    elif len(overlapping_event_names_same) >0:
        warning = "Event(s) with same priority already exists. Are you sure you want to add the event?"
    elif len(overlapping_event_names_lower) >0:
        can_add=True
        warning = "Event is overlapped with low priority Event"
    else:
        can_add=True
        warning = "Event added successfully"
    return can_add, warning

def check_if_can_be_updated(owner, c_event, new_start_date_time, new_end_date_time, current_event_priority):
    # Define your strategy here
    # Define Your strategy here
    '''
    This is the sample strategy: if the user tries tries to add the event
    and there already exists some event which has higher priority than the
    event or its priority is HIGH, then, user will not be able to add this
    event.
    '''
    overlapping_events = Event.objects.filter(owner=owner,
                                             is_all_day=False,
                                             end_date_time__gt=new_start_date_time,
                                             start_date_time__lt=new_end_date_time,
                                             priority__gte=current_event_priority)
    can_add = False
    overlapping_event_names_same = []
    overlapping_event_names_higher = []
    warning = ""
    for event in overlapping_events:
        if event.id == c_event.id:
            continue
        if current_event_priority == event.priority:
            overlapping_event_names_same.append(event.event_name)
        elif event.priority > current_event_priority:
            # one should be able to update the priority of the event
            overlapping_event_names_higher.append(event.event_name)

    if len(overlapping_event_names_higher) > 0:
        
        warning = "Event(s) with higher priority already exists!! Do you still want to update?"
        # can add the names of the events afterwards
    elif len(overlapping_event_names_same) > 0:
        warning = "Event(s) with same priority already exists. Are you sure you want to update the event?"
    else:
        can_add= True
        warning = "Event updated successfully"

    return can_add, warning
