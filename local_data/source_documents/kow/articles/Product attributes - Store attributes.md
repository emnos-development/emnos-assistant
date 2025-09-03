# What is a custom attribute

The "**Product attributes**" and "**Store attributes**" features enable Tenant Managers to update their organization's custom attributes to keep their data complete and relevant at all times.

## What is a custom attribute

The emnos platform contains 3 different types of attributes to enrich the data available on Product and Store dimensions.

1. **Retailer attributes** are maintained by the retailer and automatically updated during the regular data updates. They include attributes like: product description, brand, size, volume, store type etc. Any change of value or naming for these attributes need to be agreed with and operationally handled by the retailer's teams.
2. **Computed attributes** are maintained by emnos based on external data sources (like FEDAS attributes) or applying an aggregation rule on a Retailer attribute (like Regiao\_Nielsen which is aggregated from the Region attribute). They are automatically updated during the regular data updates. Any change of value or naming for these attributes need to be agreed with and operationally handled by the emnos team.
3. **Custom attributes** are created on-demand by emnos for our clients (retailer & supplier) and maintained by the clients' teams. They include attributes like: model name, manufacturer, product segment, sales area etc. They can be updated at any time by Tenant Manager users of each client organization. They are not updated with the regular data updates. Any change of value is completely up to the clients' decision. The Tenant Manager can handle it in full autonomy at any time.

## How to access Product attributes and Store attributes

The features are available in the Platform management topic, in the navigation panel of the emnos platform, on the left side of the screen.

![](images/1731667530509.png)

## How to use Product attributes and Store attributes

#### Creating a new custom attribute

Contact your emnos account manager telling them the name and type of attribute you need. We will create it for you. The available types are:

* text
* date
* number
* boolean (3 possible values: Y, N or empty)

#### Changing the name of a custom attribute

Attributes names cannot be changed. If you wish to keep the values but need a new name, then contact your emnos account manager. We will delete the attribute and create a new one with a different name but keeping the same values for each product or store.

#### Updating the values of an existing custom attribute

To update the values of an existing custom attribute, you must upload a csv file (comma separated) at the second step of the Product/Store attributes update process:

![](images/1731689920851.png)

The uploaded file must have this structure:

* first column called "member\_key" contains all stores or products identifiers
* next column has the attribute name as header and contains the corresponding value for each store or product

You can update several custom attributes at the same time, as long as they belong to the same dimension (Product or Store). Only include the custom attributes you wish to update. Any retailer or computed attribute you will include will be ignored.

Example of file to update 2 custom store attributes:

* BIKE\_REPAIR is a boolean, it indicates if the store offers a bike repairing service or not
* SALES\_AREA is a text, it indicates which commercial area the store is included in

![](images/1731680113241.png)

In case of doubt on the file format, an empty template can be downloaded:

![](images/1731680459815.png)

In case of doubt on the member keys to update or the values the custom attribute should have, an extract of the current database can be downloaded at the first step of the Product/Store attributes update process:

![](images/1731680870398.png)

The database extract is a comma separated csv file that follows the structure below:

![](images/1731688323264.png)

Once you have successfully uploaded your update file, the platform will give you an overview of the changes that will be processed. If you are fine with these changes, save the file.

![](images/1731691603935.png)

The update will take a few minutes. You will be notified by e-mail once the attributes are ready for use.

## Introduction video to Custom attribute update

[Video: update-custom-attributes.mp4](videos/update-custom-attributes.mp4)
