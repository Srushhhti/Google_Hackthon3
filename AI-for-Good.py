#!/usr/bin/env python
# coding: utf-8

# In[2]:


import numpy
import pandas 
import folium
import ee


# In[3]:


import matplotlib.pyplot as plt
import pandas as pd


# In[4]:


ee.Initialize()
ee.Authenticate()


# In[5]:


def add_ee_layer(self, ee_image_object, vis_params, name):
  map_id_dict = ee.Image(ee_image_object).getMapId(vis_params)
  folium.raster_layers.TileLayer(
      tiles=map_id_dict['tile_fetcher'].url_format,
      attr='Map Data &copy; <a href="https://earthengine.google.com/">Google Earth Engine</a>',
      name=name,
      overlay=True,
      control=True
  ).add_to(self)

folium.Map.add_ee_layer = add_ee_layer


# In[6]:


changes2022 = ee.Image('UMD/hansen/global_forest_change_2022_v1_10')
treeCover = changes2022.select(['treecover2000'])
lossImage = changes2022.select(['loss'])
gainImage = changes2022.select(['gain'])
gainAndLossImage = gainImage.And(lossImage)
map_palette = folium.Map(location=[28.6,77.2], zoom_start=5)

# Add the tree cover layer in green.
treeCoverVis = {'palette': ['000000', '00FF00'], 'max': 100}
map_palette.add_ee_layer(treeCover.updateMask(treeCover), treeCoverVis, 'Forest Cover')

# Add the loss layer in red.
lossVis = {'palette': ['FF0000']}
map_palette.add_ee_layer(lossImage.updateMask(lossImage), lossVis, 'Loss')

# Add the gain layer in blue.
gainVis = {'palette': ['0000FF']}
map_palette.add_ee_layer(gainImage.updateMask(gainImage), gainVis, 'Gain')

gainAndLossVis = { 'palette' :['FF00FF']}
map_palette.add_ee_layer(gainAndLossImage.updateMask(gainAndLossImage), gainAndLossVis, 'Gain and Loss')

display(map_palette)


# In[7]:


countries = ee.FeatureCollection('USDOS/LSIB_SIMPLE/2017')


# In[26]:


india = countries.filter(ee.Filter.eq('country_co', 'IN'))
china = countries.filter(ee.Filter.eq('country_co', 'CH'))
congo = countries.filter(ee.Filter.eq('country_co', 'CG'))
USA = countries.filter(ee.Filter.eq('country_co', 'US'))
nigeria = countries.filter(ee.Filter.eq('country_co', 'NI'))
brazil = countries.filter(ee.Filter.eq('country_co', 'BR'))
turkey = countries.filter(ee.Filter.eq('country_co', 'TU'))


# In[27]:


# data only for india

stats = lossImage.reduceRegion(
  reducer=ee.Reducer.sum(),
  geometry=india,
  scale=300,
  maxPixels=1e9
)
# Get the value of the loss in pixels.
lossValue = stats.get('loss')


stats = gainImage.reduceRegion(
  reducer=ee.Reducer.sum(),
  geometry=india,
  scale=300,
  maxPixels=1e9
)
gainValue = stats.get('gain')

print('Loss in pixels:', lossValue.getInfo())
print('Gain in pixels:', gainValue.getInfo())


# In[28]:


areaImage = lossImage.multiply(ee.Image.pixelArea())
stats = areaImage.reduceRegion(
  reducer=ee.Reducer.sum(),
  geometry=india,
  scale=300,
  maxPixels=1e9
)
# Get the value of the loss in pixels.
areaValue = stats.get('loss')
print(areaValue.getInfo())


# In[29]:


lossYear = changes2022.select(['lossyear'])
combinedImage = areaImage.addBands(lossYear)

lossByYear = combinedImage.reduceRegion(
    reducer=ee.Reducer.sum().group(groupField=1),
    geometry=india.geometry(),
    scale=300,
    maxPixels=1e9
)

# Print the result.
print(lossByYear.getInfo())


# In[30]:


groups = lossByYear.get('groups')

# Format the statistics and create a dictionary.
statsFormatted = ee.List(groups).map(lambda el: [
    ee.Number(ee.Dictionary(el).get('group')).format("20%02d"),
    ee.Dictionary(el).get('sum')
])
statsDictionary = ee.Dictionary(statsFormatted.flatten())

# Print the result.
print(statsDictionary.getInfo())


# In[31]:


