C:\Users\nikhilna\Documents\GitHub\FeedMe\start.py
set /P "GUID="

schtasks /create /XML C:\Users\nikhilna\Documents\GitHub\FeedMe\tasks\%GUID%.xml /tn FeedMe-%GUID% /ru NORTHAMERICA\nikhilna