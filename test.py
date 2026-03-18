from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, date, timezone
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from typing import Optional, List, Dict, Any, Tuple
import uuid
import json

# Errors
class TransactionError(Exception):
    """Raised when transaction input fails validation."""

# Domain Model
@dataclass
class Transaction:
    id: str
    transaction_type: str            # "income" | "expense"
    amount: str                      # store as "1234.50" to preserve decimal accuracy
    currency: str                    # e.g. "THB"
    date: str                        # ISO "YYYY-MM-DD"
    category: str
    payment_method: str              # e.g. "cash", "bank_transfer", "e_wallet"
    client_name: Optional[str] = None
    vendor_name: Optional[str] = None
    note: Optional[str] = None
    tags: List[str] = None
    created_at: str = ""             # ISO timestamp in UTC with Z

# Mock reference lists
INCOME_CATEGORIES = {"freelance", "salary", "bonus", "investment", "other_income"}
EXPENSE_CATEGORIES = {"food", "transport", "software", "equipment", "rent", "other_expense"}
PAYMENT_METHODS = {"cash", "bank_transfer", "e_wallet", "card", "other"}

DEFAULT_CURRENCY = "THB"

# Helpers
def _now_utc_z() -> str:
    # timezone-aware UTC, formatted with Z
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")

def _clean_str(value: Any) -> Optional[str]:
    if isinstance(value, str):
        v = value.strip()
        return v if v else None
    return None

def _sanitize_tags(tags: Any) -> List[str]:
    if tags is None:
        return []
    if not isinstance(tags, list):
        raise TransactionError("tags must be a list of strings.")
    out: List[str] = []
    for t in tags:
        if isinstance(t, str):
            s = t.strip()
            if s:
                out.append(s)
    return out

def _parse_amount(value: Any) -> Decimal:
    try:
        amt = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        raise TransactionError("Amount must be numeric.")

    if amt <= 0:
        raise TransactionError("Amount must be greater than 0.")

    # 2 decimal places (money)
    return amt.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

def _parse_date(value: Any) -> date:
    if isinstance(value, date):
        return value
    if not isinstance(value, str):
        raise TransactionError("Date must be a string in YYYY-MM-DD format.")
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        raise TransactionError("Invalid date format. Use YYYY-MM-DD.")

def _validate_type(tx_type: Any) -> str:
    if tx_type not in ("income", "expense"):
        raise TransactionError("transaction_type must be 'income' or 'expense'.")
    return tx_type

def _validate_category(tx_type: str, category: Any) -> str:
    cat = _clean_str(category)
    if not cat:
        raise TransactionError("Category is required.")

    if tx_type == "income" and cat not in INCOME_CATEGORIES:
        raise TransactionError(f"Invalid income category: {cat}")

    if tx_type == "expense" and cat not in EXPENSE_CATEGORIES:
        raise TransactionError(f"Invalid expense category: {cat}")

    return cat

def _validate_payment_method(method: Any) -> str:
    m = _clean_str(method)
    if not m:
        raise TransactionError("payment_method is required.")
    if m not in PAYMENT_METHODS:
        raise TransactionError(f"Invalid payment_method: {m}")
    return m

def _validate_currency(cur: Any) -> str:
    c = _clean_str(cur) or DEFAULT_CURRENCY
    if len(c) != 3 or not c.isalpha():
        raise TransactionError("currency must be a 3-letter code (e.g., THB, USD).")
    return c.upper()

def _enforce_client_vendor_rules(tx_type: str, client: Optional[str], vendor: Optional[str]) -> None:
    if tx_type == "income" and vendor is not None:
        raise TransactionError("Income transaction should not include vendor_name.")
    if tx_type == "expense" and client is not None:
        raise TransactionError("Expense transaction should not include client_name.")

def _is_future_date(d: date) -> bool:
    return d > datetime.now().date()

def _fingerprint_for_duplicate(tx: Transaction) -> Tuple[str, str, str, str, str]:
    # Simple fingerprint for soft duplicate warning
    party = tx.client_name or tx.vendor_name or ""
    return (tx.transaction_type, tx.amount, tx.date, tx.category, party.lower())

# In-memory Repository
class InMemoryTransactionRepo:
    def __init__(self) -> None:
        self._items: List[Transaction] = []
        self._fingerprints: set[Tuple[str, str, str, str, str]] = set()

    def add(self, tx: Transaction) -> Tuple[Transaction, List[str]]:
        warnings: List[str] = []

        fp = _fingerprint_for_duplicate(tx)
        if fp in self._fingerprints:
            warnings.append("Possible duplicate: similar transaction already exists (same type/amount/date/category/party).")

        self._items.append(tx)
        self._fingerprints.add(fp)
        return tx, warnings

    def list_all(self) -> List[Transaction]:
        return list(self._items)

    def summary(self) -> Dict[str, str]:
        income = Decimal("0")
        expense = Decimal("0")

        for tx in self._items:
            amt = Decimal(tx.amount)
            if tx.transaction_type == "income":
                income += amt
            else:
                expense += amt

        net = income - expense
        return {
            "total_income": str(income.quantize(Decimal("0.01"))),
            "total_expense": str(expense.quantize(Decimal("0.01"))),
            "net_profit": str(net.quantize(Decimal("0.01"))),
        }

# Service / Use Case
def create_transaction(repo: InMemoryTransactionRepo, payload: Dict[str, Any], *, allow_future_date: bool = False) -> Dict[str, Any]:

    tx_type = _validate_type(payload.get("transaction_type"))
    amt = _parse_amount(payload.get("amount"))
    d = _parse_date(payload.get("date"))
    if (not allow_future_date) and _is_future_date(d):
        raise TransactionError("Date cannot be in the future.")

    category = _validate_category(tx_type, payload.get("category"))
    payment_method = _validate_payment_method(payload.get("payment_method"))
    currency = _validate_currency(payload.get("currency"))

    client_name = _clean_str(payload.get("client_name"))
    vendor_name = _clean_str(payload.get("vendor_name"))
    _enforce_client_vendor_rules(tx_type, client_name, vendor_name)

    note = _clean_str(payload.get("note"))
    tags = _sanitize_tags(payload.get("tags"))

    tx = Transaction(
        id=str(uuid.uuid4()),
        transaction_type=tx_type,
        amount=str(amt),
        currency=currency,
        date=d.isoformat(),
        category=category,
        payment_method=payment_method,
        client_name=client_name,
        vendor_name=vendor_name,
        note=note,
        tags=tags,
        created_at=_now_utc_z(),
    )

    saved, warnings = repo.add(tx)

    return {
        "status": "success",
        "transaction": asdict(saved),
        "summary": repo.summary(),
        "warnings": warnings,
    }

# Output
def pretty_print(result: Dict[str, Any]) -> None:
    print(json.dumps(result, indent=2, ensure_ascii=False))

# Demo
if __name__ == "__main__":
    repo = InMemoryTransactionRepo()

    # Income
    r1 = create_transaction(repo, {
        "transaction_type": "income",
        "amount": "5000",
        "date": "2026-02-14",
        "category": "freelance",
        "payment_method": "bank_transfer",
        "currency": "THB",
        "client_name": "ABC Studio",
        "note": "Final payment",
        "tags": ["design", "urgent"]
    })
    pretty_print(r1)

    # Expense
    r2 = create_transaction(repo, {
        "transaction_type": "expense",
        "amount": 799,
        "date": "2026-02-14",
        "category": "software",
        "payment_method": "card",
        "currency": "THB",
        "vendor_name": "Adobe",
        "note": "Monthly subscription",
        "tags": ["tools"]
    })
    pretty_print(r2)
