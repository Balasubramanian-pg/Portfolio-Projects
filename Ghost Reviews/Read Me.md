# Identifying and Quantifying the Impact of Ghost Reviews on Local Economies

### **Executive Summary**

Online reviews are the lifeblood of modern local commerce, yet a critical flaw exists in the ecosystem: **ghost reviews**. These are reviews posted on the pages of businesses that have permanently closed. Our investigation reveals that these digital phantoms are not benign artifacts; they actively mislead consumers, distort market dynamics, and cause quantifiable revenue leakage from informed businesses to defunct ones, before ultimately redirecting to a second-choice competitor.

This project undertook a three-phase approach to address this problem. We first developed a methodology to systematically **identify** ghost reviews by cross-referencing review timestamps with business closure dates. Second, we conducted a geospatial and economic **analysis** to simulate and measure the "misdirection effect," quantifying the redirected customer footfall and leaked revenue. Finally, we developed a robust, actionable **solution**: a "Business Inactivity Tagging" protocol for review platforms.

Our findings indicate that a significant percentage of consumer journeys are initially influenced by highly-rated closed businesses, leading to an estimated **$X million in annual revenue leakage** within our simulated city district. By implementing our proposed tagging system, review platforms can increase user trust, create a fairer competitive landscape, and recapture this lost economic efficiency, ensuring customer traffic flows to viable, operational businesses.

---

### **1. Project Context**

In the digital age, a business's online presence is its most valuable asset. Platforms like Google Maps, Yelp, and TripAdvisor serve as the primary discovery engine for consumers seeking local services, from cafes to clinics. The decision-making process is heavily skewed by two factors: average star rating and review volume.

However, when a business ceases operations, its digital presence does not vanish. Its online profile, complete with years of accumulated positive reviews, often remains active and discoverable. This creates a new and unaddressed challenge: **ghost reviews**. These are legitimate-looking reviews posted—either through user error, system lag, or malicious intent—long after a business has shut its doors. These phantom endorsements create a misleadingly positive image of a defunct business, creating a trap for unwary consumers.

### **2. The Problem Statement**

The persistence of ghost reviews on major platforms introduces significant friction into the consumer journey and creates an unfair competitive environment. This project seeks to answer three critical questions:

1.  **Identification:** Can we reliably and systematically identify "ghost reviews" at scale by analyzing publicly available data?
2.  **Quantification:** What is the measurable economic impact of these reviews? How much potential revenue is misdirected, and which active competitors are inadvertently benefiting or losing out?
3.  **Rectification:** What is a scalable, low-friction solution that review platforms can implement to mitigate this problem and restore market integrity?

Our hypothesis is that highly-rated closed businesses act as "black holes," attracting customer interest that must then be redirected, leading to wasted time for consumers and lost primary revenue opportunities for deserving, operational businesses.

### **3. Project Objectives & Key Performance Indicators (KPIs)**

*   **Objective 1:** Develop a repeatable process to identify ghost reviews with at least 99% accuracy.
    *   **KPI:** Percentage of correctly identified ghost reviews from a curated validation set.
*   **Objective 2:** Quantify the economic impact of ghost reviews in a sample market.
    *   **KPI:** Total calculated "Revenue Leaked" per business category and per competitor.
    *   **KPI:** Percentage of simulated customer journeys that begin with a "ghost interaction."
*   **Objective 3:** Design a practical solution for review platforms.
    *   **KPI:** A formal proposal document outlining the "Business Inactivity Tagging" system.

---

### **4. Methodology and Phased Approach**

Our project is structured into four distinct phases, moving from data discovery to a final, actionable solution.

#### **Phase 1: Data Acquisition & Ghost Identification**

The first step is to gather the necessary data. This involves creating a comprehensive dataset that simulates data from online business directories and review platforms.

