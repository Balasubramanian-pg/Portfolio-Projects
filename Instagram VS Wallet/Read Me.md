We are all guilty of buying some random products after seeing an advertisement in social media which can or can not be influenced by your favourite influcers.
Hence in this project we decided to create a model which analyses and predicts how satisfied | unsatisfied certain shoppers are with their social media influenced purchase
The data set is scraped from various sites and the approach I have taken to document my steps are below

**key questions to ask**, **problems to solve**, and the **approach to take**. 

This framework will help ensure the project is comprehensive, actionable, and aligned with the needs of both consumers and businesses.

---

## **Key Questions to Ask**

### **For Consumers**
1. **Behavioral Insights**:
   - What drives consumers to purchase products they see on TikTok?
   - How often do consumers regret purchases influenced by social media trends?
   - What factors (e.g., price, product category, trend longevity) influence regret the most?

2. **Decision-Making**:
   - Are consumers aware of the potential for regret when making impulse purchases?
   - What tools or information could help consumers make more informed decisions?

3. **Post-Purchase Behavior**:
   - How do consumers dispose of regretted purchases (e.g., resale, return, discard)?
   - What role do product reviews and ratings play in post-purchase satisfaction?

---

### **For Businesses**
1. **Trend Impact**:
   - How do TikTok trends impact sales and return rates?
   - Which product categories are most affected by TikTok-driven purchases?

2. **Inventory and Marketing**:
   - How can businesses better predict and capitalize on TikTok trends?
   - What strategies can reduce return rates and improve customer satisfaction?

3. **Customer Insights**:
   - Who are the most impulsive buyers, and how can businesses target them effectively?
   - How can businesses use TikTok trends to build long-term customer loyalty?

---

## **Key Problems to Solve**

### **For Consumers**
1. **Impulse Buying**:
   - Help consumers recognize and avoid impulsive purchases driven by social media trends.
   - Provide tools to evaluate the long-term value of a product before purchasing.

2. **Post-Purchase Regret**:
   - Reduce the likelihood of regret by offering insights into product sustainability, quality, and usability.
   - Create a platform for consumers to share and learn from others’ experiences.

3. **Resale and Returns**:
   - Simplify the process of reselling or returning regretted purchases.
   - Provide data-driven recommendations on the best resale platforms for specific products.

---

### **For Businesses**
1. **Trend-Driven Sales**:
   - Help businesses identify and capitalize on TikTok trends without overstocking or misaligning inventory.
   - Predict the longevity of trends to avoid investing in short-lived fads.

2. **Return Rate Reduction**:
   - Identify products with high regret rates and improve their quality, marketing, or pricing.
   - Develop targeted campaigns to reduce impulse buying and improve customer satisfaction.

3. **Customer Retention**:
   - Use insights from regret analysis to improve product offerings and customer experiences.
   - Build trust by being transparent about the risks of trend-driven purchases.

---

## **Approach to Take**

### **1. Data Collection and Integration**
   - **Facebook Data**: Use TikTok’s API to collect data on trending products, hashtags, and engagement metrics.
   - **Transaction Data**: Partner with banks or payment platforms to access anonymized purchase data.
   - **Resale and Return Data**: Scrape or integrate with platforms like eBay, Poshmark, and Shopify for resale and return data.
   - **User Surveys**: Conduct surveys to gather qualitative data on purchase motivations and regret.

### **2. Data Analysis**
   - **Trend Analysis**:
     - Identify patterns in Facebook trends (e.g., peak popularity, decline).
     - Correlate trends with purchase and regret data.
   - **Regret Analysis**:
     - Use machine learning to predict regret based on factors like price, trend longevity, and sentiment.
     - Segment regret rates by product category, demographic, and region.
   - **Sentiment Analysis**:
     - Analyze product reviews and survey responses to gauge satisfaction and identify common pain points.

### **3. Tool Development**
   - **Consumer-Facing App**:
     - Provide real-time insights into TikTok trends and their potential for regret.
     - Offer personalized recommendations based on user behavior and preferences.
   - **Business Dashboard**:
     - Visualize trend impact, regret rates, and return data.
     - Provide actionable insights for inventory planning and marketing strategies.

### **4. Testing and Validation**
   - **A/B Testing**:
     - Test different interventions (e.g., product recommendations, trend warnings) to reduce regret.
   - **User Feedback**:
     - Continuously gather feedback from consumers and businesses to refine the tool.

### **5. Scaling and Deployment**
   - **Cloud Infrastructure**:
     - Use cloud platforms (e.g., AWS, Google Cloud) for scalable data storage and processing.
   - **API Integration**:
     - Integrate with e-commerce platforms, resale platforms, and social media APIs for real-time data.

---

## **How does the Workflow Look?**

1. **Data Collection**:
   - Collect Facebook trend data, purchase data, and resale/return data.
   - Scrape user surveys to gather qualitative insights.

2. **Data Processing**:
   - Clean and preprocess data to remove duplicates and inconsistencies (In this specific case we are narrowing down to certain categories of product and narrowing down on the timeline).
   - Anonymize sensitive data to ensure privacy.

3. **Analysis**:
   - Perform trend analysis, regret analysis, and sentiment analysis.
   - Build predictive models to estimate regret probability.

4. **Visualization**:
   - Create dashboards for consumers and businesses using Power BI or Tableau.
   - Provide actionable insights and recommendations.

5. **Deployment**:
   - Launch the consumer-facing app and business dashboard.
   - Continuously monitor performance and gather feedback for improvements.

---

By addressing these questions, solving the identified problems, and following a structured approach, you can create a powerful tool that helps consumers make smarter purchases and businesses optimize their strategies in the age of social media-driven commerce.
