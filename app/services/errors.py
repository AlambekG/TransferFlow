class AppError(Exception):
    pass


class NotFoundError(AppError):
    pass


class InsufficientFundsError(AppError):
    pass


class SameAccountError(AppError):
    pass


class CurrencyMismatchError(AppError):
    pass


class FraudDetectedError(AppError):
    pass
