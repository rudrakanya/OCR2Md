# v2 QC log

## Hand-offs (entry Opening/Closing; compare with Part III, A)

| Unit | Sections sum / target | Opening | Closing |
|---|---|---|---|
| Ch 4 | 5000 / 5,000 | takes up 3.5's last line ("Who held the hill itself in those years is not known") with Sīyaka II's eastern lim | the temple as the reign's one dated work at Udaypur. It gives no description of the building (Ch 5), no quotat |
| Ch 5 | 4000 / 4,000 | the temple faces east, but is entered today from the west (C05-PANDE-002, -011). | the flag-bearer and the inscribed name at the east doorway, not read (Ch 6 reads them). |
| Ch 6 | 4050 / 4,050 | the six lines of V.S. 1137 at the east door, with their named poet. | the inscribed mosques, dated but not described (Ch 7). |
| Ch 7 | 4250 / 4,250 | a colonial observer's nameless wall (C07-GEOHER-002). The observer is to be named only after the ingest (R9). | Vikrama's tank and its stated uses. |
| Ch 8 | 3800 / 3,800 | Dhāmadeva's four *biswa*, "taking water in hand", in 1229 (Part I, I.5). | the time-keepers' family and its hereditary service. |
| Ch 9 | 2800 / 2,800 | the lane on the left as one leaves the temple: Hindu and Muslim households, described by community, never by r | Daulatpur, as memory only, with no location given. |
| Ch 10 | 4200 / 4,200 | the V.S. 1220 record naming a Gujarat king at Udaypur (Part I, I.5). | the Gazetteer's sentence. |
| Ch 11 | 4250 / 4,250 | Beglar's tour of 1871–72. | the households and occupants at the record's edges. No recommendation. |
| Ch 12 | 3750 / 3,750 | a family's house, found buried in an excavation decades ago, cleaned out and lived in. | residents expecting visitors and trade; outsiders drawing up plans. No recommendation. |
| Afterword | 2750 / 2,750 | Tiwari's 2019 letter to the Collector. | the village under the temple, by content. No exhortation, no question, no claim beyond the last record. |

## checks_v2.py

```
C04: sections [650, 700, 900, 400, 1050, 1300] = 5000 (target 5000); problems 0; warnings 0
C05: sections [750, 650, 550, 550, 650, 400, 450] = 4000 (target 4000); problems 0; warnings 0
C06: sections [550, 500, 600, 450, 700, 600, 450, 200] = 4050 (target 4050); problems 0; warnings 0
C07: sections [750, 450, 650, 600, 650, 550, 600] = 4250 (target 4250); problems 0; warnings 0
C08: sections [800, 650, 550, 550, 300, 550, 400] = 3800 (target 3800); problems 0; warnings 1
  warn 8.5 Later trades *(the district in t: Gazetteer 4/5 of cited items (R8)
C09: sections [650, 300, 400, 600, 450, 400] = 2800 (target 2800); problems 0; warnings 0
C10: sections [800, 800, 850, 750, 650, 350] = 4200 (target 4200); problems 0; warnings 1
  warn 10.5 Revenue, brass and the railway : Gazetteer 26/35 of cited items (R8)
C11: sections [800, 850, 850, 750, 400, 600] = 4250 (target 4250); problems 0; warnings 0
C12: sections [750, 650, 650, 450, 400, 850] = 3750 (target 3750); problems 0; warnings 0
C13: sections [400, 600, 450, 300, 550, 450] = 2750 (target 2750); problems 0; warnings 0
primary in two units: none
```
