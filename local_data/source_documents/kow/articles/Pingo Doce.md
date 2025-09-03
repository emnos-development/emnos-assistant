# Overview

# Overview

| Column 1 | Column 2 |
| --- | --- |
| Name \| | Pingo Doce, Jeronimo Martins group \| |
| Region \| | Portugal \| |
| Data update \| | * Transaction data for KPI export & Customer insights = Weekly on Wednesday morning * Recurrent KPI exports = Weekly on Thursday morning * Brand Performance, Brand Weekly and Category Weekly datastories = Weekly on Thursday morning * Category Deep Dive = Monthly on the Monday morning following the full month data's availability \| |
| Transactions held \| | Rolling last 27 month, all stores including Lidosol, all EANs \| |
| Customer Segmentation \| | Frequency, FACTS \| |

# Data provided by Pingo Doce to emnos

### Transactions

* rolling last 118 weeks of transactions (i.e. last 27 month), updated weekly
* both transactions with and without loyalty card are provided
* spend amount includes VAT and all discounts
* promotional transactions are identified
* returned transactions (with a negative quantity) are not included
* all sales channel are included (physical stores and e-commerce) and identified
* Lidosol stores are included
* transactions are identified at EAN level

### Updating process

Every week on Tuesday, Pingo Doce shares transactional data with emnos covering the **last two promotional weeks** (from Tuesday D-14 to Monday D-1). This two-week window ensures we capture:

* Complete data for the most recent week (Week D-7 to D-1), and
* Any delayed transactions from the prior week (Week D-14 to D-8) that may not have been included in the initial update.

By loading two weeks at once, we ensure the platform reflects the most accurate and complete picture of customer activity, even if some transactions are reported late.

Alongside transactions, we also receive **updated product and store attributes, as well as customer segmentations.** All new transactions are added to the platform—existing ones are never modified in the regular data flow.

The update runs overnight, and the **refreshed data is available every Wednesday morning** for on-demand reporting tools like KPI exports and Customer insights.

### Automated update frequency by insight type

* Recurrent KPI exports = Weekly on Thursday morning
* Brand Performance, Brand Weekly and Category Weekly datastories = Weekly on Thursday morning
* Category Deep Dive = Monthly on the Monday morning following the full month data's availability

# Frequency segmentation

The Frequency segmentation divides customers according to their purchasing frequency over a year i.e. based on their number of visits in Pingo Doce stores.

There are 4 segments from F1 - Most frequent to F4 - Most punctual customers. These 4 segments are built in a way that their size is constant and there are no fixed thresholds on purchasing frequency.

![](images/1739194663009.png)

# FACTS segmentation

FACTS stands for Frequency, Advocated Categories, Total Spend. This segmentation ranks customers relatively to each other based on 3 factors: Frequency, Category range, Total spend.

There are 3 segments:

![](images/1743425918099.png)
