"""Local fallback package for `google` to help editor/type-checkers and runtime

This package provides a minimal `generativeai` module used only when the
official `google-generativeai` package is not installed. It mirrors a tiny
surface of the real API used by this repository: `configure` and
`GenerativeModel.generate_content`.
"""

__all__ = ["generativeai"]
