def splitter(request, lst):
    if request.user_agent.is_mobile:
        num = 1
    elif request.user_agent.is_tablet:
        num = 2
    else:
        num = 3
    
    for i in range(0, len(lst), num):
        yield lst[i:i + num]