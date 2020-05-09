def ping_info(number):
    try:
        number = float(number)
    except:
        return("Error, not a number.")      # This error should theoretically never be reached unless there is some serious error within the latest Discord.py API itself


    number = round(number, 0)           # 0 decimal places because the decimal values for latency information is considered irrelevant

    connection_quality = "Unknown"
    if number < 100.0 and number > 0.0:
        connection_quality = "Excellent"
    elif number >= 100.0 and number < 200.0:
        connection_quality = "Mediocre"
    elif number >= 200.0:
        connection_quality = "Very poor"
    elif number <= 0.0:             # This should theoretically be impossible, if connection quality is ever "Unknown" then there is something very wrong within the Discord.py implementation
        pass

    number = int(number)

    return(f"Pong!\nYour internet latency to Discord is {number} ms. {connection_quality} connection quality.")