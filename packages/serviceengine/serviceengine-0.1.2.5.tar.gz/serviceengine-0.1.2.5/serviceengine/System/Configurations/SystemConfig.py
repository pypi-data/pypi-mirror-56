SystemConfig = {
  "Logger": {
    "LogToFile": {
      "all": True,
      "System": True,
      "Info": True,
      "Debug": True,
      "Warn": True,
      "Error": True
    },
    "Display": {
      "all": True,
      "System": True,
      "Info": True,
      "Debug": True,
      "Warn": True,
      "Error": True
    },
    "LogFilePath": {
      "Windows": "Logs",
      "Linux": "Logs"
    },
    "LogFileForEachContext": True
  },
  "Async": {
    "threadPoolSize": 5
  },
  "ShellCommands": {
    "Ping": {
      "PingTimes": 4
    }
  }
}