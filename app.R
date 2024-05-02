

library(reticulate)
library(here)
library(terra)
library(sf)
library(RColorBrewer)
library(leaflet)
library(tidyverse)
library(shiny)
library(shinyWidgets)
library(htmlwidgets)
library(leaflet.providers)


# Use the created virtual environment
use_virtualenv("VARUNA", required = TRUE)

here::here("utils.py") 

## source the python script
source_python(here::here("utils.py")) 

## source R functions 
source(here::here("R-functions.R"))

####### 
## grabbing all the country names from the shapefile 
###

countries <- sf::read_sf(here::here("Data","Shapefile",
                                    "World_Countries_Generalized.shp"))


country_list <- countries %>% 
                 sf::st_drop_geometry() %>%
                 dplyr::select("COUNTRY")



########## 
#### 


ui <- fluidPage(
  titlePanel("V.A.R.U.N.A. - Visual Analyzer for Regional Understanding of Numerical Atmospheric forecasts"),
  sidebarLayout(
    sidebarPanel(
      selectInput("country", "Select region around a country:", choices = country_list$COUNTRY),
      textInput("startYear", "Start Year:", value = "2025"),
      textInput("endYear", "End Year:", value = "2026"),
      selectInput("model", "Climate Model:", choices = c("ACCESS-CM2","ACCESS-ESM1-5","BCC-CSM2-MR","CanESM5","CESM2-WACCM",
                                                         "CESM2","CMCC-CM2-SR5","CMCC-ESM2","CNRM-CM6-1",
                                                         "CNRM-ESM2-1","EC-Earth3-Veg-LR","EC-Earth3","FGOALS-g3",
                                                         "GFDL-CM4","GFDL-CM4_gr1","GFDL-ESM4","GISS-E2-1-G",
                                                         "HadGEM3-GC31-LL","HadGEM3-GC31-MM","IITM-ESM","INM-CM4-8",
                                                         "INM-CM5-0","IPSL-CM6A-LR","KACE-1-0-G","KIOST-ESM",
                                                         "MIROC-ES2L","MIROC6","MPI-ESM1-2-HR","MPI-ESM1-2-LR",
                                                         "MRI-ESM2-0","NESM3","NorESM2-LM","NorESM2-MM","TaiESM1",
                                                         "UKESM1-0-LL")),
      selectInput("variable", "Climate Variable:", choices = c("tas","tasmax", "tasmin", 
                                                               "pr","hurs","huss","rlds",
                                                               "rsds","sfcWind")),
      actionButton("submit", "Submit"),
      uiOutput("dynamicSlider"),  # UI placeholder for dynamically generated slider
      helpText("Use the slider to select different time layers for visualization.")
    ),
    mainPanel(
      tabsetPanel(type = "tabs",
                  tabPanel("SSP 126", leafletOutput("map_ssp126", height = 600)),
                  tabPanel("SSP 245", leafletOutput("map_ssp245", height = 600)),
                  tabPanel("SSP 370", leafletOutput("map_ssp370", height = 600)),
                  tabPanel("SSP 585", leafletOutput("map_ssp585", height = 600)),
                  tabPanel("About V.A.R.U.N.A.", 
                           h3("About V.A.R.U.N.A."),
                           p("V.A.R.U.N.A., named after the Hindu deity of sky, ocean and celestial order, is a tool for visualizing atmospheric forecasts derived from CMIP6 models on a regional scale."),
                           p("This tool enables you to select a region around a country, choose from a variety of climate models, and examine different climate variables across several Shared Socioeconomic Pathways (SSPs)."),
                           p("Learn more about CMIP6 models, the climate forecasts and about the Intergovernmental Panel on Climate Change (IPCC):"),
                           p(tags$a(href="https://www.carbonbrief.org/cmip6-the-next-generation-of-climate-models-explained/", target="_blank", "Simple explanation on CMIP6 and IPCC")),
                           p(tags$a(href="https://www.ipcc.ch/", target="_blank", "IPCC")),
                           p(tags$a(href="https://www.carbonbrief.org/cmip6-the-next-generation-of-climate-models-explained/", target="_blank", "CMIP6")),
                           h4("Climate Models and Scenarios"),
                           p("This tool enables the user to visualize forecasts from 35 CMIP6 global climate models. These models help predict how the climate could evolve based on various internal and external factors."),
                           p("The SSPs represent different pathways of socioeconomic development, affecting greenhouse gas emissions and land use in the future. The scenarios available in V.A.R.U.N.A. include SSP 126 (a sustainable path aiming for a low greenhouse gas concentration), SSP 245 (a middle-of-the-road scenario), SSP 370 (a high greenhouse gas emissions due to energy-intensive consumption), and SSP 585 (the highest greenhouse gas emissions pathway, representing a future with no policy changes to curb emissions)."),
                           p(tags$a(href="https://www.carbonbrief.org/explainer-how-shared-socioeconomic-pathways-explore-future-climate-change/", target="_blank", "A great resource to learn more about SSPs apart from the original publication.")),
                           h4("Citation"),
                           p("Riahi, K., van Vuuren, D. P., Kriegler, E., Edmonds, J., O’Neill, B. C., Fujimori, S., Bauer, N., Calvin, K., Dellink, R., Fricko, O., Lutz, W., Popp, A., Crespo Cuaresma, J., KC, S., Leimbach, M., Jiang, L., Kram, T., Rao, S., Emmerling, J., ... Tavoni, M. (2017). The Shared Socioeconomic Pathways and their energy, land use, and greenhouse gas emissions implications: An overview. Global Environmental Change, 42, 153-168. ", tags$a(href="https://doi.org/10.1016/j.gloenvcha.2016.05.009", target="_blank", "https://doi.org/10.1016/j.gloenvcha.2016.05.009")),
                           h4("Climate Variables"),
                           p("tas (Temperature at Surface), tasmax (Maximum Temperature at Surface), tasmin (Minimum Temperature at Surface), pr (mean precipitation flux), hurs (near surface relative humidity), huss (Specific Humidity), rlds (Downwelling Longwave Radiation at Surface), rsds (Downwelling Shortwave Radiation at Surface), and sfcWind (Surface Wind Speed)."),
                           p("More information about these variables and how they are measured can be found here: https://pcmdi.llnl.gov/mips/cmip3/variableList.html"),
                           h5("Data Source"),
                           p("The NEX-GDDP-CMIP6 dataset, provided by NASA Earth Exchange, comprises global downscaled climate scenarios derived from the General Circulation Model (GCM) runs conducted under CMIP6. Developed in support of the IPCC's Sixth Assessment Report, these high-resolution, bias-corrected projections are distributed through the Earth System Grid Federation. The dataset spans all four 'Tier 1' SSPs, offering insights into climate change impacts on processes sensitive to climate gradients and local topography."),
                           h5("Citation"),
                           p("NASA Earth Exchange Global Daily Downscaled Projections (NEX-GDDP-CMIP6) was accessed on 2024-05-02 from https://registry.opendata.aws/nex-gddp-cmip6. NEX-GDDP-CMIP6 data was accessed on [date] from https://registry.opendata.aws/nex-gddp-cmip6"),
                           p("This tool was developed by Dr. Sambadi Majumder. For any questions and suggestions please feel free to email sambadimajumder@gmail.com"),
                           p("The source code and citations for libraries used can be found here: https://github.com/SamMajumder/VARUNA")
                  )
      ),
      textOutput("status")
    )
  )
) 


