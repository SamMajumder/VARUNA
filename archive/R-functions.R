# Adjusted function definition to include 'input' and 'output' as parameters
createMap <- function(input, output, dataset, outputId, inputId, baseMapType = "OpenStreetMap") {
  # Retrieve the variable name once, assuming it's consistent across all layers
  variable_name <- terra::varnames(dataset)[1]
  
  # Dynamic retrieval of timestamps
  timestamps <- reactive({ as.character(terra::time(dataset)) })
  
  # Compute the layer index reactively based on the input slider
  layer_index <- reactive({
    which(timestamps() == input$layer)
  })
  
  output[[outputId]] <- renderLeaflet({
    raster_layer <- dataset[[layer_index()]]
    
    # Setup the color palette
    pal <- colorNumeric(palette = "RdYlBu", 
                        domain = range(values(raster_layer), 
                                       na.rm = TRUE), 
                        na.color = "transparent",
                        reverse = TRUE)
    
    # Create and render the Leaflet map
    leaflet() %>%
      # Select base map type based on function argument
      addProviderTiles(provider = baseMapType) %>%
      addRasterImage(raster_layer, colors = pal, opacity = 1, layerId = "rasterLayer") %>%
      addLegend(pal = pal, values = values(raster_layer), opacity = 0.5, 
                title = sprintf("%s: %s", variable_name, input$layer))
  })
  
  observeEvent(input[[inputId]], {
    click <- input[[inputId]]
    if (!is.null(click)) {
      coords <- matrix(c(click$lng, click$lat), ncol = 2)
      value <- terra::extract(dataset[[layer_index()]], coords)
      value <- ifelse(is.na(value), "No data", round(value, 1))
      
      # Update map with a popup showing the data value and timestamp
      leafletProxy(outputId) %>%
        clearPopups() %>%
        addPopups(lng = click$lng, lat = click$lat, 
                  popup = sprintf("%s Value: %s (%s)", variable_name, value, input$layer))
    }
  })
} 


