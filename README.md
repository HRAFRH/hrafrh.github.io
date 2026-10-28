# Achraf RAHIBE | Engineering Portfolio

[Visit the portfolio](https://hrafrh.github.io/)

Sixteen individual aircraft and system projects are visible directly on the homepage and Projects page. The 35 detailed records and five platform collections remain accessible. The blog contains 24 project stories with documented challenges, contributions and validation.

## Maintain the site

Edit content/projects.json for the detailed engineering records and content/collections.json for the five platform portfolios. Asset mappings are in content/platform-media.json. Add verified photos or clearly labeled diagrams under docs/media/. Keep record IDs stable so old links remain usable.

Run python build_portfolio.py. It generates the detailed records and then executes build_collections.py to assemble the main platform pages. Commit the source and generated docs directory. GitHub Pages publishes main, /docs.

Blog entries are maintained in the generator and content/additional-blog.json. Report metadata is in content/papers.json and content/vtol-media.json. The searchable Documents library organizes 13 public report versions across five document types; build_document_library.py generates the library after the platform and resume builders.

## Public material

Photographs, technical illustrations and edited report samples are labeled according to their role. Private conversations, raw flight logs, restricted reports, credentials, client costs and private source files are excluded. Client identities are omitted from the project narratives.

The visual direction is inspired by https://nikoweaver.github.io/. Project descriptions and supplied photographs relate to Achraf's own work. Software logos retain their owners' trademarks; sources are recorded in docs/assets/logos/ATTRIBUTION.txt.

The final build step, build_project_showcase.py, maintains the individual project presentation. New stories are in content/project-stories.json. Add matching project images to the existing records without replacing confidential-vessel reference labels.
