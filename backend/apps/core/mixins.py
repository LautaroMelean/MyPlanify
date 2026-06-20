class RatingMixin:
    def get_avg_rating(self, obj):
        val = getattr(obj, "avg_rating", None)
        return round(float(val), 1) if val is not None else None

    def get_review_count(self, obj):
        return getattr(obj, "review_count", None) or 0
