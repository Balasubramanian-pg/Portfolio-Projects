Creating synthetic data for a project like this is an exercise in "controlled storytelling." You must make specific assumptions to build in the patterns you intend to discover. Without these assumptions, the data would be random noise, and your analysis would find nothing.

Here are the key assumptions I would make for each of the three datasets, along with the rationale for why each assumption is critical to the project's success.

### Assumptions for Dataset 1: `businesses.csv`

This dataset sets the stage for our entire simulated world.

1.  **Assumption: A Significant Minority of Businesses are Closed.**
    *   **The Assumption:** Around 20-30% of businesses in the dataset will have a `status` of "Permanently Closed." Their `closure_date` will be randomly distributed over the last 1-3 years.
    *   **Rationale:** This ensures there is a large enough sample of closed businesses to make the "ghost review" problem statistically significant and not just a rare anomaly. It gives your scraping and identification phase a meaningful target.

2.  **Assumption: Businesses are Geographically Clustered.**
    *   **The Assumption:** Businesses are not randomly scattered. Their latitude/longitude coordinates will be grouped into 2-3 "city centers" or "districts."
    *   **Rationale:** This makes the concept of "competitors" and "proximity" realistic. In the real world, cafes compete with other nearby cafes. This assumption allows you to calculate distance and identify the direct competitors who would benefit from revenue leakage.

3.  **Assumption: Closed Businesses Often Retain High Historical Ratings.**
    *   **The Assumption:** The businesses that are now closed were, on average, successful and well-regarded when they were open. We will assign them a slightly higher average historical rating than the currently open businesses.
    *   **Rationale:** This is the core reason the problem exists. A customer is only misled if the closed business looks attractive. If all closed businesses had a 1-star rating, nobody would ever choose them. This assumption creates the "bait" for the trap.

### Assumptions for Dataset 2: `reviews.csv`

This dataset contains the primary evidence for your analysis.

1.  **Assumption: Ghost Reviews are a Systematic, Not Random, Phenomenon.**
    *   **The Assumption:** For businesses marked as "Permanently Closed," a predictable percentage (e.g., 10-15%) of their total reviews will have a `review_date` that occurs *after* their `closure_date`.
    *   **Rationale:** This is the most crucial assumption. You are intentionally creating the "ghost review" phenomenon. This ensures that your identification script in Phase 1 will have something to find. These ghost reviews could be a mix of spam, bots, or legitimate reviews posted with a lag.

2.  **Assumption: Review Text and Rating are Strongly Correlated.**
    *   **The Assumption:** The sentiment of the `review_text` will be directly linked to the `rating` value. 5-star reviews will use positive keywords ("amazing," "best," "loved it"), while 1-star reviews will use negative keywords ("terrible," "avoid," "disappointed").
    *   **Rationale:** This makes your Sentiment Analysis phase meaningful. It guarantees that when you run an NLP model, it will produce results that are internally consistent. A positive ghost review for a closed business is more misleading than a negative one, and this assumption allows you to prove that.

3.  **Assumption: Review Volume is Proportional to Business Popularity.**
    *   **The Assumption:** Businesses with higher average ratings will also have a higher volume of reviews.
    *   **Rationale:** This adds a layer of realism and reinforces the problem. The most attractive (and therefore most misleading) closed businesses will have a larger digital footprint, amplifying their negative impact.

### Assumptions for Dataset 3: `customer_journeys.csv`

This dataset is a simulation layer used to measure the final business impact.

1.  **Assumption: Customer Choice is Rational but Uninformed.**
    *   **The Assumption:** A simulated customer's `initial_choice_id` is determined by a simple function of `rating` and `distance`. They will always choose the highest-rated business within a reasonable distance, *without knowing its operational status*.
    *   **Rationale:** This creates a predictable decision-making model that can be "fooled" by the high ratings of closed businesses. It's the mechanism that directly leads to the "misdirection" you are trying to measure.

2.  **Assumption: Misdirection Leads to Redirection, Not Abandonment.**
    *   **The Assumption:** When a customer's `initial_choice` is a closed business (`is_ghost_interaction = 1`), they do not give up their search. They are "redirected" to the *next-best available (i.e., open)* competitor.
    *   **Rationale:** This allows you to model **revenue leakage**. The revenue doesn't vanish; it flows from the intended (closed) business to a specific competitor. This makes the economic impact tangible and assignable.

3.  **Assumption: Economic Impact Can Be Standardized by Category.**
    *   **The Assumption:** Every customer journey has a potential monetary value based on its `search_category`. A visit to a "Cafe" is worth $15, a "Restaurant" is $50, and a "Bookstore" is $25.
    *   **Rationale:** This allows you to convert the abstract concept of "redirected footfall" into a concrete, measurable metric: `revenue_leaked`. It provides the final dollar amount for your economic impact study and executive summary.
