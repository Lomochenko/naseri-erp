# Financial correctness fixes

This patch corrects customer/supplier debt summaries and synchronizes invoice
balances whenever a customer or supplier payment is created, edited, moved to
another invoice, or deleted (including queryset deletion). Payment writes lock
affected invoices within a transaction. Nonpositive payments, overpayments and
payments against cancelled invoices are rejected with HTTP 400.

Customer account balance means payments minus confirmed/completed sale totals:
negative is debt. Confirmed/completed sales without a separate invoice are not
hidden from the debt summary. Line discounts are included in sale totals.
Partial draft-sale edits retain items when `items` is omitted. Use the existing
`update-status` endpoint for confirmation/completion instead of bypassing stock
checks through generic sale updates. Only drafts can be edited through that API.

The frontend labels account balance and debt explicitly, updates product counts
after deletion, removes mock dashboard/report records, and warns that advanced
report generation is not implemented. It does not manufacture financial reports.

## Verification

- Full backend suite: 100 tests passed using an isolated in-memory SQLite DB.
- Includes regressions for both payment ledgers, edits/deletes/moves, partial and
  full settlement, cancelled invoices, overpayments, API error responses, draft
  edits and line discounts.
- Migration check: no schema changes detected.
- Production frontend build passed. Existing CSS/chunk-size warnings remain.
- MariaDB/PostgreSQL-specific locking and production deployment were not tested
  by the SQLite suite; staging verification remains required.

## Deployment

GitHub push does not deploy this shared host automatically. Back up the database
and files, pull the commit in the server checkout, deploy a frontend build with
`VITE_API_BASE_URL=https://api-naserierp.getsmartspace.ir/api`, run the Django
checks in the configured virtual environment, and restart the Python application.
No schema migration is added by this patch. Do not run database flush/reset.

Existing inconsistent `paid_amount` values are not bulk rewritten by deployment.
Review existing invoices against their payment ledger before relying on them;
future payment writes recalculate the affected invoice. Invoices whose paid
amount was entered manually without payment records require reconciliation,
not an automatic destructive overwrite of the database.

Automatic chart-of-accounts setup/posting, automatic invoice creation, the
frontend purchase/payment workflow, historical ledger repair, PDF verification
and advanced reporting remain separate follow-up work. PostgreSQL and MariaDB
configuration and the retained live QA scenario are unchanged.
