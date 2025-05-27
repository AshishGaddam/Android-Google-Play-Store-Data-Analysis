#!/usr/bin/env python
# coding: utf-8

# ## 1. Google Play Store apps and reviews

# 📱 As mobile apps become easier to develop and increasingly profitable, the Android app market has expanded rapidly. This growth highlights the importance of analyzing app performance, pricing, and user feedback to uncover valuable insights that can support growth and user retention.
# 
# In this project, I conducted an in-depth analysis of more than 10,000 **`Android apps`** available on the **`Google Play Store`**, covering various categories and app features. The goal was to identify patterns and trends that can help optimize app development and marketing strategies.

# <img src="https://upload.wikimedia.org/wikipedia/commons/7/78/Google_Play_Store_badge_EN.svg" alt="Google Play Store Logo" width="850">

# Dataset Details: The data was collected by scraping the Google Play Store and consists of:

# **`apps.csv`** : Detailed information about each app, including category, rating, size, number of installs, type (free or paid), and price.
# 
# **`user_reviews.csv`** : contains 100 reviews for each app, [most helpful first](https://www.androidpolice.com/2019/01/21/google-play-stores-redesigned-ratings-and-reviews-section-lets-you-easily-filter-by-star-rating/). The text in each review has been pre-processed and attributed with three new features: Sentiment (Positive, Negative or Neutral), Sentiment Polarity and Sentiment Subjectivity.
# 

# In[9]:


# Read in dataset
import pandas as pd


# Load the datasets (Mac style path with forward slashes)
apps_with_duplicates = pd.read_csv('/Users/ashish/Downloads/datasets/apps.csv')


# Drop duplicates
apps = apps_with_duplicates.drop_duplicates()


# Print the total number of apps in the dataset
print('Total number of apps in the dataset = ', apps['App'].count())


# Print a concise summary of apps dataframe
print(apps.info())


# Have a look at a random sample of n rows
# View 5 random rows
n = 5
apps.sample(n=5)


# ## 2. Data Cleaning & Preprocessing

# The four primary features we will focus on throughout this analysis are **`Installs`**, **`Size`**, **`Rating`**, and **`Price`**. These columns are crucial in determining patterns around app popularity, usability, and monetization strategies.
# 
# From our earlier exploration using the **`info()`** function, we observed that both **`Installs`** and **`Price`** are of data type **`object`** instead of the expected **`int64`** or **`float64`**. This discrepancy occurs because these columns contain non-numeric characters such as commas **`(0,9)`**, dollar signs **`($)`**, and plus signs **`(+)`**, which prevent them from being treated as purely numerical values.
# 
# In order to perform meaningful analysis and statistical operations, it is essential to clean and convert these columns into numeric types. This step involves:
# 
# Removing special characters like **`$`**, **`+`**, and **`,`**
# 
# Handling missing or inconsistent entries
# 
# Casting the cleaned strings into appropriate numeric types (**`int`** or **`float`**)
# 
# This **data cleaning** process is a vital preprocessing step to ensure accuracy and consistency in our upcoming visualizations, comparisons, and modeling tasks.
# 
# 

# In[14]:


# List of characters to remove
chars_to_remove = ['+',',','$']     

# List of column names to clean
cols_to_clean = ['Installs','Price']

# Loop for each column
for col in cols_to_clean:
    
    # Replace each character with an empty string
    for char in chars_to_remove:
        apps[col] = apps[col].astype(str).str.replace(char, '')
    
    # Convert column to numeric type
    apps[col] = pd.to_numeric(apps[col])


# ## 3. Exploring App Categories

# Google Play serves over 1 billion active users across 190 countries, making it a critical platform for app deployment and user acquisition. To enhance app discoverability and optimize user search experience, Google classifies apps into predefined categories.
# 
# This categorization enables us to analyze:
# 
# * The distribution and market share of apps across various categories.
# 
# * Identification of categories with dominant market penetration.
# 
# * Categories with minimal app representation.
# 
# Our dataset comprises 33 unique app categories. Analysis shows that the **`Family`** and **`Games`** categories have the highest app count, indicating significant user engagement and developer focus. Categories such as **`Tools`**, **`Business`**, and **`Medical`** also demonstrate substantial market presence, highlighting their importance in the app ecosystem.
# 
# 

