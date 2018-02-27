#
# This is a Shiny web application. You can run the application by clicking
# the 'Run App' button above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

library(shiny)
library(dplyr)
library(ggplot2)

load(file = "playSounds.RData")
# Define UI for application that draws a histogram
ui <- fluidPage(
   
   # Application title
   titlePanel("Unspoken Shakespeare"),
   
   # Sidebar with a slider input for number of bins 
   sidebarLayout(
      sidebarPanel(
        checkboxGroupInput("playsSelected", 
                           "Play Symbols: ", 
                           playSounds$`Play Code`)), 
      
      # Show a plot
      mainPanel(
        h2("Number of Sounds in Each Act"), 
        plotOutput("histPlot")
      )
   )
)

# Define server logic required to draw a histogram
server <- function(input, output) {
   output$histPlot <- renderPlot({
       playsSelected = input$playsSelected
       playNames = c(rep(playsSelected, each = 7))
       acts = rep(c("_Induction", "Act 1", "Act 2", "Act 3",
                "Act 4", "Act 5", "Total"), length(playsSelected))
       tempPlays = playSounds[playSounds$`Play Code` %in% playsSelected, ]
       tempPlays$'Play Code' <- NULL
       values = as.vector(t(tempPlays))
       data= data.frame(playNames, acts, values)

       ggplot(data, aes(fill= playNames, x = acts,y = values )) +
            geom_bar(stat = "identity")
   })
}

# Run the application 
shinyApp(ui = ui, server = server)

