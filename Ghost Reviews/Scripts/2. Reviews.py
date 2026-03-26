import pandas as pd
import numpy as np
import random
import string
from datetime import datetime, timedelta

# --- Core Configurations ---
random.seed(99)
np.random.seed(99)

INPUT_FILENAME = 'simulated_businesses.csv'
OUTPUT_FILENAME = 'simulated_reviews.csv'

# Behavior variables
GHOST_REVIEW_PROBABILITY = 0.08      # Chance of reviewing a dead business post-closure
BURST_PROBABILITY = 0.05             # Chance a business experiences a "Review Bomb / Viral Spike"
SPAM_BOT_PROBABILITY = 0.03          # Chance a review is duplicated bot spam
CONTRADICTION_PROBABILITY = 0.02     # E.g., user clicked 1-star but text says "I loved it!"

TODAY = datetime.now()

print("[*] Initializing the Chaotic Ecosystem Review Simulator...")

# --- Combinatorial High-Cardinality Text Engine ---
# By combining pieces, we easily get >100,000 unique reviews
FRAGMENTS = {
    5: {
        'intro':["Absolutely fantastic.", "A revelation!", "Loved every second.", "Perfection.", "10/10."],
        'body':["The ambiance and quality were off the charts.", "Everything exceeded my highest expectations.", "You can tell they really care about their craft.", "My new favorite spot."],
        'outro':["Will definitely be coming back!", "Can't recommend it enough.", "Bringing my friends next time.", "Just wow."]
    },
    4: {
        'intro':["Pretty good overall.", "A solid choice.", "Really nice.", "I liked it.", "Very pleasant."],
        'body':["Quality was great, though it took a little while.", "Nearly perfect, just missing a tiny spark.", "A few hiccups but largely a wonderful time.", "Delivered exactly what was promised."],
        'outro':["I'll return soon.", "Good value.", "Worth a visit if you're in the area.", "Thumbs up."]
    },
    3: {
        'intro':["It was okay.", "Exactly average.", "Nothing special.", "Meh.", "Not bad, not great."],
        'body':["Met my expectations but didn't wow me.", "You get what you pay for.", "There are better places, but also worse.", "Totally middle of the road."],
        'outro':["Might go back, might not.", "It is what it is.", "Fairly standard.", "Could be better."]
    },
    2: {
        'intro':["Disappointing.", "Really fell short.", "Yikes.", "Not worth the hype.", "Below average."],
        'body':["We waited forever and it wasn't worth it.", "Staff seemed overwhelmed and quality suffered.", "The whole thing felt poorly managed.", "I wanted to like it, but I just can't."],
        'outro':["I'd suggest going elsewhere.", "Not returning.", "Save your money.", "Needs major improvements."]
    },
    1: {
        'intro':["Terrible.", "Worst ever.", "Absolute disaster.", "DO NOT GO HERE.", "Horrific."],
        'body':["Complete lack of respect for customers.", "Everything was awful, start to finish.", "A chaotic mess, ruined my night.", "They scammed us essentially."],
        'outro':["Avoid at all costs!!!", "Never stepping foot here again.", "Reporting this place.", "Zero stars if I could."]
    },
    'ghost': {
        'body':["Maps said it was open but it's boarded up?", "Drove an hour and it looks abandoned.", "Are they closed forever? Lights out.", "Says open online. Complete lie. Closed."],
    }
}

def generate_text(rating, is_ghost=False):
    """Dynamically builds a review, sometimes returning nulls, sometimes messy."""
    # Guardrail 43: Occasional completely empty text
    if random.random() < 0.08: return np.nan

    if is_ghost and random.random() < 0.7:
        text = random.choice(FRAGMENTS['ghost']['body'])
    else:
        # Guardrail 37 & Contradiction check
        effective_rating = rating
        if random.random() < CONTRADICTION_PROBABILITY: 
            effective_rating = 1 if rating == 5 else 5 # Oops, clicked wrong stars
            
        r_parts = FRAGMENTS[effective_rating]
        text = f"{random.choice(r_parts['intro'])} {random.choice(r_parts['body'])} {random.choice(r_parts['outro'])}"
    
    # Apply Typographical & Format Noise
    if random.random() < 0.1: text = text.lower() # lazy typist
    if random.random() < 0.05: text = text.upper() # ALL CAPS RANT
    if random.random() < 0.05 and len(text) > 10: 
        # Insert a realistic typo (duplicate char or drop char)
        idx = random.randint(0, len(text)-2)
        if random.random() < 0.5:
            text = text[:idx] + text[idx] + text[idx:]
        else:
            text = text[:idx] + text[idx+1:]
            
    return text

# --- Data Loading & SELF HEALING ---
try:
    df_biz = pd.read_csv(INPUT_FILENAME)
    print(f"[+] Successfully loaded {len(df_biz)} businesses.")
except FileNotFoundError:
    print(f"[!] ERROR: Cannot find '{INPUT_FILENAME}'. Run the business generator script first.")
    exit()

