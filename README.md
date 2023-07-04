# Google_Hackthon_Round_3
Accelerating the application of AI

## How to Setup the system for the Code
Install the library by using `pip install earthengine-api`. Then import the libraries written in the code. 
`ee` library refers to the earth engine library which helps us capture satellite imagery data and can also visualise and process it to make inferences. 
Once the libraries are imported then we have to initialize and authenticate `ee` library by running the command which will automatically open Earth Engine Notebook Client. Sign up with the required google account and get the authentication code to access the commands in the python notebook. 

## Visualisation of the map
The data was gathered from "Earth Engine Hansen Global Forest Change Data" for the years up to 2022 and prior years up to 2001. The grayscale version of the 2000 tree cover was then applied, and the unforested parts were masked up. In areas with enhanced forestation, the colour blue was applied; otherwise, the colour red was used. And pink to the regions showing both an upward and downward trend.

## Data of different countries
The dataset for the "USDOS/LSIB_SIMPLE/2017" feature collection was first filtered to extract India's data. I computed the area of lost deforestation in pixels and decreased the resolution of the `lossImage` from the map visualisation shown above.
The data was then organised into "groups" after being analysed for loss by year. 
I formatted the statistics from the "groups" using the data structure `dictionary`, where the keys are years and the values are the amount of deforestation per year.
I plotted the graph for Yearly Forest Loss in India. 
Repeating the same procedure for 2 more countries The Republic of Congo and Turkey, I analysed the trends in all of the three countries by plotting a line graph.

## Use of AI
The model can be improved further by including various metrics, such as the budget share allocated to the respective Environment Ministries of each country and the various factors causing deforestation, which will help to gather more data and combine all the components in order to train a model. The trained model can then be used to forecast changes in the country's environment or its "deforestation index" in the next years.

