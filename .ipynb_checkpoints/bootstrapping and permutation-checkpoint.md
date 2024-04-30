https://towardsdatascience.com/bootstrapping-vs-permutation-testing-a30237795970
https://web.archive.org/web/20060215221403/http://bcs.whfreeman.com/ips5e/content/cat_080/pdf/moore14.pdf

- Bootstrapping, and resampling methods in general, are very powerful because they make fewer assumptions about the population distributions (there is no normality constraint, for example), there are typically no formulas involved and the calculations are relatively simple.
- The main advantage of using the bootstrap method over the analytical method when comparing two groups is that under the BS method there is no Normality restriction for the populations. Also, we are not restricted here to just the comparison of the means.
- We need to interpret this result very carefully now, depending on what kind of test we are conducting, in order to get the p-value:
    - if we are conducting a left-tailed test, we need to take the AUC to the left
    - if we are conducting a right-tailed test, we need to take the AUC to the right
    - if we are conducting a two-tailed test, we need to take the smaller AUC value (because it always represents a tail region) and multiply it by 2


- Permutation tests are used to determine whether an observed effect could reasonably be ascribed to the randomness introduced in selecting the sample(s)
- When permutation tests can be used:

    - Two-sample scenarios when the null hypothesis states that the two populations are identical. We may wish to compare any base statistic for the populations. Traditional tests are very limited in terms of what statistic we can choose.
    - Matched pair scenarios when the null hypothesis states that there are only random differences within pairs. A wide selection of comparisons is possible here too.
    - Two quantitative variables scenarios when the null hypothesis states that the variables are not related. Usually the correlation is the most common measure, but not the only one.
    
When permutation tests should be used instead of bootstrap tests:
    - a permutation test really looks at whether the two samples can hypothetically come from the same population using a certain narrow statistic, while a bootstrap test looks specifically at the statistic itself, so a permutation test is a “deeper”, more general comparison than a bootstrap test
    - BUT (beware!) the test statistic may not show it, depending on how you design it and how well it captures the actual differences between the samples.
   
   In summary, permutation tests should be used for:

    - Hypothesis testing for the presence (or absence) of effects (e.g. whether any effect of a certain kind is present at all, or whether some positive effect is present, or whether some negative effect is present).
    
   Bootstrapping should be used for:

    - Quantitative hypothesis testing for specific known/expected effects (e.g. was the average life span of the car batteries actually improved by a year or more?).
    - Determining confidence intervals non-parametrically.
    


Data Engineer is the most in-demand position with over 2,200 job openings.
The position that has the greatest median salary is Data Modeler at $244,650, but there are 63 vacancies for this role. 
California is the highest job growth with more than 1,300 job opportunies, but its median salary ranks only within the top 7.
Most jobs are seeking cancidates at the Mid Senior level rather than the Associate level, and it'll make sense that the median salary for the Mid Senior level is $40,000 higher than that for the Associate level.
Among some large companies, Capital One and Amazon stand out as the most active companies, with 89 and 88 job openings orespectively, significant more than other companies. Google has the highest median salary at $251,000, followed by Capital One.
Each company tends to focus on different positions. For example, Bank of America is seeking more Data Analyst while Amazon is hiring more Data Engineer. Walmart needs both Data Engineer and Data Scientist, while Capital One has many job openings for Data Manager.
Communication skills are the most commonly required in the data-related job market, followed by two programming skills which are Python and SQL.
In some comparisons of skills, it shows that among three programming languages used in the data field, Python and SQL are more popular than R. Regarding data visualization tools, Tableau is slightly more recognized than Power BI. It seems like there is just little difference in usage between two machine learning platforms: Tensorflow and Pytorch. Spark is a little better-known big data tool compared to Snowflake and Hadoop. Among five different database management system Nosql, Mysql, Sql Server, Postgres and Oracle, Nosql is more in demand than the others, while the remaining four have simirlar popularity in the market. For cloud platforms, AWS skills are significantly more needed, followed by Azure.