print("[-] Self-healing missing business data constraints...")
# If dates are entirely broken or missing, default to reasonable constraints
df_biz['opening_date'] = pd.to_datetime(df_biz['opening_date']).fillna(pd.to_datetime(TODAY - timedelta(days=1000)))
df_biz['closure_date'] = pd.to_datetime(df_biz['closure_date'])

# Handle missing stats from parent dataset gently
if 'review_count' not in df_biz.columns:
    df_biz['review_count'] = np.random.randint(1, 50, size=len(df_biz))
df_biz['review_count'] = df_biz['review_count'].fillna(np.random.randint(1, 10)).astype(int)

if 'average_rating' not in df_biz.columns:
    df_biz['average_rating'] = np.random.uniform(2.0, 5.0, size=len(df_biz))
df_biz['average_rating'] = df_biz['average_rating'].fillna(3.5).astype(float)


# --- Global User Ecosystem (Heavy Tailed Power Laws) ---
print("[*] Building global user population (incorporating power-law & behavioral profiles)...")
NUM_USERS = int(len(df_biz) * 3)
users =[]
for _ in range(NUM_USERS):
    user_id = f"USR-{random.randint(1000000, 9999999)}"
    # Behavioral biases: Some users are generous (bias +1), some are extremely critical (bias -1.5)
    sentiment_bias = np.random.normal(0, 0.7) 
    # Frequency tier: Power law for reviews. 
    frequency_weight = int(np.random.pareto(1.5) + 1)
    users.append((user_id, sentiment_bias, frequency_weight))

# Fast random.choices extraction weights
USER_IDS = [u[0] for u in users]
USER_BIASES = {u[0]: u[1] for u in users}
USER_WEIGHTS = [u[2] for u in users]


# --- Core Generation Loop ---
print("[-] Spawning temporal histories and simulated interactions...")
all_reviews =[]
review_id_counter = 10000

for index, biz in df_biz.iterrows():
    b_id = biz['business_id']
    b_open = biz['opening_date']
    b_close = biz['closure_date']
    b_status = biz.get('status', 'Open')
    b_rating_anchor = biz['average_rating']
    
    # Introduce Relational Dissonance (Sync lags). Actual counts might drift slightly from parent dataset
    expected_reviews = biz['review_count']
    drift = int(expected_reviews * random.uniform(-0.1, 0.1))
    target_reviews = max(0, expected_reviews + drift)
    
    if target_reviews == 0: continue

    # Lifecycle Timestamps & "Review Burst" configuration
    has_burst = target_reviews > 20 and random.random() < BURST_PROBABILITY
    burst_center = None
    if has_burst:
        valid_end = b_close if pd.notnull(b_close) else TODAY
        burst_days = max(1, (valid_end - b_open).days)
        burst_center = b_open + timedelta(days=random.randint(1, burst_days))

    # Pull user batch efficiently based on heavy-tail weights
    active_users = random.choices(USER_IDS, weights=USER_WEIGHTS, k=target_reviews)

    for i in range(target_reviews):
        uid = active_users[i]
        u_bias = USER_BIASES[uid]
        is_ghost = False

        # --- 1. DETERMINE DATE ---
        end_boundary = TODAY if pd.isnull(b_close) else b_close
        
        # Ghost Reviews Logic
        if pd.notnull(b_close) and random.random() < GHOST_REVIEW_PROBABILITY:
            is_ghost = True
            days_since_close = (TODAY - b_close).days
            if days_since_close <= 1: days_since_close = 2
            
            # Ghosts usually happen closely after closure (confused patrons finding the store closed)
            # Use beta distribution heavily skewed towards the early days after closure
            fraction = np.random.beta(1.5, 5) 
            r_date = b_close + timedelta(days=int(fraction * days_since_close))
        
        # Normal Life Review
        else:
            total_days = max(1, (end_boundary - b_open).days)
            
            # If we're inside a viral burst
            if has_burst and random.random() < 0.4: # 40% of reviews clump together
                time_fuzz = timedelta(days=int(np.random.normal(0, 3)))
                r_date = burst_center + time_fuzz
            else:
                r_date = b_open + timedelta(days=random.randint(0, total_days))
                
        r_date = min(max(r_date, b_open), TODAY) # Bound logic guard
        
        # --- 2. DETERMINE RATING (Lifecycle / Decay Aware) ---
        if is_ghost:
            raw_rating = np.random.choice([1, 2], p=[0.8, 0.2]) # Usually angry/confused about closed place
        else:
            # Baseline Anchor + User Persona Bias
            base_r = b_rating_anchor + u_bias + np.random.normal(0, 0.5)
            
            # Sentiment Decay (If a business closed, the last few months usually feature severe drop-offs in quality)
            if pd.notnull(b_close):
                days_to_end = (b_close - r_date).days
                if days_to_end < 90:
                    base_r -= 1.5 # Harsh drop-off

            raw_rating = int(np.clip(round(base_r), 1, 5))

        # --- 3. METADATA IMPERFECTIONS ---
        text = generate_text(raw_rating, is_ghost)
        
        # Add 'Helpful' upvotes following heavy tail distribution
        upvotes = int((np.random.pareto(1.2)) * (1 if raw_rating in [1,5] else 0.2)) # Polarizing gets more votes

        review_dict = {
            'review_id': f'REV-{review_id_counter}',
            'business_id': b_id,
            'user_id': uid,
            'review_date': r_date.date() if r_date else np.nan,
            'rating': float(raw_rating),
            'review_text': text,
            'helpful_votes': upvotes,
            'is_edited': 1 if random.random() < 0.05 else 0
        }
        all_reviews.append(review_dict)
        review_id_counter += 1