values = statsDictionary.values().getInfo()
keys = statsDictionary.keys().getInfo()

data = {'Year': keys, 'Loss by year': values}

# Create the dataframe
df = pd.DataFrame(data)
print(df)


# In[14]:


data = [[k, v] for k, v in zip(keys, values)]

# Create the chart.
chart = plt.bar(*zip(*data))
plt.xlabel('Year')
plt.ylabel('Area (square meters)')
plt.title('Yearly Forest Loss')
plt.xticks(rotation=90)
plt.show()


# In[32]:


stats2 = lossImage.reduceRegion(
  reducer=ee.Reducer.sum(),
  geometry=congo,
  scale=300,
  maxPixels=1e9
)
# Get the value of the loss in pixels.
lossValue2 = stats2.get('loss')


# In[33]:


areaImage2 = lossImage.multiply(ee.Image.pixelArea())
stats2 = areaImage2.reduceRegion(
  reducer=ee.Reducer.sum(),
  geometry=congo,
  scale=300,
  maxPixels=1e9
)
# Get the value of the loss in pixels.
areaValue2 = stats2.get('loss')
print(areaValue2.getInfo())


# In[34]:


lossYear2 = changes2022.select(['lossyear'])
combinedImage = areaImage2.addBands(lossYear)

lossByYear2 = combinedImage.reduceRegion(
    reducer=ee.Reducer.sum().group(groupField=1),
    geometry=congo.geometry(),
    scale=300,
    maxPixels=1e9
)

# Print the result.
print(lossByYear2.getInfo())


# In[35]:


groups2 = lossByYear2.get('groups')

# Format the statistics and create a dictionary.
statsFormatted2 = ee.List(groups2).map(lambda el: [
    ee.Number(ee.Dictionary(el).get('group')).format("20%02d"),
    ee.Dictionary(el).get('sum')
])
statsDictionary2 = ee.Dictionary(statsFormatted2.flatten())


# In[36]:


values2 = statsDictionary2.values().getInfo()

data = {'Year': keys, 'India': values, 'Congo' : values2}

# Create the dataframe
df = pd.DataFrame(data)
print(df)


# In[39]:


stats3 = lossImage.reduceRegion(
  reducer=ee.Reducer.sum(),
  geometry=turkey,
  scale=300,
  maxPixels=1e9
)
# Get the value of the loss in pixels.
lossValue3 = stats3.get('loss')


# In[40]:


areaImage3 = lossImage.multiply(ee.Image.pixelArea())
stats3 = areaImage3.reduceRegion(
  reducer=ee.Reducer.sum(),
  geometry=turkey,
  scale=300,
  maxPixels=1e9
)
# Get the value of the loss in pixels.
areaValue3 = stats3.get('loss')
print(areaValue3.getInfo())


# In[44]:


lossYear3 = changes2022.select(['lossyear'])
combinedImage = areaImage3.addBands(lossYear3)

lossByYear3 = combinedImage.reduceRegion(
    reducer=ee.Reducer.sum().group(groupField=1),
    geometry=turkey.geometry(),
    scale=300,
    maxPixels=1e9
)

# Print the result.
print(lossByYear3.getInfo())


# In[45]:


groups3 = lossByYear3.get('groups')

# Format the statistics and create a dictionary.
statsFormatted3 = ee.List(groups3).map(lambda el: [
    ee.Number(ee.Dictionary(el).get('group')).format("20%02d"),
    ee.Dictionary(el).get('sum')
])
statsDictionary3 = ee.Dictionary(statsFormatted3.flatten())


# In[46]:


values3 = statsDictionary3.values().getInfo()

data = {'Year': keys, 'India': values, 'Congo' : values2, 'Turkey': values3}

# Create the dataframe
df = pd.DataFrame(data)
print(df)


# In[49]:


#data1 = [[k, v1] for k, v in zip(keys, values)]
#data2 = [[k, v2] for k, v in zip(keys, values2)]
#data3 = [[k, v3] for k, v in zip(keys, values3)]

plt.plot(keys, values, label='India')
plt.plot(keys, values2, label='Congo')
plt.plot(keys, values3, label='Turkey')

# Adding labels and title to the graph
plt.xlabel('Years')
plt.ylabel('Forest Loss')
plt.title('Forest Loss by Country')

# Adding a legend to differentiate the line plots
plt.legend()
plt.xticks(rotation=90)

# Displaying the graph
plt.show()


# In[ ]:




