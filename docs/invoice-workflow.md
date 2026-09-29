# Invoice workflow and deployment

## Changes

- A Persian, RTL invoice layout for purchases and sales, with mobile item cards, real totals, payment balance, A4 print styling and downloadable PDF.
- Layout inspired by the public [Zoho minimal invoice sample](https://www.zoho.com/invoice/invoice-templates/sample/zoho-invoice-minimalist-template.pdf), adapted to Naseri ERP. No Canva assets or invented company address, tax identity or bank details are included.
- Saving a purchase opens its document automatically. Ordered/fully received purchases with items create one purchase invoice atomically; draft purchases remain nonfinancial documents. Saving a sale also opens its document.
- A purchases page is now available in navigation. It uses the existing supplier/product/warehouse records. Ordered purchases do not add stock; full receipt adds stock. Partial receipt and returns are not implemented in this change.
- Existing purchases are not invoiced merely by viewing them. A document without an accounting invoice is labelled unissued rather than presented as a paid/issued invoice.

## QR and privacy

The QR encodes an absolute frontend `/invoice/<signed-token>` URL. A phone can open it without ERP login or data from the original device's local storage, and download the PDF there.

The token grants access to that invoice: anyone possessing the URL can view it. Do not post private invoice links publicly. Public output excludes internal notes, warehouse name, phone numbers, addresses and account details. Signing prevents changing the invoice identifier inside a token; it is not encryption of the identifier.

Links expire after `INVOICE_SHARE_MAX_AGE` seconds (default 2592000, thirty days). Changes to the public document, including items, totals, payment balance or status, invalidate previously generated links. Reopen the invoice to get an updated QR. There is no independent manual token-revocation screen in this release. Changing `SECRET_KEY` also invalidates existing links and other Django signatures.

Document endpoints:

- Authenticated: `GET /api/invoice-documents/<sale|purchase>/<id>/`
- Signed public: `GET /api/invoice-documents/public/<token>/`

Public responses use no-store/noindex headers. Opening a document does not create an invoice, payment or stock movement.

## Hosting

1. Back up the database and current frontend before publishing.
2. Pull the commit into the backend checkout and restart the cPanel Python application. No database schema migration is introduced by this feature.
3. Build the frontend with `VITE_API_BASE_URL=https://api-naserierp.getsmartspace.ir/api`, or upload the verified release archive contents to the frontend web root.
4. Preserve SPA fallback routing: `/invoice/<token>` must serve `index.html`, not Apache's 404 page. Keep the API host separate from the frontend web root.
5. Verify one newly created test purchase, A4 preview, and QR on a different phone over HTTPS. Old already-printed local-storage QR links are not converted automatically.

Browser print should use A4, actual size/100%, with browser headers and footers disabled. PDFs contain rasterized Persian content, not searchable/selectable text. A physical printer was not used during local verification.

## Verification scope

Backend regression tests cover automatic invoice creation, stock receipt, rollback, draft handling, anonymous sharing, tampering, expiry, changed-document invalidation, and immutable received rows. Testing uses isolated local SQLite data; hosted MariaDB should receive a post-deployment smoke test. Visual review covers desktop, a 390px phone viewport, and short/multipage A4 PDFs. Review uses an available same-provider evaluator; no independent-provider review was available.

Final checks: 118 backend tests passed; no schema changes detected; production frontend build passed with existing CSS/chunk-size warnings. A local browser purchase automatically opened its correct 5000-toman invoice. Final one/four-page A4 samples were rendered and inspected; their QR codes decoded successfully from the rendered PDFs. Mobile PDF downloading was verified at 390px. The evaluator's second round could not complete because of its usage limit; the main agent performed final visual and QR checks after the evaluator's initial findings were fixed.

No production records were created, changed or removed for these feature checks. This commit does not enable automatic deployment.