# --- Final Aggregation & Chaos Induction ---
df_reviews = pd.DataFrame(all_reviews)

print("[*] Injecting extreme noise vectors and structural imperfections...")

# Guardrail 45: Occasional duplicated bot spam 
spam_indices = np.random.choice(df_reviews.index, size=int(len(df_reviews)*SPAM_BOT_PROBABILITY), replace=False)
spam_rows = df_reviews.loc[spam_indices].copy()
spam_rows['review_id'] =[f"REV-{i}" for i in range(review_id_counter, review_id_counter+len(spam_rows))]
# Spammers heavily blast the same text
spam_rows['review_text'] = "Great link !! Buy followers online cheap >> link.com" 
spam_rows['rating'] = 5.0
df_reviews = pd.concat([df_reviews, spam_rows], ignore_index=True)

# Guardrail 43: System Missing/Nulling values intentionally
drop_indices = np.random.choice(df_reviews.index, size=int(len(df_reviews)*0.01))
df_reviews.loc[drop_indices, 'rating'] = np.nan # Accidental lost rating

drop_date_indices = np.random.choice(df_reviews.index, size=int(len(df_reviews)*0.015))
df_reviews.loc[drop_date_indices, 'review_date'] = np.nan # Log ingestion error

# Guardrail 44: Formatting shifts in output (simulate legacy migration formats and sloppy normalization)
def screw_up_dates(dt):
    if pd.isnull(dt): return np.nan
    if random.random() < 0.02: return dt.strftime('%Y/%m/%d') # Format variation
    if random.random() < 0.02: return dt.strftime('%m-%d-%y') # Legacy format
    return dt.isoformat()

df_reviews['review_date'] = df_reviews['review_date'].apply(screw_up_dates)

# Sort loosely by date (adding realism: mostly chronolocial but messy data ingests over time)
temp_dates = pd.to_datetime(df_reviews['review_date'], errors='coerce')
df_reviews['temp_sort'] = temp_dates

# Adding an ingestion stagger sort noise
stagger_noise = pd.Series([timedelta(days=random.randint(-5, 5)) for _ in range(len(df_reviews))], index=df_reviews.index)
df_reviews['temp_sort'] = df_reviews['temp_sort'] + stagger_noise

df_reviews.sort_values(by=['business_id', 'temp_sort'], inplace=True)
df_reviews.drop(columns=['temp_sort'], inplace=True)

df_reviews.to_csv(OUTPUT_FILENAME, index=False)

# --- Statistical Output Verification ---
print(f"\n[+] Generation Complete! Wrote {len(df_reviews)} reality-hardened reviews to '{OUTPUT_FILENAME}'.")
print("\n========== ECOSYSTEM AUDIT & ANALYTICS ==========")

# Null/Missing Value Checks
print("\n[-] Data Missingness Vectors:")
for col in df_reviews.columns:
    nulls = df_reviews[col].isnull().sum()
    if nulls > 0: print(f"    - '{col}' contains {nulls} missing records.")

# Validation Check of Data Synchronization (The Dissonance metric)
dissonance_ct = len(df_reviews[df_reviews['rating'].isnull()])
print(f"\n[-] Null Rating Rows (Ingestion Drop Error rate): {round(dissonance_ct / len(df_reviews)*100, 2)}%")

# Heavy Tailed Feature Check
max_upvotes = df_reviews['helpful_votes'].max()
median_upvotes = df_reviews['helpful_votes'].median()
print(f"\n[-] Vote Inequality: Most helpful review had {max_upvotes} votes. The median has {median_upvotes}.")

power_users = df_reviews.groupby('user_id').size()
print(f"[-] User Demographics: Average user leaves {round(power_users.mean(),1)} reviews, Top user left {power_users.max()} reviews.")

# Rating Contradiction / Sentiment Checks
five_star_complaints = df_reviews[
    (df_reviews['rating'] == 5) & 
    (df_reviews['review_text'].str.contains('Terrible|Awful|DO NOT', na=False, case=False))
]
print(f"\n[-] Real-life Edge Cases: Caught {len(five_star_complaints)} users rating 5-stars while cursing in the review text.")

spam_bot_ct = len(df_reviews[df_reviews['review_text'].str.contains('Buy followers', na=False, case=False)])
print(f"[-] Intercepted {spam_bot_ct} obvious spam bot requests masquerading as valid user sessions.")
