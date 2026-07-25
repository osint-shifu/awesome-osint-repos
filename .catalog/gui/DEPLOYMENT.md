# Deploying the catalogue browser

Choose a stable public address, for example `https://osint-tools.example.com/`.

The GUI is a static site. It does not need a database server, Node.js, or a
Python process on the public host. Its `catalog.json` file is generated from the
repository CSV during the build.

## Build

Run from the repository root:

```bash
python3 .catalog/gui/build_static.py --domain osint-tools.example.com
```

The deployable files are created in `.catalog/gui/dist/`.

## Existing web hosting

1. Create the selected subdomain in the hosting panel.
2. Point its document root to a dedicated empty directory.
3. Add the DNS record requested by the hosting provider. This is normally an
   `A` record to the hosting IP or a `CNAME` record to the host name supplied by
   the provider.
4. Upload the contents of `.catalog/gui/dist/`, not the `dist` directory itself,
   to that document root.
5. Enable an SSL certificate and force HTTPS.
6. Verify that `/`, `/catalog.json`, `/styles.css`, and `/app.js` return HTTP 200.

After the public address works, add its URL to the main
repository README as the database browser link.

## Updating the public database

After `osint-repositories.csv` changes, rebuild and upload the generated files
again:

```bash
python3 .catalog/gui/build_static.py --domain osint-tools.example.com
```

This can later be automated through the hosting provider's deployment system,
SFTP, or a GitHub Actions workflow. No deployment automation is enabled by the
current local implementation.

## GitHub Pages alternative

The same static build can be published with GitHub Pages and a custom
subdomain. Configure the selected host as the Pages custom domain and point its
DNS `CNAME` record to `oryon-osint.github.io`. GitHub recommends domain
verification and supports HTTPS after the DNS record resolves.

Official references:

- <https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site>
- <https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages>
