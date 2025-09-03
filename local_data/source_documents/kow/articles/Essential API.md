# When to use Essential API

**Essential API** is emnos' weekly data-sharing interface that allows direct access to performance data via a secure API. It delivers a standardized CSV dataset that can be retrieved using your API username and API key, without needing to log into the emnos platform

## When to use Essential API

Use the Essential API if you:

1. Want to connect emnos data directly to your BI tools like Power BI, Tableau, or Qlik.
2. Need up-to-date, granular data in a fixed structure for your regular performance reporting (can also be achieved using KPI export).
3. Prefer to build your own aggregations and timeframes using raw, detailed data (can also be achieved using KPI export).

## What data Essential API provides

The Essential API delivers **weekly data** for the categories included in your subscription. Since it's a **standardized tool** used by multiple supplier partners, we aim to ensure consistency across all users. Because each partner may have different reporting needs, we provide the **data at a granular level**—allowing you to shape and aggregate it as needed. This approach offers maximum flexibility while maintaining a common foundation for everyone.

#### Metrics

* Sales, Units, Volume
* Promo Sales, Promo Units, Promo Volume
* Baskets
* Number of Selling Stores

#### Dimensions

* Granularity: EAN ID level (no product aggregates)
* Timeframe: Last 2 weeks, at day level (no time aggregates)
* Attributes: Category, Brand, EAN Name (as defined by the retailer) (no additional attributes)
* Sales channels:
  + One file for all transactions (offline + e-commerce)
  + One file for e-commerce only

For an additional fee, you can receive **historical data** (last 27 months, daily granularity) on your first API update.

![](images/1748878547424.png)

## How to use Essential API

#### Set up

1. Go to the API Admin page <https://pingodoce.emnos.com/admin/api>. (also accessible from the left navigation pane).
2. Note your API Username and API Key. This is a one-time setup.
3. Check the key’s validity under the "Valid until" field. You’ll be notified via email when your API key needs renewal.

![](images/1748878623281.png)

#### Making API calls

1. **To get the file containing all transactions** (both e-commerce and offline).

Endpoint: POST <https://pingodoce.emnos.com/>

Headers:

Content-Type: application/json

x-username: <API\_USERNAME>

x-api-key: <API\_KEY>

Request Body:

{}

Expected Response: CSV file containing all transactions (suggested filename: output.csv)

**2. To get the file containing e-commerce transactions only**

Endpoint: POST <https://pingodoce.emnos.com/ecommerce/>

Headers:

Content-Type: application/json

x-username: <API\_USERNAME>

x-api-key: <API\_KEY>

Request Body:

{}

Expected Response: CSV file containing e-commerce transactions only (suggested filename: output.csv)

**Files are updated weekly upon successul data load**. The newly generated file erases the data from previous week. Access the latest data from Wednesday morning onwards.

[Essential API Documentation 1.pdf](https://dyzz9obi78pm5.cloudfront.net/app/image/id/683dbed69fdc54c31f066922/n/essential-api-documentation-1.pdf)

## Essential API data structure & sample file

The data structure is the same for weekly updates and one-time historical data. The columns are in the order below:

| Column 1 |
| --- |
| EAN (Name) (ID) \| |
| EAN (Name) (Name) \| |
| Category \| |
| Brand \| |
| Date \| |
| Selling stores (All customers) \| |
| Sales (All customers) \| |
| Units (All customers) \| |
| Baskets (All customers) \| |
| Volume (All customers) \| |
| Promo sales (All customers) \| |
| Promo units (All customers) \| |
| Promo volume (All customers) \| |

[Essential API sample.csv](https://dyzz9obi78pm5.cloudfront.net/app/image/id/683ece3b8ea0f5612c095a92/n/essential-api-sample.csv)

## How to pull data manually

[Video: how-to-manually-retrieve-api-data.mp4](videos/how-to-manually-retrieve-api-data.mp4)
