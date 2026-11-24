# 🍽️ Bangalore Zomato EDA — 8 Verified Findings

A data-driven synthesis of restaurant market structure, pricing economics, cuisine distribution, and consumer satisfaction across Bangalore, audited and verified directly against `zomato_features.csv` (8,921 restaurants) and `zomato_cuisines_long.csv` (28,770 exploded items).

---

1. **Electronic City Leads Restaurant Density:** Electronic City ranks #1 in Bangalore with 673 outlets, followed by Marathahalli (484), HSR (457), Whitefield (447), and BTM (397), heavily concentrating food service capacity across the southern and eastern IT corporate belts.

2. **Heritage Pockets Share a Quality Plateau:** Among localities with $\ge 50$ restaurants, Basavanagudi (4.047, $n=118$) and Frazer Town (4.027, $n=93$) post the highest delivery ratings; however, the 0.020 gap is far smaller than the sample standard deviation ($\sigma \approx 0.24-0.28$), demonstrating a shared high-quality baseline across traditional neighborhoods rather than a single runaway winner.

3. **86.7% of Restaurants Cluster Under ₹500:** Budget ($\le$ ₹200) and Affordable (₹201–₹500) restaurants make up 43.4% and 43.3% of the city's food options respectively, while Mid-Range (₹501–₹1000) accounts for 9.8%, and luxury Fine Dining (> ₹1000) represents just 3.5% of total supply.

4. **Dine-In Seating Imposes a 2.62× Cost Multiplier:** Restaurants offering indoor dine-in seating average ₹518.9 for two versus ₹198.3 for takeaway and delivery-only cloud kitchens—a 2.62$\times$ cost ratio (162% premium) reflecting commercial real-estate and service overheads.

5. **Exploded Counts Reveal Massive Beverage & Chinese Offerings:** Unpacking multi-cuisine strings reveals the true breadth of restaurant menus: North Indian (3,248) is #1, but secondary staples like Beverages (2,828), Chinese (2,764), Desserts (2,320), Fast Food (2,172), and Biryani (1,987) represent huge multi-cuisine volume invisible to single-tag counts.

6. **92.8% Non-Vegetarian Market with Universal Delivery:** 92.8% of restaurants in Bangalore serve non-vegetarian cuisine, leaving pure vegetarian eateries as a dedicated 7.2% niche concentrated in cultural strongholds, while home delivery is virtually universal across the dataset (99.8%).

7. **Satisfaction Base Rates Prove Price is Decoupled from Quality:** Base rates of high satisfaction ($\ge 4.2\star$) are nearly identical across every price tier—Budget (19.1%), Affordable (19.5%), Mid-Range (17.8%), and Fine Dining (20.4%)—yielding 942 elite-rated gems at or below ₹300 and a negligible Spearman correlation between cost and rating ($r_s = 0.057$).

8. **Extreme Skewness Distorts Budget Averages by 9.4×:** Review counts display extreme right-skewness where arithmetic means outstrip medians across all tiers, peaking in the Budget tier where the mean review count (1,341.9) is 9.4$\times$ the median (142.5), proving that viral institutions heavily bias standard averages.
