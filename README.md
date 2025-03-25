# 2025 March Madness Predictice Model

The goal of this project was to minimize total brier score of outcomes for the 2025 NCAA March Madness Tournaments in hopes of winning [this kaggle competition.](https://www.kaggle.com/competitions/march-machine-learning-mania-2025)

My approach to this project differs to past winners in a few different ways. To start, instead of creating a model for team ratings I made use of the Glicko-2 rating system as well as the [Stephenson Rating System, in which I created my own implementation for python found here.](https://github.com/dsw225/Stephenson-Rating-System) Using these two system I can gather relative team strength more accurately than that of a traditional elo ranking, as well as account for home team advantage using the additional advantage parameter from the stephenson system (Originally used for white-black advantages in chess.) This allowed me to more accurately rank the teams respective to each other.

Beyond pure ratings I also employed relative ratings for Offensive/Defensive efficiency which can be directly compared team-team. This comes in handy where teams strengths may come into play vs. total team strength. (IE Duke has a lower team rating than that of houston, however due to their offensive efficiency rating they are favored in a a H2H matchup.)

After computing team averages, ratings, strengths, as well as seeding differential, I used an XGBoost model training on point differential, as simple W/L results 1/0, don't show how close an outcome was. From there we can then clip our predictions into probabilities.

<img src="https://github.com/dsw225/March-Machine-Learning-Mania-2025/blob/main/imgs/mens_curve.png?raw=true" alt="spread" width="550">
Above is the mens predicted point spread vs. win rate


While the tournament is still currently underway, there are a few improvements I would have made had I had more time. In years past, most winners have won by using overrides on strong teams to win, and while I made use of this on one of my submissions (Duke), I didn't force through other teams. If I had forced 100% proababilities for more teams in the 2nd/3rd round in which I was confident (Houston/Florida), I could've lowered my brier score. 

Another factor which I wanted to implement but was short on time was that of further matchups. IE. While a 14 seed is unlikely to beat a 3, if victorious, their rating/strength (the 14 seed), should be adjusted for that win preemptively. Since games that don't occur aren't considered in our score, adjusting percentages or each teams ratings as if they had defeated the stronger team in the next round matchup could potentially reduce total brier score.

There are many shoulda - coulda - woulda things in this attempt, however, in another year with more upsets, I believe this model has very high ceiling.

## Contributing

Pull requests are welcome. For any changes, please open an issue first
to discuss what you would like to change.