server <- function(input, output, session) {
  observeEvent(input$submit, {
    withProgress(message = 'Processing data...', {
      setProgress(0)
      output$status <- renderText("Extracting bounds...")
      
      # Extract bounds based on selected country
      bounds <- extract_bounds(Country = input$country)
      setProgress(0.1)  # Update progress after extracting bounds
      
      # Scenarios being processed
      scenarios <- c("ssp126", "ssp245", "ssp370", "ssp585")
      setProgress(0.2)  # Update progress after defining scenarios
      
      output$status <- renderText("Processing data scenarios...")
      # Process and export data
      datasets <- process_multiple_scenarios(start_year = as.numeric(input$startYear),
                                             end_year = as.numeric(input$endYear),
                                             model = input$model,
                                             variable = input$variable,
                                             scenarios = scenarios,
                                             bounds = bounds,
                                             num_workers = 4)
      setProgress(0.6)  # Major data processing step, update progress significantly
      
      if (!dir.exists(here("Geotif"))) {
        dir.create(here("Geotif"), recursive = TRUE)
      }
      
      output$status <- renderText("Exporting datasets...")
      export_datasets_to_netcdf(dataset_dict = datasets, output_folder = here("Geotif"))
      setProgress(0.8)  # Update progress after exporting data
      
      output$status <- renderText("Loading data for visualization...")
      # Load datasets into separate objects
      test_ssp126 <- terra::rast(list.files(here("Geotif"), pattern = "_ssp126\\.nc$", full.names = TRUE))
      test_ssp245 <- terra::rast(list.files(here("Geotif"), pattern = "_ssp245\\.nc$", full.names = TRUE))
      test_ssp370 <- terra::rast(list.files(here("Geotif"), pattern = "_ssp370\\.nc$", full.names = TRUE))
      test_ssp585 <- terra::rast(list.files(here("Geotif"), pattern = "_ssp585\\.nc$", full.names = TRUE))
      
      setProgress(1)  # Set progress to 100% after loading all data
      output$status <- renderText("Data processing, export, and loading complete.")
      
      # Setup time slider
      times <- terra::time(test_ssp126)
      output$dynamicSlider <- renderUI({ 
        sliderTextInput("layer", "Month-Year:",
                        choices = as.character(times),
                        selected = as.character(times[1]),
                        animate = TRUE)
      })
      
      # Initialize maps for each dataset
      createMap(input, output, test_ssp126, "map_ssp126", "map_ssp126_click", baseMapType = "Esri.WorldImagery")
      createMap(input, output, test_ssp245, "map_ssp245", "map_ssp245_click", baseMapType = "Esri.WorldImagery")
      createMap(input, output, test_ssp370, "map_ssp370", "map_ssp370_click", baseMapType = "Esri.WorldImagery")
      createMap(input, output, test_ssp585, "map_ssp585", "map_ssp585_click", baseMapType = "Esri.WorldImagery")
    })
    # Use session$onEnded to ensure folder is deleted after session ends
    session$onEnded(function() {
      unlink(here("Geotif"), recursive = TRUE)
    })
  })
} 


shinyApp(ui = ui, server = server)








