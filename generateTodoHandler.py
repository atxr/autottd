with open("autottdTodoHandlerTemplate.py") as templatefd:
    template = templatefd.read()

with open("logonTemplate.ps1") as logonfd:
    logon = logonfd.read()   

with open("autottdTodoHandler.py", "w") as handlerfd:
    handlerfd.write(template.replace("REPLACE_LOGON", logon))

