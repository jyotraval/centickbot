
# <u>generalized questions (multiple query - same intend grp)</u>

### 04 jan 2025

- exposed to actual user queries: email format
- granted read access and awaiting download access

### 25 dec


FINAL approch. -->
```
Data extraction:
SQL -> get raw data -> normalize (lowercase and all that) -> save final processed data

Embedding: 
processed data -> MPNet or MiniLM -> metadata and vectors

Clustering/grouping:
vectors -> downscale (dimensionality reduction) -> HDBSCAN or K-means -> clusters

Naming / generalizing:
clusters -> retrieve random 10–15 items from every cluster -> pass sample to NLP or Keywords + Zero-shot classification-> category like OTP-related, refund, or anything
```

### Summary:

1. Preprocess text > clean & normalize
2. Embed text > MPNet / MiniLM → store in FAISS
3. Reduce dimensions > UMAP (10–50 dims)
4. Run `HDBSCAN` > detect natural clusters & filter noise **OR** Run `K-Means` (k=20) on remaining/noise or to consolidate > 20 clusters
6. Sample texts per cluster > extract `keywords / zero-shot labels` > assign topic names
7. Rank clusters by size > top FAQ topics

<br>

![query grouping](GeneralizeQuery\centraltickquery.png)

![query grouping](https://raw.githubusercontent.com/jyotraval/centickbot\GeneralizeQuery\centraltickquery.png)

### 23 dec 2025

- yt on clusting algo - HDBSCAN
- drafted rough idea
```
Data extraction:
raw data -> normalize

processed data -> vectors

vectors -> HDBSCAN / k-means -> clusters

clusters -> keyword frequecy -> get genreal label
```

### 21 dec 2025

- initial taking one vector, cosim with every other
- Cosine similarity between two vectors = $O(d)$, $d$ = embedding dimension. Linear scan for one query vector = $O(n*d)$. OVERALL: $O(n^2 * d)$

- learnt about clustering: optimsed approch
- methods: kmeans, hirarical, dbscan, shilutte score.
- going with dbscan, assumeing dataset must be large.


---

# <u>MCP server Working - DONE</u>

### 19 dec 2025

- added dummy data
- tested and verifed.

### 18 dec 2025

- leanrd how to use it
- confure it on claude desktop
- mcp server connection to  claude desktop - done

- impnedted more tools (extra)
    - **get_available_seats** - list of all available (vacant) seats with their prices
    - **book_ticket** - Book a ticket for a user

### 17 dec 2025

- toold immeneted (pre-listed)
    - **cancel_booking** - Cancel a booking and initiate refund if applicable
    - **get_refund_status** - Get refund status for a booking
    - **create_ticket** - Create a support ticket for human assistance

### 15 dec 2025

- imenpted in acttual code, using supabase/postrgree.
- tools immented: (pre-listed) 
    - **get_booking** - Fetch booking details using booking ID
    - **list_user_bookings** - List all bookings for a user

### 15 dec 2025

- understood core meaning of those tools, brainstome about what may be sql scehma for query for bot to execute.
- dfrafted what can be sql schema

### 14 dec 2025

- nahashu impmented fundamental mcp template, listed what will be core tools.


### 12 dec2025

- learnt about MCP thing


---

# <u>RAG based chatbot **completed!!!**</u>

### 9dec 2025

- nehashu implemented FASTapi to creant an public endpoint.

- NPL thing which was pending had been emeplemtned with use of groq api.
```.env
.env template
PINECONE_API_KEY=apikey
PINECONE_IDX_HOST = idxhostlink
PRODUCTION='false' <- true while deplyoung
FILES_ROOT_PATH =data\\ <- vary
GROQ_API_KEY=groqapikey
MODEL=modelthatinuse
```

### 8dec 2025

- working on embedding and pinecone unsperting
- pinecone namespaces, and search query
- connect everything, 
-  **note: `connector.py` this is final script where evrything will be connected and api will interact on this file**

- **CHECKPOINT** - getting topk from db is done!!

### 7dec 2025
- understand pinecone db, how it works, mainly `pinecone` lib
- pinecone does embedding thing, no need for external embeddinf models
- droped idea of `FAISS` for inital phase and shifted directly to `pinecone` -> effective + alredy in use
- based on pinecone upsert change reader files. 
- changes `list[str]` -> `list[dict['id': , 'text':]]`

- new effective approch - shfted from `tiktoken` to normal `word based chunking` -> **reduce depedenacies** (main thing)

### 6 dec 2025
- scripted readers for bot. This utility will read files, data retrieved from files via this reader will be embedded
- normalised data to be veoctorised

- csv to string list
- `PyPDF2` used ot parse pdf
- csv, txt, pdf can be used.
- `readers\csvreader.py` `readers\txtreader.py` `reader\pdfreader` used tiktoken to get chunks 


### 5th Dec 2025

- Scrapped using selenuim.immented `faq_scraper.py` to gather info, like FAQs.

- Storeed it in faqs.cvs- enhanced `faq_scraper.py` using gpt - > added comments and better error handling.
- Imented `tnc_scraper.py` - > tnc.csv
- `policy_sraper.py` - > policy.csv
- Data gathering done for initial phase done.
- cvs formate `section` - > `Clause Content`
- `..\scraper\..` will be update via ci/cd pipeline after every update in site. (corn job / manual -  optional)

### 4th dec 2025 

- Got `Chatbot Architecture.docx`
- understand client req and problem, and current solution.

- Build an MVP type system arctitecture - MY APPORCH

![CentickBOTv1](https://raw.githubusercontent.com/jyotraval/centickbot/refs/heads/main/PRD_approch/CentickBOTv1.png)
