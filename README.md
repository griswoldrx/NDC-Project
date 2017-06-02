# NDC-Project
Supports research when matching claim National Drug Codes (NDC) numbers with drug names
This program can help interface with the RxNorm API and allow you to pass large numbers of NDC numbers for identification.
The program will return the unique RX concept identifier (RxCUI) as well as the drug name.
If there is a target group of drugs you are interested in, you can provide a list of RxCUI to match against.
This program also builds a txt file of cached results for RXCUI and drug information.  This cached information allows the quick processing of
tens of thousands of NDC numbers very quickly and without complete reliance on the API for each and every query.


The RxNorm API was developed and is maintained by the United States National Library of Medicine (NLM).  When analyzing NDC numbers it is important to
note that medical supplies, medical devices, and vaccines are not within the scope of this database.  Additionally some Over-the-Counter (OTC) medication
is in the RxNorm database, but it isn't the primary focus, so many NDC for OTC will not return useful information.
