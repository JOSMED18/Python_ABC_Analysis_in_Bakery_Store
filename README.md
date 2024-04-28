# ABC Analysis in Bakery Store Dataset 🥖
This dataset comes from Kaggle and the link below. This represents the 2021 sales and january to september 2022 sales.
  Url: https://www.kaggle.com/datasets/matthieugimbert/french-bakery-daily-sales 

One of the basic concepts in supply chain management is ABC analysis. Even though is a superficial analysis, provides very useful information and insights in terms of forecasting and inventory management. In theory, ABC analysis represents 3 categories which are represented by 3 different groups of products. This analysis follows the pareto rule and the most common metric to develop it is Revenue. 

## Applying Pareto Rule
The Pareto rule says that 80% of the revenue comes from 20% of the products. Ok, but, why is it useful? Well, it means the world in companies with hundread, thousands of SKUs! And this rule applies in this case also, let's see the plots 👀: 

![image](https://user-images.githubusercontent.com/101015892/209892735-b98422aa-726b-4d85-83a4-db471405e8d0.png)

This image shows us that 80% of revenue comes from products in A segment. However, if you see the code attached you will notice that is not a big deal. It is programmed to get this numbers so category A has it. But let's look how amazing is Pareto rule.

![image](https://user-images.githubusercontent.com/101015892/209893459-d58c4335-e0bd-4483-a43c-7d9e9a5abed3.png)

Now we see that 90 of 147 items represent this category C, that is 5% of the revenue!💥

Let's see the impact at the first 2 Supply Chain stages of this analysis:

### Forecasting 
Forecast, specially quantitive analysis implies Demand data. Some companies are used to use sales data, but it does not represent real demand. For this project, we have sales dataset available. In a basic quantitive analysis there is a forecat for each product you distribute. It is really easy for companies with 30 SKU's, now imagine having 200 or 10,000! And you can't focus in each one equally, it is simply not productive since, as we saw before, 80% percent of SKU's rise only 5% of revenue. 

![image](https://user-images.githubusercontent.com/101015892/209895216-99f2860b-b3a3-4a9d-a684-182307619d67.png)

Here we see sales through the whole dataset period, and we could see some seasonality within certain periods. However, that's a topic for a time series analysis. 

### Inventory Management
What happens inside a warehouse? There are boxes and pallets going from one place to another and that movement have a cost. As a consequence, movement have to be optimized. So it's better to have your category A as near as possible from de doors so you can find it quickly. 

## Conclusion
ABC analysis can save a bunch of time in forecasting analysis and also a lot of money in terms of warehouse management. It is a good place to start an analysis and set the basis for further analysis in Supply Chain Management. 