# In[17]:


# 
import plotly
plotly.offline.init_notebook_mode(connected=True)
import plotly.graph_objs as go


# Print the total number of unique categories
num_categories = len(apps['Category'].unique())
print('Number of categories = ', num_categories)


# Count the number of apps in each 'Category' and sort them in descending order
num_apps_in_category = apps['Category'].value_counts().sort_values(ascending = False)


#print(num_apps_in_category)
fig = go.Figure(data=[go.Bar(
    x=num_apps_in_category.index,  # index = category name
    y=num_apps_in_category.values,  # value = count
)])

fig.update_layout(title_text='Number of Apps in Each Category')

fig.show()


# ## 4. Distribution of app ratings

# App ratings play a critical role in influencing an app’s visibility on Google Play, user trust, and potential download volume. With ratings ranging from `1` to `5`, they act as an essential quality metric for developers and businesses alike.
# 
# In this section, we aim to explore how **`app ratings are distributed`** across the Play Store using our dataset. Understanding this distribution allows us to assess user satisfaction levels, identify potential outliers, and evaluate overall app performance.
# 
# To begin, we examined the **`Rating`** column to identify any null or missing values, then visualized the ratings through a histogram for a clearer understanding.

# In[19]:


import plotly.graph_objs as go

# Average rating of apps
avg_app_rating = apps['Rating'].mean()
print('Average app rating = ', avg_app_rating)

# Distribution of apps according to their ratings
data = [go.Histogram(x=apps['Rating'], nbinsx=20, marker=dict(color='skyblue'))]

# Create a layout
layout = go.Layout(title='Distribution of App Ratings', xaxis=dict(title='App Rating'), yaxis=dict(title='Count'))

# Combine data and layout into a Figure object
fig = go.Figure(data=data, layout=layout)

# Use show to display the figure
fig.show()


# ## 5. Size and price of an app

# Let's now examine app size and app price. For **`size`**, if the mobile app is too large, it may be difficult and/or expensive for users to download. Lengthy download times could turn users off before they even experience your mobile app. Plus, each user's device has a finite amount of disk space. For **`price`**, some users expect their apps to be free or inexpensive. These problems compound if the developing world is part of your target market; especially due to internet speeds, earning power and exchange rates.
# 
# How can we effectively come up with strategies to **`size`** and **`price`** our app?
# 
# * Does the size of an app affect its rating?
# * Do users really care about system-heavy apps or do they prefer light-weighted apps?
# * Does the price of an app affect its rating?
# * Do users always prefer free apps over paid apps?
# 
# We find that the majority of `top rated apps` (rating over 4) range from 2 MB to 20 MB. We also find that the vast majority of apps price themselves under `$10`.

# In[20]:


import matplotlib.pyplot as plt

# Filter rows where both Rating and Size values are not null
apps_with_size_and_rating_present = apps[(~apps['Rating'].isnull()) & (~apps['Size'].isnull())]

# Subset for categories with at least 250 apps
large_categories = apps_with_size_and_rating_present.groupby('Category').filter(lambda x: len(x) >= 250).reset_index()

# Create a scatter plot for Size vs. Rating
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.scatter(large_categories['Size'], large_categories['Rating'], alpha=0.5, color='blue')
plt.title('Size vs. Rating')
plt.xlabel('App Size (in MB)')
plt.ylabel('App Rating')
plt.grid(True)

# Filter rows where both Rating and Price values are not null
apps_with_price_and_rating_present = apps[(~apps['Rating'].isnull()) & (~apps['Price'].isnull())]

# Subset for paid apps
paid_apps = apps_with_price_and_rating_present[apps_with_price_and_rating_present['Type'] == 'Paid']

