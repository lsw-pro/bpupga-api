# BPUPGA API documentation

Static documentation for the BPUPGA local Python API, prepared for GitHub Pages.

Expected website after enabling Pages: <https://lsw528.github.io/bpupga-api/>

Source page: <https://lsw528.github.io/bpupga-api/source.html> (also accepts `source/`).

The website is public and visitors do not need a GitHub or ChatGPT account.
Publishing still requires a repository owner to configure Pages once.

## Publish

1. Keep this repository **Public**.
2. Open **Settings → Pages**.
3. Under **Build and deployment**, choose **Deploy from a branch**.
4. Select branch **main** and folder **/docs**, then **Save**.
5. Wait for the Pages deployment, then use the **Visit site** link.

The `.nojekyll` file keeps these prebuilt files unchanged. No Python server,
package installation, access token in website code, or frontend login is needed.
Later commits to `main/docs` update the website automatically.

## Contents

- Twelve documentation pages with the original navigation and search.
- API signatures, parameters, returns, errors and source line anchors.
- Python examples and `examples.zip` downloads.
- The original local JSON run inspector, which reads visitor-selected files in
  the browser; it does not submit remote benchmark jobs.

This repository contains the documentation and the facade source snapshot shown
on the source page. The examples that run actual models require the complete
research checkout and its method dependencies, as explained by the installation
page. This documentation repository is not a standalone model distribution.

Only the exported `docs/` files and this README are needed for publication.
The existing ChatGPT-hosted site is a separate deployment.
