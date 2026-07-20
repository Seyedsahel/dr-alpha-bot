def format_service_price(service):

    minimum_price = getattr(service, "minimum_price", None)
    maximum_price = getattr(service, "maximum_price", None)

    if not minimum_price:
        return "تماس بگیرید"

    if maximum_price and maximum_price > minimum_price:
        return f"{minimum_price:,} تا {maximum_price:,} تومان"

    return f"{minimum_price:,} تومان"