# Create a scatter plot for Price vs. Rating
plt.subplot(1, 2, 2)
plt.scatter(paid_apps['Price'], paid_apps['Rating'], alpha=0.5, color='green')
plt.title('Price vs. Rating for Paid Apps')
plt.xlabel('App Price (in $)')
plt.ylabel('App Rating')
plt.grid(True)

plt.tight_layout()
plt.show()


# ## 6. Relation between app category and app price

# So now comes the hard part. How are companies and developers supposed to make ends meet? What monetization strategies can companies use to maximize profit? The costs of apps are largely based on **`features`**, **`complexity`**, and **`platform`**.
# 
# There are many factors to consider when selecting the right pricing strategy for your mobile app. It is important to consider the willingness of your customer to pay for your app. A wrong price could break the deal before the download even happens. Potential customers could be turned off by what they perceive to be a shocking cost, or they might delete an app they’ve downloaded after receiving too many ads or simply not getting their money's worth.
# 
# Different categories demand different price ranges. Some apps that are simple and used daily, like the calculator app, should probably be kept free. However, it would make sense to charge for a highly-specialized medical app that diagnoses diabetic patients. Below, we see that Medical and Family apps are the most expensive. Some medical apps extend even up to `$80`! All game apps are reasonably priced below `$20`.

# In[32]:


import seaborn as sns
import matplotlib.pyplot as plt

# Set the size of the plot
plt.figure(figsize=(15, 8))

# Select a few popular app categories
popular_app_cats = apps[apps.Category.isin(['GAME', 'FAMILY', 'PHOTOGRAPHY',
                                            'MEDICAL', 'TOOLS', 'FINANCE',
                                            'LIFESTYLE','BUSINESS'])]

# Create a box plot to visualize the distribution of app prices across categories
sns.boxplot(x='Category', y='Price', data=popular_app_cats)
plt.title('App Price Distribution Across Categories')
plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
plt.show()


# ## 7. Exploring Differences Between App Categories: Count, Ratings & Price

# Objective:
# To uncover patterns in how different `app categories` compare in terms of:
# 
# * The `number of available apps`
# 
# * Their `average user ratings`
# 
# * Their `pricing strategies`
# 
# This analysis helps us understand which categories are saturated, which ones are performing well in terms of user satisfaction, and how developers are monetizing apps in each category.

# In[31]:


# Clean 'Rating' column and remove missing values for this analysis
apps = apps[apps['Rating'].notnull()]

# 1. Count of apps in each category
category_counts = apps['Category'].value_counts()

# 2. Average rating by category
avg_rating_by_category = apps.groupby('Category')['Rating'].mean().sort_values(ascending=False)

# 3. Average price by category
avg_price_by_category = apps.groupby('Category')['Price'].mean().sort_values(ascending=False)

# ----------------------------------
# Plot 1: Number of Apps in Each Category
fig1 = go.Figure([go.Bar(
    x=category_counts.index,
    y=category_counts.values,
    marker_color='lightskyblue'
)])
fig1.update_layout(title='Number of Apps per Category',
                   xaxis_title='Category',
                   yaxis_title='Number of Apps',
                   xaxis_tickangle=-45)
fig1.show()



# Plot 2: Average Rating by Category
fig2 = go.Figure([go.Bar(
    x=avg_rating_by_category.index,
    y=avg_rating_by_category.values,
    marker_color='mediumseagreen'
)])
fig2.update_layout(title='Average App Rating by Category',
                   xaxis_title='Category',
                   yaxis_title='Average Rating',
                   xaxis_tickangle=-45)
fig2.show()



# Plot 3: Average Price by Category
fig3 = go.Figure([go.Bar(
    x=avg_price_by_category.index,
    y=avg_price_by_category.values,
    marker_color='salmon'
)])
fig3.update_layout(title='Average App Price by Category',
                   xaxis_title='Category',
                   yaxis_title='Average Price (USD)',
                   xaxis_tickangle=-45)
fig3.show()


# ## 8. Filtering Out "Junk" Apps — Refined Analysis

