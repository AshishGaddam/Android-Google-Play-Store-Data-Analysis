# The Android App Market on Google Play – Data Insights
📱 As mobile apps become easier to develop and increasingly profitable, the Android app market has expanded rapidly. This growth highlights the importance of analyzing app performance, pricing, and user feedback to uncover valuable insights that can support growth and user retention.

In this project, I conducted an in-depth analysis of more than 10,000 Android apps available on the Google Play Store, covering various categories and app features. The goal was to identify patterns and trends that can help optimize app development and marketing strategies.

`Dataset Details`:
The data was collected by scraping the Google Play Store and consists of:

`apps.csv`: Detailed information about each app, including category, rating, size, number of installs, type (free or paid), and price.

`user_reviews.csv`: Contains up to 100 user reviews per app, pre-processed and labeled with sentiment scores to facilitate textual analysis.

This analysis offers valuable insights for developers, marketers, and stakeholders to better understand trends in the Android app market and make informed decisions.

### 📱 Project Tasks
#### 1. Import & Explore iPhone App Store Data
Analyzed datasets containing metadata about thousands of iOS apps across various categories.

#### 2. Data Cleaning & Preprocessing
Removed duplicates, handled missing values, and standardized formats to ensure clean and consistent data.

#### 3. Correcting Data Types
Converted price, size, rating, and review count to appropriate numeric formats for analysis.

#### 4. Exploring App Categories
Identified the most common app categories, analyzed their average ratings, pricing strategies, and app count distribution to understand market focus.

#### 5. App Ratings Distribution
Visualized the distribution of app ratings to assess overall quality trends and outliers.

#### 6. Analyzing App Size and Pricing
Investigated how app size and pricing vary across categories and their impact on popularity.

#### 7. Category vs Price Insights
Compared average app prices across different categories to highlight monetization trends.

#### 8. Filtering Low-Quality or Irrelevant Apps
Identified and excluded "junk" or low-engagement apps using thresholds for ratings, reviews, and relevance.

#### 9. Free vs Paid Apps Analysis
Compared popularity metrics (downloads, ratings) between free and paid apps to evaluate market dynamics.

#### 10. Sentiment Analysis of User Reviews (if review data is available)
Analyzed review text using sentiment scoring to understand user satisfaction and app perception.


## Dataset

This project uses two main datasets:

- [apps.csv](data/apps.csv) — Contains app details such as category, rating, size, installs, type, and price.
- [user_reviews.csv](data/user_reviews.csv) — Contains user reviews pre-processed and tagged with sentiment scores.

If you want to explore the original dataset, you can find it here:  
[Android App Market Dataset on Kaggle](https://www.kaggle.com/datasets/utshabkumarghosh/android-app-market-on-google-play)


