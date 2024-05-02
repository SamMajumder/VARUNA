
library(shiny.exe)
library(here)

shiny.exe(appName = "VARUNA", port = 3838,host = 'public',  
          appDir = here::here())

