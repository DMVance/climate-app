# sqlalchemy-challenge: Climate App

### Step 1 Climate Analysis and Exploration

Started by creating the engine and connection to the database, then used declarative_base() to reflect the database tables into classes.

In the Station Analysis section, I ran into trouble trying to do something like this: max(count(m.station)) with either SQL or SQLAlchemy queries, so I first queried the count of stations, then made a dataframe with count of stations in descending order. Then the max count of any single station was the first element of the dataframe. I need to research a more efficient query that can take care of that without having to do some of the work in pandas.

I was pleased with the use of f-strings in combination with SQL statements for querying the database.

### Step 2 Climate App

I used the same patterns for reflecting the database tables into classes and query statements as I did for Step 1.

An unexpected error was solved with "?check_same_thread=False" in the create_engine statement.

A new-to-me numpy method of unpacking the results of a query was used: np.ravel(results)

### Bonus: Other Recommended Analyses

Temperature Analysis I t-test: 
The differences in average temps between June and December are relatively insignificant, ranging from 1 to 6 degrees depending on the station.
The t-test resulted in a high t-score, indicating the datasets are more different (meaning the results are likely repeatable) and less similar and the probability is very low that the difference is a result of chance (very low p-value).
I chose to do an unpaired t-test since there are two distinct datasets (temperatures for June and December over multiple years), rather than samples from within a single dataset.

Temperature Analysis II: Done.

Daily Rainfall Average: Done.
