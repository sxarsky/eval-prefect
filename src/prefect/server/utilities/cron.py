"""
Pure helpers for parsing cron expressions.

Supports the three shapes Prefect's scheduling surface accepts:

- **5-field cron** — ``minute hour day_of_month month day_of_week``
  (the standard POSIX cron layout). ``seconds`` is returned as ``"0"``.
- **6-field cron with leading seconds** — ``seconds minute hour day_of_month month day_of_week``
  (the 5-field form with a leading seconds field).
- **Macros** — ``@daily``, ``@hourly``, ``@weekly`` (and their common aliases).

Invalid input raises ``ValueError`` naming the offending token.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CronParts:
    """Structured form of a parsed cron expression.

    Every field is a raw cron token string (e.g. ``"0"``, ``"*/5"``, ``"1-5"``).
    Callers are expected to feed this into a downstream cron evaluator; the
    goal of this helper is to normalise the input shape, not to compute
    fire times.
    """

    seconds: str
    minutes: str
    hours: str
    day_of_month: str
    month: str
    day_of_week: str


_MACROS: dict[str, CronParts] = {
    "@hourly": CronParts("0", "0", "*", "*", "*", "*"),
    "@daily": CronParts("0", "0", "0", "*", "*", "*"),
    "@midnight": CronParts("0", "0", "0", "*", "*", "*"),
    "@weekly": CronParts("0", "0", "0", "*", "*", "0"),
}


def _validate_token(token: str, field_name: str) -> str:
    """Return ``token`` after a light per-field validity check.

    This does not attempt full cron-grammar validation (ranges, lists,
    step values, named weekdays, etc.). It catches obvious junk so the
    caller gets a clear diagnostic pointing at the offending field name
    and value.
    """
    if not token or token.isspace():
        raise ValueError(f"cron: empty {field_name} token")
    allowed = set("0123456789*/,-LW#?")
    # Also permit named-weekday and named-month abbreviations (3 alpha chars).
    if any(c not in allowed for c in token) and not token.isalpha():
        raise ValueError(
            f"cron: invalid {field_name} token {token!r} "
            "(expected digits, '*', ',', '-', '/', or a named alias)"
        )
    return token


def parse_cron_expression(expr: str) -> CronParts:
    """Parse a cron expression into its structured ``CronParts`` form.

    Accepts 5-field cron, 6-field cron with leading seconds, and the
    ``@daily`` / ``@hourly`` / ``@weekly`` macros. Raises ``ValueError``
    on malformed input; the error message names the offending token.

    Args:
        expr: The cron expression as a string.

    Returns:
        A ``CronParts`` instance with one attribute per cron field.
    """
    if not isinstance(expr, str):
        raise ValueError(f"cron: expected str, got {type(expr).__name__}")

    trimmed = expr.strip()
    if not trimmed:
        raise ValueError("cron: empty expression")

    if trimmed.startswith("@"):
        macro = trimmed.lower()
        if macro not in _MACROS:
            raise ValueError(f"cron: unknown macro {macro!r}")
        return _MACROS[macro]

    tokens = trimmed.split()
    if len(tokens) == 5:
        minute, hour, dom, month, dow = tokens
        return CronParts(
            seconds="0",
            minutes=_validate_token(minute, "minute"),
            hours=_validate_token(hour, "hour"),
            day_of_month=_validate_token(dom, "day_of_month"),
            month=_validate_token(month, "month"),
            day_of_week=_validate_token(dow, "day_of_week"),
        )
    if len(tokens) == 6:
        seconds, minute, hour, dom, month, dow = tokens
        return CronParts(
            seconds=_validate_token(seconds, "seconds"),
            minutes=_validate_token(minute, "minute"),
            hours=_validate_token(hour, "hour"),
            day_of_month=_validate_token(dom, "day_of_month"),
            month=_validate_token(month, "month"),
            day_of_week=_validate_token(dow, "day_of_week"),
        )
    raise ValueError(
        f"cron: expected 5- or 6-field expression or a supported macro, "
        f"got {len(tokens)} field(s) in {trimmed!r}"
    )
