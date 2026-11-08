from .choices import IngredientUnit


DELIVERY_COMMISSION_RATE = 0.098   # 배달 수수료 9.8%
DELIVERY_FEE = 3200
DEFAULT_PACKAGING_COST = 1000
DEFAULT_ADDITIONAL_FIXED_COST = 0

# TODO: 와이어프레임 기준으로 확정
OPERATING_HOUR_CHOICES = [f"{h:02d}:00" for h in range(0, 24)]
INGREDIENT_UNIT_CHOICES = IngredientUnit.values