# In app marketplaces, anomalies often exist in the form of **`unrealistically priced apps`**—frequently categorized as "junk apps." These apps typically offer little or no real value, have exaggerated prices, and often show signs of being joke or test projects like "I Am Rich Premium".
# 
# To ensure cleaner analysis and accurate insights, it is essential to identify and remove these outliers.
# 
# **`Our Objectives`**:
# * Detect and remove **`"junk apps"`** with very high prices.
# 
# * Understand the distribution of price values.
# 
# * Re-plot clean price distributions to reflect real market behavior.
# 
# 

# In[23]:


# Set the size of the plot
plt.figure(figsize=(15, 8))

# Select apps priced below $100 to filter out potential "junk" apps
apps_under_100 = popular_app_cats[popular_app_cats['Price'] < 100]

# Create a box plot to visualize the distribution of app prices across categories after filtering for junk apps
sns.boxplot(x='Category', y='Price', data=apps_under_100)
plt.title('App Price Distribution Across Categories (Prices < $100)')
plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
plt.show()


# In[24]:


apps


# ## 9. Popularity of paid apps vs free apps

# For apps in the Play Store today, there are five types of pricing strategies: free, freemium, paid, paymium, and subscription. Let's focus on free and paid apps only. Some characteristics of free apps are:
# 
# * Free to download.
# * Main source of income often comes from advertisements.
# * Often created by companies that have other products and the app serves as an extension of those products.
# * Can serve as a tool for customer retention, communication, and customer service.
# 
# 
# Some `characteristics` of paid apps are:
# 
# * Users are asked to pay once for the app to download and use it.
# * The user can't really get a feel for the app before buying it.
# 
# 
# Are paid apps installed as much as free apps? It turns out that paid apps have a relatively lower number of installs than free apps, though the difference is not as stark as I would have expected!

# In[25]:


trace0 = go.Box(
    # Data for paid apps
    y=apps[apps['Type'] =='Paid']['Installs'],
    name = 'Paid'
)

trace1 = go.Box(
    # Data for free apps
    y=apps[apps['Type'] == 'Free']['Installs'],
    name = 'Free'
)

layout = go.Layout(
    title = "Number of downloads of paid apps vs. free apps",
    yaxis = dict(
        type = 'log',
        autorange = True
    )
)

# Combine traces into a Figure object
fig = go.Figure(data=[trace0, trace1], layout=layout)

# Use show to display the figure
fig.show()


# ## 10. Sentiment analysis of user reviews

# Mining user review data to determine how people feel about your product, brand, or service can be done using a technique called sentiment analysis. User reviews for apps can be analyzed to identify if the mood is positive, negative or neutral about that app. For example, positive words in an app review might include words such as **`'amazing'`**, **`'friendly'`**, **`'good'`**, **`'great'`**, and **`'love'`**. Negative words might be words like **`'malware'`**, **`'hate'`**, **`'problem'`**, **`'refund'`**, and **`'incompetent'`**.
# 
# By plotting sentiment polarity scores of user reviews for **`paid`** and **`free`** apps, we observe that free apps receive a lot of harsh comments, as indicated by the outliers on the negative y-axis. Reviews for paid apps appear never to be extremely negative. This may indicate something about app quality, i.e., paid apps being of higher quality than free apps on average. The median polarity score for paid apps is a little higher than free apps, thereby syncing with our previous observation.
# 
# In this notebook, we analyzed over ten thousand apps from the Google Play Store. We can use our findings to inform our decisions should we ever wish to create an app ourselves.

# In[28]:


# Load user_reviews.csv
reviews_df = pd.read_csv('/Users/ashish/Downloads/datasets/user_reviews.csv')

merged_df = pd.merge(apps, reviews_df, on = 'App', how = "inner")

# Drop NA values from Sentiment and Translated_Review columns
merged_df = merged_df.dropna(subset=['Sentiment', 'Translated_Review'])
sns.set_style('ticks')
fig, ax = plt.subplots()
fig.set_size_inches(11, 8)

# User review sentiment polarity for paid vs. free apps
ax = sns.boxplot(x ='Sentiment_Polarity', y ='Type', data = merged_df)
ax.set_title('Sentiment Polarity Distribution')


# 

# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





#  