*   **Step 1: Business Directory Aggregation:** We compile a master list of businesses, including their name, category, geographic coordinates (latitude/longitude), and most importantly, their operational **status** (`Open` or `Permanently Closed`) and a `closure_date` for the latter.
*   **Step 2: Review Data Collection:** For each business, we gather all associated reviews, capturing the rating, text, and `review_date`.
*   **Step 3: The "Ghost" Filter:** The core of this phase is a simple but powerful operation. We merge the two datasets and apply a filter to isolate reviews where the `review_date` is more recent than the business's `closure_date`. The output is a clean list of all identified ghost reviews.

#### **Phase 2: Qualitative & Sentiment Analysis**

Once identified, we need to understand the *nature* of these ghost reviews. Are they positive and misleading, or are they negative warnings?

*   **Step 1: Sentiment Scoring:** We apply a pre-trained Natural Language Processing (NLP) model to the `review_text` of each ghost review. This assigns a sentiment score (e.g., from -1.0 for highly negative to 1.0 for highly positive).
*   **Step 2: Insight Generation:** We analyze the distribution of these scores. Our key finding is that a majority of ghost reviews carry a positive sentiment, confirming that they are actively misleading consumers by praising a service that no longer exists.

#### **Phase 3: Geospatial & Economic Impact Analysis**

This is the most critical phase, where we measure the real-world impact. We simulate customer behavior to understand how ghost reviews affect decisions.

*   **Step 1: Simulating the Customer Journey:** We generate thousands of simulated "customer journeys." Each journey consists of a customer at a specific location looking for a business in a certain category (e.g., "Cafe").
*   **Step 2: Modeling the "Uninformed Choice":** We model a customer's initial choice based on a combined "attractiveness score" (a function of a business's average rating and its proximity to the customer). Crucially, this model is "uninformed" of the business's operational status.
*   **Step 3: Detecting the Misdirection:** We flag every journey where the initial choice is a closed business as a "ghost interaction."
*   **Step 4: Quantifying Revenue Leakage:** For each ghost interaction, we identify the next-best *open* competitor the customer would be redirected to. We then assign a standard transaction value based on the business category (e.g., $15 for a cafe). This value represents the "revenue leaked" to a secondary choice, a direct measure of economic inefficiency.

#### **Phase 4: Synthesis & Solutioning**

In the final phase, we consolidate our findings and formulate a recommendation. The analysis from Phase 3 provides undeniable evidence that the lack of clear "closed" signals on business profiles leads to quantifiable economic distortion.

---

### **5. The Proposed Solution: "Business Inactivity Tagging"**

Based on our findings, we propose a simple, elegant, and highly effective solution for review platforms.

*   **Concept:** A clear, visually distinct "Permanently Closed" or "Inactive" tag should be prominently displayed on the profile of any business confirmed to be out of operation.
*   **Implementation:**
    1.  **Filtering at the Source:** Businesses with this tag should be automatically filtered out from default search results (e.g., "cafes near me").
    2.  **Disabling New Reviews:** The ability to post new reviews for tagged businesses should be disabled, preventing the creation of new ghost reviews.
    3.  **Historical Transparency:** The profile should remain accessible via a direct link for historical reference, but with clear warnings that the business is no longer operational.

**Benefits of this Solution:**
*   **For Consumers:** Eliminates confusion and wasted time, leading to a more trustworthy and efficient user experience.
*   **For Open Businesses:** Creates a level playing field where they compete only against other operational businesses, not the ghosts of past successes.
*   **For Platforms:** Increases user trust, data quality, and the overall integrity of their ecosystem.

### **6. Project Deliverables**

1.  **A Comprehensive Report:** This document, detailing the project's context, methodology, findings, and recommendations.
2.  **An Interactive Dashboard (Power BI/Tableau):** A dashboard visualizing the key findings, including a map of ghost review hotspots, a breakdown of revenue leakage by category, and a list of the most impacted competitors.
3.  **A Formal Proposal:** A presentation deck outlining the "Business Inactivity Tagging" solution, designed for stakeholders at major review platforms.
