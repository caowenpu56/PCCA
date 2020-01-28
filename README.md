# Quantifying urban areas with multi-source data based on percolation theory
by Wenpu Cao (PKU), Lei Dong (PKU), Lun Wu (PKU), and Yu Liu (PKU)

## Abstract
Quantifying urban areas is crucial for addressing associated urban issues such as environmental and sustainable problems. Remote sensing data, especially the nighttime light images, have been widely used to delineate urbanized areas across the world. Meanwhile, some emerging urban data, such as volunteered geographical information (e.g., OpenStreetMap) and social sensing data (e.g., mobile phone, social media), have also shown great potential in revealing urban boundaries and dynamics. However, consistent and robust methods to quantify urban areas from these multi-source data have remained elusive. Here, we propose a percolation-based method to extract urban areas from these multi-source urban data. We derive the optimal urban-rural threshold by considering the critical nature of the urban system with the support of the percolation theory. Furthermore, we apply the method with three open-source datasets - population, road, and nighttime light - to 28 countries. We show that the proposed method captures the similar urban characteristics in terms of urban areas from multi-source data, and Zipf's law holds well in most countries. The derived urban areas by different datasets show good agreement with the Global Human Settlement Layer (GHSL) and can be further improved by data fusion. Our study not only provides an efficient method to quantify urban areas with open-source data, but also deepens the understanding of urban systems and sheds some light on the multi-source data fusion in geographical fields.

## Replication data and code
- Raw_Data: Raw data (population, road, nightime light) in China.
- PCCA_Codes: Python codes to replicate the results of the paper.
- Urban_Results: Maps of urban areas delimited by PCCA.
- Validation_Data: Landsat-based urban reference maps, 0: Non-urban, 1: Urban, -999: Outside the city boundary.

Contact: caowenpu56@gmail.com
