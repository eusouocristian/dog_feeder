from datetime import date, datetime

texto = "16:15"
dt = datetime.strptime(texto, "%H:%M")

if dt.hour == datetime.now().hour and dt.minute == datetime.now().minute:
    print("CKECHED")
